from __future__ import annotations

import logging
from typing import Any

import requests
import onix

logger = logging.getLogger(__name__)

DEFAULT_API_NAME = "business_partners"

DEFAULT_API_REGISTRY: dict[str, dict[str, Any]] = {
    "business_partners": {
        "api_name": "business_partners",
        "label": "Business Partners",
        "technical_name": "API_BUSINESS_PARTNER",
        "entity_set": "A_BusinessPartner",
        "service_url": "https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_BUSINESS_PARTNER",
        "default_top": 5,
        "columns": [
            {"key": "BusinessPartner", "label": "Business Partner"},
            {"key": "BusinessPartnerFullName", "label": "Full Name"},
        ],
        "mock_rows": [
            {"BusinessPartner": "1000001", "BusinessPartnerFullName": "Acme Corp"},
            {"BusinessPartner": "1000002", "BusinessPartnerFullName": "Northwind"},
        ],
    },
    "sales_orders": {
        "api_name": "sales_orders",
        "label": "Sales Orders",
        "technical_name": "API_SALES_ORDER_SRV",
        "entity_set": "A_SalesOrder",
        "service_url": "https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_SALES_ORDER_SRV",
        "default_top": 5,
        "columns": [
            {"key": "SalesOrder", "label": "Sales Order"},
            {"key": "SalesOrderType", "label": "Type"},
        ],
        "mock_rows": [
            {"SalesOrder": "500001", "SalesOrderType": "OR"},
            {"SalesOrder": "500002", "SalesOrderType": "RE"},
        ],
    },
}


def _find_api_descriptor(*, api_name: str) -> dict[str, Any]:
    if api_name not in DEFAULT_API_REGISTRY:
        raise ValueError(f"Unknown API: {api_name}")
    return DEFAULT_API_REGISTRY[api_name]


@onix.action
def fetch_s4hana_api_rows(
    *,
    api_name: str,
    api_key: str,
    service_url: str | None,
    top: int,
    use_mock: bool,
) -> dict[str, Any]:

    descriptor = _find_api_descriptor(api_name=api_name)
    service = service_url or descriptor["service_url"]

    if use_mock:
        rows = descriptor["mock_rows"][:top]
        return {
            "api_name": api_name,
            "rows": rows,
            "columns": descriptor["columns"],
            "count": len(rows),
            "source": "mock",
        }

    if not api_key:
        raise ValueError("api_key required")

    url = f"{service}/{descriptor['entity_set']}"

    res = requests.get(
        url,
        params={
            "$top": top,
            "$format": "json",
            "$select": ",".join(c["key"] for c in descriptor["columns"]),
        },
        headers={"APIKey": api_key},
    )

    res.raise_for_status()
    data = res.json()

    entries = data.get("d", {}).get("results", [])

    rows = [
        {col["key"]: e.get(col["key"]) for col in descriptor["columns"]}
        for e in entries
    ]

    return {
        "api_name": api_name,
        "rows": rows,
        "columns": descriptor["columns"],
        "count": len(rows),
        "source": "sap",
    }


# ======================
# FLOWS (your requirement)
# ======================

@onix.flow
def list_s4hana_apis(*, api_key: str | None = None):
    return {
        "default_api_name": DEFAULT_API_NAME,
        "available_apis": list(DEFAULT_API_REGISTRY.values()),
    }


@onix.flow
def list_s4hana_api_rows(
    *,
    api_name: str,
    api_key: str,
    service_url: str | None = None,
    top: int = 5,
    use_mock: bool = True,
):
    return fetch_s4hana_api_rows(
        api_name=api_name,
        api_key=api_key,
        service_url=service_url,
        top=top,
        use_mock=use_mock,
    )


@onix.flow
def list_s4hana_api_rows_safe(
    *,
    api_name: str,
    api_key: str,
    service_url: str | None = None,
    top: int = 5,
    use_mock: bool = True,
):
    try:
        result = fetch_s4hana_api_rows(
            api_name=api_name,
            api_key=api_key,
            service_url=service_url,
            top=top,
            use_mock=use_mock,
        )
        return {"ok": True, **result, "error": None}
    except Exception as e:
        return {"ok": False, "rows": [], "count": 0, "error": str(e)}


# ======================
# 🔥 CRITICAL EXPORT FIX
# ======================

__all__ = [
    "list_s4hana_apis",
    "list_s4hana_api_rows",
    "list_s4hana_api_rows_safe",
]