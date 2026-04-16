from __future__ import annotations

import copy
import logging
from typing import Any

import requests

try:
    import fc as _platform
except ImportError:  # pragma: no cover
    import onix as _platform  # type: ignore

flow = _platform.flow
compute = getattr(_platform, "compute", getattr(_platform, "action"))

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
        "description": "Business partner master data used for customers, suppliers, and general partner lookups.",
        "columns": [
            {"key": "BusinessPartner", "label": "Business Partner"},
            {"key": "BusinessPartnerFullName", "label": "Full Name"},
            {"key": "BusinessPartnerCategory", "label": "Category"},
            {"key": "Country", "label": "Country"},
        ],
        "mock_rows": [
            {
                "BusinessPartner": "1000001",
                "BusinessPartnerFullName": "Acme Corporation",
                "BusinessPartnerCategory": "2",
                "Country": "US",
            },
            {
                "BusinessPartner": "1000002",
                "BusinessPartnerFullName": "Northwind Traders",
                "BusinessPartnerCategory": "2",
                "Country": "DE",
            },
            {
                "BusinessPartner": "1000003",
                "BusinessPartnerFullName": "Globex Supply",
                "BusinessPartnerCategory": "1",
                "Country": "GB",
            },
            {
                "BusinessPartner": "1000004",
                "BusinessPartnerFullName": "Blue Ocean Imports",
                "BusinessPartnerCategory": "2",
                "Country": "IN",
            },
            {
                "BusinessPartner": "1000005",
                "BusinessPartnerFullName": "Vertex Manufacturing",
                "BusinessPartnerCategory": "2",
                "Country": "SG",
            },
        ],
    },
    "sales_orders": {
        "api_name": "sales_orders",
        "label": "Sales Orders",
        "technical_name": "API_SALES_ORDER_SRV",
        "entity_set": "A_SalesOrder",
        "service_url": "https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_SALES_ORDER_SRV",
        "default_top": 5,
        "description": "Sales order header data for order monitoring and downstream process demos.",
        "columns": [
            {"key": "SalesOrder", "label": "Sales Order"},
            {"key": "SalesOrderType", "label": "Order Type"},
            {"key": "SoldToParty", "label": "Sold-To Party"},
            {"key": "OverallSDDocumentStatus", "label": "Status"},
        ],
        "mock_rows": [
            {
                "SalesOrder": "500000001",
                "SalesOrderType": "OR",
                "SoldToParty": "1000001",
                "OverallSDDocumentStatus": "C",
            },
            {
                "SalesOrder": "500000002",
                "SalesOrderType": "OR",
                "SoldToParty": "1000002",
                "OverallSDDocumentStatus": "B",
            },
            {
                "SalesOrder": "500000003",
                "SalesOrderType": "CR",
                "SoldToParty": "1000003",
                "OverallSDDocumentStatus": "A",
            },
            {
                "SalesOrder": "500000004",
                "SalesOrderType": "OR",
                "SoldToParty": "1000004",
                "OverallSDDocumentStatus": "C",
            },
            {
                "SalesOrder": "500000005",
                "SalesOrderType": "OR",
                "SoldToParty": "1000005",
                "OverallSDDocumentStatus": "B",
            },
        ],
    },
    "products": {
        "api_name": "products",
        "label": "Products",
        "technical_name": "API_PRODUCT_SRV",
        "entity_set": "A_Product",
        "service_url": "https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_PRODUCT_SRV",
        "default_top": 5,
        "description": "Material and product master data for catalog, pricing, and planning demos.",
        "columns": [
            {"key": "Product", "label": "Product"},
            {"key": "ProductType", "label": "Product Type"},
            {"key": "BaseUnit", "label": "Base Unit"},
            {"key": "ProductGroup", "label": "Product Group"},
        ],
        "mock_rows": [
            {
                "Product": "TG11",
                "ProductType": "FERT",
                "BaseUnit": "EA",
                "ProductGroup": "L001",
            },
            {
                "Product": "TG12",
                "ProductType": "FERT",
                "BaseUnit": "EA",
                "ProductGroup": "L002",
            },
            {
                "Product": "TG13",
                "ProductType": "HALB",
                "BaseUnit": "EA",
                "ProductGroup": "L001",
            },
            {
                "Product": "TG14",
                "ProductType": "ROH",
                "BaseUnit": "KG",
                "ProductGroup": "R010",
            },
            {
                "Product": "TG15",
                "ProductType": "FERT",
                "BaseUnit": "EA",
                "ProductGroup": "L003",
            },
        ],
    },
    "purchase_orders": {
        "api_name": "purchase_orders",
        "label": "Purchase Orders",
        "technical_name": "API_PURCHASEORDER_PROCESS_SRV",
        "entity_set": "A_PurchaseOrder",
        "service_url": "https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV",
        "default_top": 5,
        "description": "Purchase order headers for procurement and supplier demos.",
        "columns": [
            {"key": "PurchaseOrder", "label": "Purchase Order"},
            {"key": "CompanyCode", "label": "Company Code"},
            {"key": "PurchasingOrganization", "label": "Purchasing Org"},
            {"key": "Supplier", "label": "Supplier"},
        ],
        "mock_rows": [
            {
                "PurchaseOrder": "4500000010",
                "CompanyCode": "1710",
                "PurchasingOrganization": "1710",
                "Supplier": "1000001",
            },
            {
                "PurchaseOrder": "4500000011",
                "CompanyCode": "1710",
                "PurchasingOrganization": "1710",
                "Supplier": "1000002",
            },
            {
                "PurchaseOrder": "4500000012",
                "CompanyCode": "1710",
                "PurchasingOrganization": "1710",
                "Supplier": "1000003",
            },
            {
                "PurchaseOrder": "4500000013",
                "CompanyCode": "1710",
                "PurchasingOrganization": "1710",
                "Supplier": "1000004",
            },
            {
                "PurchaseOrder": "4500000014",
                "CompanyCode": "1710",
                "PurchasingOrganization": "1710",
                "Supplier": "1000005",
            },
        ],
    },
}


def _clone_rows(*, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def _normalize_service_url(*, service_url: str | None, default_service_url: str) -> str:
    chosen = service_url.strip() if isinstance(service_url, str) else ""
    base = chosen if chosen else default_service_url
    return base.rstrip("/")


def _coerce_top(*, top: int | None, default_top: int) -> int:
    value = default_top if top is None else top
    try:
        parsed = int(value)
    except Exception:
        parsed = default_top
    return max(1, min(parsed, 100))


def _extract_entries(*, payload: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(payload.get("d"), dict):
        results = payload["d"].get("results", [])
        return results if isinstance(results, list) else []
    results = payload.get("value", [])
    return results if isinstance(results, list) else []


def _find_api_descriptor(*, api_name: str) -> dict[str, Any]:
    descriptor = DEFAULT_API_REGISTRY.get(api_name)
    if descriptor is None:
        raise KeyError(f"Unknown SAP API '{api_name}'")
    return descriptor


@compute
def fetch_s4hana_api_rows(
    *,
    api_name: str,
    api_key: str,
    service_url: str | None,
    top: int | None,
    use_mock: bool,
) -> dict[str, Any]:
    descriptor = _find_api_descriptor(api_name=api_name)
    effective_top = _coerce_top(top=top, default_top=descriptor["default_top"])
    effective_service_url = _normalize_service_url(
        service_url=service_url,
        default_service_url=descriptor["service_url"],
    )

    if use_mock:
        rows = _clone_rows(rows=descriptor["mock_rows"][:effective_top])
        return {
            "api_name": descriptor["api_name"],
            "label": descriptor["label"],
            "technical_name": descriptor["technical_name"],
            "entity_set": descriptor["entity_set"],
            "service_url": effective_service_url,
            "source": "mock",
            "count": len(rows),
            "columns": descriptor["columns"],
            "rows": rows,
        }

    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("api_key is required when use_mock is false")

    request_url = f"{effective_service_url}/{descriptor['entity_set']}"
    params = {
        "$top": effective_top,
        "$format": "json",
        "$select": ",".join(column["key"] for column in descriptor["columns"]),
    }
    headers = {
        "APIKey": api_key.strip(),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.get(request_url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    payload = response.json()
    entries = _extract_entries(payload=payload)

    rows: list[dict[str, Any]] = []
    for entry in entries[:effective_top]:
        row: dict[str, Any] = {}
        for column in descriptor["columns"]:
            key = column["key"]
            row[key] = entry.get(key)
        rows.append(row)

    return {
        "api_name": descriptor["api_name"],
        "label": descriptor["label"],
        "technical_name": descriptor["technical_name"],
        "entity_set": descriptor["entity_set"],
        "service_url": effective_service_url,
        "source": "sap",
        "count": len(rows),
        "columns": descriptor["columns"],
        "rows": rows,
    }


@flow
def list_s4hana_apis(*, api_key: str | None = None) -> dict[str, Any]:
    available_apis: list[dict[str, Any]] = []
    for api_name in DEFAULT_API_REGISTRY:
        descriptor = DEFAULT_API_REGISTRY[api_name]
        available_apis.append(
            {
                "api_name": descriptor["api_name"],
                "label": descriptor["label"],
                "technical_name": descriptor["technical_name"],
                "entity_set": descriptor["entity_set"],
                "service_url": descriptor["service_url"],
                "default_top": descriptor["default_top"],
                "description": descriptor["description"],
                "columns": descriptor["columns"],
            }
        )

    return {
        "default_api_name": DEFAULT_API_NAME,
        "available_apis": available_apis,
    }


@flow
def list_s4hana_api_rows(
    *,
    api_name: str,
    api_key: str,
    service_url: str | None = None,
    top: int | None = 5,
    use_mock: bool = True,
) -> dict[str, Any]:
    return fetch_s4hana_api_rows(
        api_name=api_name,
        api_key=api_key,
        service_url=service_url,
        top=top,
        use_mock=use_mock,
    )


@flow
def list_s4hana_api_rows_safe(
    *,
    api_name: str,
    api_key: str,
    service_url: str | None = None,
    top: int | None = 5,
    use_mock: bool = True,
) -> dict[str, Any]:
    try:
        result = fetch_s4hana_api_rows(
            api_name=api_name,
            api_key=api_key,
            service_url=service_url,
            top=top,
            use_mock=use_mock,
        )
        return {
            "ok": True,
            **result,
            "error": None,
        }
    except Exception as exc:
        descriptor = DEFAULT_API_REGISTRY.get(api_name)
        return {
            "ok": False,
            "api_name": api_name,
            "label": descriptor["label"] if descriptor else api_name,
            "technical_name": descriptor["technical_name"] if descriptor else "",
            "entity_set": descriptor["entity_set"] if descriptor else "",
            "service_url": _normalize_service_url(
                service_url=service_url,
                default_service_url=descriptor["service_url"] if descriptor else "",
            )
            if descriptor
            else "",
            "source": "mock" if use_mock else "sap",
            "count": 0,
            "columns": descriptor["columns"] if descriptor else [],
            "rows": [],
            "error": {
                "type": type(exc).__name__,
                "message": str(exc),
            },
        }