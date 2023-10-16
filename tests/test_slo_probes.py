# -*- coding: utf-8 -*-
import pytest

from httpx import Response

from chaoshoneycomb.slo.probes import get_slo, slo_has_enough_remaining_budget


@pytest.mark.respx(base_url="https://api.honeycomb.io")
def test_get_slo(respx_mock):
    route = respx_mock.get(
        "/1/slos/ds/slo1?detailed=true"
    ).mock(
        return_value=Response(200,
            json={
                "id": "slo1",
                "name": "My SLO",
                "description": "SLO to ensure requests succeed and are fast",
                "sli": {
                    "alias": "error_sli"
                },
                "time_period_days": 30,
                "target_per_million": 990000,
                "reset_at": "2022-011-11T09:53:04Z",
                "created_at": "2022-09-22T17:32:11Z",
                "updated_at": "2022-10-31T15:08:11Z",
                "compliance": 95.39,
                "budget_remaining": 7.73
            }
        )
    )

    s = get_slo(
        "ds",
        "slo1",
        True,
        {},
        {
            "api_key": "1235"
        }
    )

    assert route.called


@pytest.mark.respx(base_url="https://api.honeycomb.io")
def test_slo_has_enough_remaining_budget(respx_mock):
    route = respx_mock.get(
        "/1/slos/ds/slo1?detailed=true"
    ).mock(
        return_value=Response(200,
            json={
                "id": "slo1",
                "name": "My SLO",
                "description": "SLO to ensure requests succeed and are fast",
                "sli": {
                    "alias": "error_sli"
                },
                "time_period_days": 30,
                "target_per_million": 990000,
                "reset_at": "2022-011-11T09:53:04Z",
                "created_at": "2022-09-22T17:32:11Z",
                "updated_at": "2022-10-31T15:08:11Z",
                "compliance": 95.39,
                "budget_remaining": 7.73
            }
        )
    )

    s = slo_has_enough_remaining_budget(
        "ds",
        "slo1",
        3.4,
        {},
        {
            "api_key": "1235"
        }
    )

    assert s is True


@pytest.mark.respx(base_url="https://api.honeycomb.io")
def test_slo_has_not_enough_remaining_budget(respx_mock):
    route = respx_mock.get(
        "/1/slos/ds/slo1?detailed=true"
    ).mock(
        return_value=Response(200,
            json={
                "id": "slo1",
                "name": "My SLO",
                "description": "SLO to ensure requests succeed and are fast",
                "sli": {
                    "alias": "error_sli"
                },
                "time_period_days": 30,
                "target_per_million": 990000,
                "reset_at": "2022-011-11T09:53:04Z",
                "created_at": "2022-09-22T17:32:11Z",
                "updated_at": "2022-10-31T15:08:11Z",
                "compliance": 95.39,
                "budget_remaining": 7.73
            }
        )
    )

    s = slo_has_enough_remaining_budget(
        "ds",
        "slo1",
        8.4,
        {},
        {
            "api_key": "1235"
        }
    )

    assert s is False
