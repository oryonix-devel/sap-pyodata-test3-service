from __future__ import annotations

import logging
from typing import Any

import onix
from odata import ODataClient

logger = logging.getLogger(__name__)

DEFAULT_API_NAME = "business_partners"

# Pure metadata registry - NO MOCK DATA
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
            {"key": "BusinessPartnerCategory", "label": "Category"},
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
            {"key": "SoldToParty", "label": "Sold-To Party"},
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
            {"key": "BaseUnit", "label": "Unit"},
        ],
    },
    "purchase_orders": {
        "api_name": "purchase_orders",
        "label": "Purchase Orders",
        "technical_name": "API_PURCHASEORDER_PROCESS_SRV",
        "entity_set": "A_PurchaseOrder",
        "service_url": "https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV",
        "default_top": 5,
        "description": "Access Purchase Order headers from SAP S/4HANA Cloud.",
        "columns": [
            {"key": "PurchaseOrder", "label": "Purchase Order"},
            {"key": "CompanyCode", "label": "Company Code"},
            {"key": "PurchasingOrganization", "label": "Purchasing Org"},
            {"key": "Supplier", "label": "Supplier"},
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


# -------------------------
# Actions (Focused I/O)
# -------------------------

@onix.action
def execute_sap_odata_read(
    *,
    service_url: str,
    api_key: str,
    entity_set_name: str,
    select_fields: list[str],
    top: int,
) -> list[dict[str, Any]]:
    """
    Focused action for executing a read-only OData query across the network.
    Following Oryonix best practices, this action is strictly for side-effects (I/O).
    """
    client = ODataClient(service_url=service_url, api_key=api_key)
    
    # Execute network call via the OData client
    return (
        client.entity_sets.__getattr__(entity_set_name)
        .select(fields=select_fields)
        .top(n=top)
        .execute()
    )


# -------------------------
# Logic Helpers (Regular Python Functions)
# -------------------------

def _process_odata_rows(*, entries: list[dict[str, Any]], columns: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Pure-Python logic for transforming OData entries into clean rows."""
    return [
        {col["key"]: entry.get(col["key"]) for col in columns}
        for entry in entries
    ]


# -------------------------
# Flows (Orchestration)
# -------------------------

@onix.flow
def list_s4hana_apis() -> dict[str, Any]:
    """Lists all available SAP API descriptors. Serves as a public API entrypoint flow."""
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
) -> dict[str, Any]:
    """
    Orchestrates the metadata lookup and OData execution.
    Complies with Oryonix durability by calling actions for side effects.
    """
    descriptor = _find_api_descriptor(api_name=api_name)
    service = (service_url or descriptor["service_url"]).rstrip("/")
    limit = max(1, min(int(top), 100))

    if not api_key:
        raise ValueError("SAP API Key is required for real-time access.")

    # Call the focused I/O action
    entries = execute_sap_odata_read(
        service_url=service,
        api_key=api_key,
        entity_set_name=descriptor["entity_set"],
        select_fields=[c["key"] for c in descriptor["columns"]],
        top=limit,
    ).result()

    # Apply deterministic transformation logic
    rows = _process_odata_rows(entries=entries, columns=descriptor["columns"])

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


@onix.flow
def list_s4hana_api_rows_safe(
    *,
    api_name: str,
    api_key: str,
    service_url: str | None = None,
    top: int = 5,
) -> dict[str, Any]:
    """Safe wrapper flow (endpoint) that returns structured errors instead of raising."""
    try:
        # Reusing the existing flow orchestration
        result = list_s4hana_api_rows(
            api_name=api_name,
            api_key=api_key,
            service_url=service_url,
            top=top,
        ).result()
        result["ok"] = True
        result["error"] = None
        return result
    except Exception as e:
        descriptor = DEFAULT_API_REGISTRY.get(api_name)
        return {
            "ok": False,
            "api_name": api_name,
            "label": descriptor["label"] if descriptor else api_name,
            "technical_name": descriptor["technical_name"] if descriptor else "Unknown",
            "entity_set": descriptor["entity_set"] if descriptor else "Unknown",
            "service_url": descriptor["service_url"] if descriptor else service_url,
            "source": "error",
            "columns": descriptor["columns"] if descriptor else [],
            "rows": [],
            "count": 0,
            "error": {
                "type": type(e).__name__,
                "message": str(e),
            },
        }


# -------------------------
# Exports
# -------------------------

__all__ = [
    "list_s4hana_apis",
    "list_s4hana_api_rows",
    "list_s4hana_api_rows_safe",
]