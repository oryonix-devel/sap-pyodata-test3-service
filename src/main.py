"""
SAP S/4HANA Cloud API_BUSINESS_PARTNER (A2X) via Pure Python (JSON).
Replaces pyodata with standard requests to ensure WASM/Oryonix compatibility.
"""

from __future__ import annotations

import logging
import onix
import requests

# We use standard json parsing, so no special logging level for pyodata needed
logger = logging.getLogger(__name__)

DEFAULT_SERVICE_URL = (
    "https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_BUSINESS_PARTNER"
)

@onix.compute
def fetch_business_partners(*, service_url: str, api_key: str, top: int):
    """
    Load Business Partner entities using raw REST/JSON.
    Avoids lxml/pyodata C-extension dependencies.
    """
    # 1. Target the specific EntitySet and force JSON response
    # OData uses $format=json or Accept headers
    url = f"{service_url}/A_BusinessPartner"
    params = {
        "$top": top,
        "$format": "json",
        "$select": "BusinessPartner,BusinessPartnerFullName"
    }
    
    headers = {
        "APIKey": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    # SAP OData V2 wraps results in d/results, V4 uses 'value'
    # The sandbox A_BusinessPartner is typically V2
    entries = data.get("d", {}).get("results", []) if "d" in data else data.get("value", [])
    
    rows: list[dict[str, str | None]] = []
    for entry in entries:
        rows.append({
            "BusinessPartner": str(entry.get("BusinessPartner")),
            "BusinessPartnerFullName": entry.get("BusinessPartnerFullName"),
        })
    return rows

@onix.flow
def list_business_partners(
    *,
    api_key: str,
    service_url: str | None = None,
    top: int = 5,
):
    url = service_url if service_url else DEFAULT_SERVICE_URL
    partners = fetch_business_partners(service_url=url, api_key=api_key, top=top)
    return {
        "service_url": url,
        "count": len(partners),
        "business_partners": partners,
    }

@onix.flow
def list_business_partners_safe(
    *,
    api_key: str,
    service_url: str | None = None,
    top: int = 5,
):
    url = service_url if service_url else DEFAULT_SERVICE_URL
    try:
        partners = fetch_business_partners(service_url=url, api_key=api_key, top=top)
        return {
            "ok": True,
            "service_url": url,
            "count": len(partners),
            "business_partners": partners,
            "error": None,
        }
    except Exception as e:
        return {
            "ok": False,
            "service_url": url,
            "count": 0,
            "business_partners": [],
            "error": {"type": type(e).__name__, "message": str(e)},
        }