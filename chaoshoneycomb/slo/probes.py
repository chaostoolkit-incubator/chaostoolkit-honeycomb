# -*- coding: utf-8 -*-
from typing import Any, Dict, cast

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaoshoneycomb import honeycomb_client

__all__ = [
    "get_slo",
    "slo_has_enough_remaining_budget",
    "list_burn_alerts",
    "has_budget_decreased_by",
    "is_error_budget_exhausted_in",
]


def get_slo(
    dataset_slug: str,
    slo_id: str,
    detailed: bool = True,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    params = {"detailed": detailed}

    with honeycomb_client(configuration, secrets) as c:
        r = c.get(f"/1/slos/{dataset_slug}/{slo_id}", params=params)

        if r.status_code > 399:
            raise ActivityFailed(f"failed to retrieve SLO: {r.json()}")

        return cast(Dict[str, Any], r.json())


def slo_has_enough_remaining_budget(
    dataset_slug: str,
    slo_id: str,
    min_budget: float = 1.0,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    slo = get_slo(dataset_slug, slo_id, True, configuration, secrets)
    return cast(float, slo["budget_remaining"]) >= min_budget


def list_burn_alerts(
    dataset_slug: str,
    slo_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    params = {"slo_id": slo_id}

    with honeycomb_client(configuration, secrets) as c:
        r = c.get(f"/1/burn_alerts/{dataset_slug}", params=params)

        if r.status_code > 399:
            raise ActivityFailed(f"failed to retrieve burn alerts: {r.json()}")

        return cast(Dict[str, Any], r.json())


def has_budget_decreased_by(
    dataset_slug: str,
    slo_id: str,
    amount: float = 25.0,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """
    Has one of the burn rate of a SLO dropped suddenly.

    The `amount` is the percentage of drop during the window of the burn
    alert.
    """
    alerts = list_burn_alerts(dataset_slug, slo_id, configuration, secrets)
    if not alerts:
        logger.debug(f"No burn alerts found for SLO {slo_id}")
        return False

    for alert in alerts:
        if alert["alert_type"] == "budget_rate":  # type: ignore
            logger.debug(f"Checking burn alert {alert}")
            value = float(alert["budget_rate_decrease_threshold_per_million"])  # type: ignore  # noqa
            if (value / 10000.0) >= amount:
                return True

    return False


def is_error_budget_exhausted_in(
    dataset_slug: str,
    slo_id: str,
    minutes: int = 60,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """
    Will the error budget be exhausted within the next amount of `minutes`?
    """
    alerts = list_burn_alerts(dataset_slug, slo_id, configuration, secrets)
    if not alerts:
        logger.debug(f"No burn alerts found for SLO {slo_id}")
        return False

    for alert in alerts:
        if alert["alert_type"] == "exhaustion_time":  # type: ignore
            logger.debug(f"Checking burn alert {alert}")
            if alert["exhaustion_minutes"] <= minutes:  # type: ignore
                return True

    return False
