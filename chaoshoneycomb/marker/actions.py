# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional, cast

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaoshoneycomb import honeycomb_client

__all__ = ["add_marker"]


def add_marker(
    message: str,
    marker_type: str = "chaostoolkit-experiment",
    dataset_slug: str = "__all__",
    url: Optional[str] = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Add a marker.

    Leave the default `"__all__"` for `dataset_slug` to set an environment
    marker.
    """
    with honeycomb_client(configuration, secrets) as c:
        payload = {"message": message, "type": marker_type, "url": url}
        r = c.post(f"/1/markers/{dataset_slug}", json=payload)

        if r.status_code > 399:
            raise ActivityFailed(f"failed to create marker: {r.json()}")

        marker = cast(Dict[str, Any], r.json())
        logger.debug(f"Honeycomb marker: {marker}")

        return marker
