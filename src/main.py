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
        "description": "Access Business Partner master data from SAP S/4HANA Cloud.",
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
        "description": "Access Sales Order data from SAP S/4HANA Cloud.",
        "columns": [
            {"key": "SalesOrder", "label": "Sales Order"},
            {"key": "SalesOrderType", "label": "Type"},
        ],
        "mock_rows": [
            {"SalesOrder": "500001", "SalesOrderType": "OR"},
            {"SalesOrder": "500002", "SalesOrderType": "RE"},
        ],
    },
    "products": {
        "api_name": "products",
        "label": "Products",
        "technical_name": "API_PRODUCT_SRV",
        "entity_set": "A_Product",
        "service_url": "https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_PRODUCT_SRV",
        "default_top": 5,
        "description": "Access Product master data from SAP S/4HANA Cloud.",
        "columns": [
            {"key": "Product", "label": "Product"},
            {"key": "ProductType", "label": "Type"},
        ],
        "mock_rows": [
            {"Product": "Z-100", "ProductType": "FERT"},
            {"Product": "Z-200", "ProductType": "HAWA"},
        ],
    },
}


# -------------------------
# Helpers
# -------------------------

def _find_api_descriptor(*, api_name: str) -> dict[str, Any]:
    if api_name not in DEFAULT_API_REGISTRY:
        raise ValueError(f"Unknown API: {api_name}")
    return DEFAULT_API_REGISTRY[api_name]


def _extract_entries(*, payload: dict[str, Any]) -> list[dict[str, Any]]:
    # Handles SAP OData V2 + V4
    if "d" in payload:
        d = payload["d"]
        if isinstance(d, dict) and "results" in d:
            return d["results"]
        return [d]
    return payload.get("value", [])


# -------------------------
# Compute
# -------------------------

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
    service = (service_url or descriptor["service_url"]).rstrip("/")
    top = max(1, min(int(top), 100))

    # ✅ MOCK MODE
    if use_mock:
        rows = descriptor["mock_rows"][:top]
        return {
            "api_name": api_name,
            "label": descriptor["label"],
            "technical_name": descriptor["technical_name"],
            "entity_set": descriptor["entity_set"],
            "service_url": service,
            "rows": rows,
            "columns": descriptor["columns"],
            "count": len(rows),
            "source": "mock",
        }

    # ✅ REAL SAP CALL
    if not api_key:
        raise ValueError("api_key required when use_mock=false")

    # 🔥 Important: warm-up metadata call (SAP quirk)
    try:
        requests.get(
            f"{service}/$metadata",
            headers={
                "APIKey": api_key,
                "apikey": api_key,
                "Accept": "application/xml",
            },
            timeout=5,
        )
    except Exception:
        pass  # not fatal

    url = f"{service}/{descriptor['entity_set']}"

    res = requests.get(
        url,
        params={
            "$top": top,
            "$select": ",".join(c["key"] for c in descriptor["columns"]),
            "$format": "json",
        },
        headers={
            "APIKey": api_key,
            "apikey": api_key,
            "Accept": "application/json",
        },
        timeout=30,
    )

    if not res.ok:
        try:
            error_data = res.json()
            message = error_data.get("error", {}).get("message", {}).get("value", res.text)
        except Exception:
            message = res.text
        raise RuntimeError(f"SAP API Error ({res.status_code}): {message}")

    data = res.json()

    entries = _extract_entries(payload=data)

    rows = [
        {col["key"]: entry.get(col["key"]) for col in descriptor["columns"]}
        for entry in entries
    ]

    return {
        "api_name": api_name,
        "label": descriptor["label"],
        "technical_name": descriptor["technical_name"],
        "entity_set": descriptor["entity_set"],
        "service_url": service,
        "rows": rows,
        "columns": descriptor["columns"],
        "count": len(rows),
        "source": "sap",
    }


# -------------------------
# FLOWS
# -------------------------

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
    ).result()


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
        action_result = fetch_s4hana_api_rows(
            api_name=api_name,
            api_key=api_key,
            service_url=service_url,
            top=top,
            use_mock=use_mock,
        ).result()

        # Build response explicitly to avoid future-proxy issues
        return {
            "ok": True,
            "api_name": action_result.get("api_name"),
            "label": action_result.get("label"),
            "technical_name": action_result.get("technical_name"),
            "entity_set": action_result.get("entity_set"),
            "service_url": action_result.get("service_url"),
            "rows": action_result.get("rows", []),
            "columns": action_result.get("columns", []),
            "count": action_result.get("count", 0),
            "source": action_result.get("source"),
            "error": None,
        }
    except Exception as e:
        descriptor = DEFAULT_API_REGISTRY.get(api_name)

        return {
            "ok": False,
            "api_name": api_name,
            "source": "error",
            "columns": descriptor["columns"] if descriptor else [],
            "rows": [],
            "count": 0,
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "details": getattr(e, "message", None) if isinstance(e, RuntimeError) else None,
            },
        }


# -------------------------
# EXPORTS
# -------------------------

__all__ = [
    "list_s4hana_apis",
    "list_s4hana_api_rows",
    "list_s4hana_api_rows_safe",
]