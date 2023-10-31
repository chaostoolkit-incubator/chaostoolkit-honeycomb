# -*- coding: utf-8 -*-
from typing import Any, Dict, cast

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaoshoneycomb import honeycomb_client

__all__ = ["get_trigger", "trigger_is_unresolved", "trigger_is_resolved"]


def get_trigger(
    dataset_slug: str,
    trigger_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    with honeycomb_client(configuration, secrets) as c:
        r = c.get(f"/1/triggers/{dataset_slug}/{trigger_id}")

        if r.status_code > 399:
            raise ActivityFailed(f"failed to retrieve SLO: {r.json()}")

        trigger = cast(Dict[str, Any], r.json())
        logger.debug(f"Honeycomb trigger: {trigger}")
        return trigger


def trigger_is_unresolved(
    dataset_slug: str,
    trigger_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """
    Checks that the trigger is in unresolved ("triggered") state.
    """
    trigger = get_trigger(dataset_slug, trigger_id, configuration, secrets)
    return trigger["triggered"] is True


def trigger_is_resolved(
    dataset_slug: str,
    trigger_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """
    Checks that the trigger is in resolved (not "triggered") state.
    """
    trigger = get_trigger(dataset_slug, trigger_id, configuration, secrets)
    return trigger["triggered"] is False
