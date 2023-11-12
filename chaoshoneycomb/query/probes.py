# -*- coding: utf-8 -*-
import time
from typing import Any, Dict, cast

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaoshoneycomb import honeycomb_client

__all__ = [
    "query_results",
    "result_data_must_be_lower_than",
    "result_data_must_be_greater_than",
]


def query_results(
    dataset_slug: str,
    query_result_id: str,
    timeout: int = 30,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Fetch the results of a query
    """
    with honeycomb_client(configuration, secrets) as c:
        start = time.time()
        while True:
            r = c.get(f"/1/query_results/{dataset_slug}/{query_result_id}")

            if r.status_code > 399:
                raise ActivityFailed(f"failed to get query result: {r.json()}")

            qr = cast(Dict[str, Any], r.json())

            if qr["complete"] is True:
                return qr

            time.sleep(1)

            if (start + timeout) > time.time():
                raise ActivityFailed("Failed to fetch query results in time")


def result_data_must_be_lower_than(
    dataset_slug: str,
    query_result_id: str,
    property_name: str,
    max_value: float,
    timeout: int = 30,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    r = query_results(
        dataset_slug, query_result_id, timeout, configuration, secrets
    )

    data = r["data"].get("results", [])
    for d in data:
        if property_name in d:
            return cast(bool, d[property_name] < max_value)

    raise ActivityFailed(f"Property {property_name} not part of query results")


def result_data_must_be_greater_than(
    dataset_slug: str,
    query_result_id: str,
    property_name: str,
    min_value: float,
    timeout: int = 30,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    r = query_results(
        dataset_slug, query_result_id, timeout, configuration, secrets
    )

    data = r["data"].get("results", [])
    for d in data:
        if property_name in d:
            return cast(bool, d[property_name] > min_value)

    raise ActivityFailed(f"Property {property_name} not part of query results")
