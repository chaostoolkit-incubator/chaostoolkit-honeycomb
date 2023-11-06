# -*- coding: utf-8 -*-
import os
import sys

if sys.version_info < (3, 9):
    from typing import Generator
else:
    from collections.abc import Generator

from contextlib import contextmanager
from typing import List, cast

import httpx
from chaoslib.discovery.discover import (
    discover_actions,
    discover_probes,
    initialize_discovery_result,
)
from chaoslib.exceptions import ActivityFailed
from chaoslib.types import (
    Configuration,
    DiscoveredActivities,
    Discovery,
    Secrets,
)
from logzero import logger

__all__ = ["__version__", "discover"]
__version__ = "0.1.0"


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Honeycomb capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-grafana")

    discovery = initialize_discovery_result(
        "chaostoolkit-honeycomb", __version__, "honeycomb"
    )
    discovery["activities"].extend(load_exported_activities())

    return discovery


def get_api_key(secrets: Secrets) -> str:
    secrets = secrets or {}
    key = secrets.get("api_key", os.getenv("HONEYCOMB_API_KEY"))

    if not key:
        raise ActivityFailed("missing Honeycomb API key")

    return cast(str, key)


@contextmanager
def honeycomb_client(
    configuration: Configuration, secrets: Secrets
) -> Generator[httpx.Client, None, None]:
    h = {
        "X-Honeycomb-Team": get_api_key(secrets),
        "Accept": "application/json",
    }

    with httpx.Client(
        http2=True, headers=h, base_url="https://api.honeycomb.io"
    ) as c:
        yield c


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_probes("chaoshoneycomb.slo.probes"))
    activities.extend(discover_probes("chaoshoneycomb.trigger.probes"))
    activities.extend(discover_actions("chaoshoneycomb.marker.actions"))
    return activities
