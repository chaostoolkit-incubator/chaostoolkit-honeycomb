# -*- coding: utf-8 -*-
from typing import Any, Dict, cast

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaoshoneycomb import honeycomb_client

__all__ = ["get_slo", "slo_has_enough_remaining_budget"]


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
