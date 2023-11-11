# -*- coding: utf-8 -*-
import time
from typing import Any, Dict, cast

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaoshoneycomb import honeycomb_client

__all__ = ["query_results"]


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
