# -*- coding: utf-8 -*-
import time
from typing import Any, Dict, Optional, cast

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
    other_properties: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """
    Verifies the value for given property is lower than the given `max_value`.

    To select the most appropriate data, set `other_properties` to a set
    of properties and their values.
    """
    r = query_results(
        dataset_slug, query_result_id, timeout, configuration, secrets
    )

    is_match = False
    data = r["data"].get("results", [])
    for d in data:
        if property_name in d["data"]:
            if other_properties is not None:
                is_match = True
                for p, v in other_properties.items():
                    if not (p in d["data"] and d["data"][p] == v):
                        is_match = False
            else:
                is_match = True

            if is_match:
                return cast(bool, d[property_name] < max_value)

    raise ActivityFailed(f"Property {property_name} not part of query results")


def result_data_must_be_greater_than(
    dataset_slug: str,
    query_result_id: str,
    property_name: str,
    min_value: float,
    other_properties: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> bool:
    """
    Verifies the value for given property is higher than the given `min_value`.

    To select the most appropriate data, set `other_properties` to a set
    of properties and their values.
    """
    r = query_results(
        dataset_slug, query_result_id, timeout, configuration, secrets
    )

    is_match = False
    data = r["data"].get("results", [])
    for d in data:
        if property_name in d["data"]:
            if other_properties is not None:
                is_match = True
                for p, v in other_properties.items():
                    if not (p in d["data"] and d["data"][p] == v):
                        is_match = False
            else:
                is_match = True

            if is_match:
                return cast(bool, d[property_name] > min_value)

    raise ActivityFailed(f"Property {property_name} not part of query results")
