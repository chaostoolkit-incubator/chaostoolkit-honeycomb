# -*- coding: utf-8 -*-
from typing import List

from chaoslib.discovery.discover import (
    discover_probes,
    initialize_discovery_result,
)
from chaoslib.types import DiscoveredActivities, Discovery
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
    return


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(
        discover_probes("chaoshoneycomb.slo.probes"),
    )
    return activities
