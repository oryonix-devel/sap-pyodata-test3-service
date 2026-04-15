"""
SAP S/4HANA Cloud API_BUSINESS_PARTNER (A2X) via pyodata.

HTTP and OData client work run in compute (Temporal activity). The flow only
orchestrates and returns JSON-safe data. All flow/compute calls use keywords.
"""

from __future__ import annotations

import logging

import onix
import pyodata
import requests

logging.getLogger("pyodata").setLevel(logging.ERROR)

DEFAULT_SERVICE_URL = (
    "https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_BUSINESS_PARTNER"
)


@onix.compute
def fetch_business_partners(*, service_url: str, api_key: str, top: int):
    """
    Load Business Partner entities from SAP OData (mock/sandbox).
    Read-only: no idempotency key required for side effects.
    """
    session = requests.Session()
    session.headers.update({"APIKey": api_key})
    client = pyodata.Client(service_url, session)
    entities = client.entity_sets.A_BusinessPartner.get_entities().top(top).execute()
    rows: list[dict[str, str | None]] = []
    for entity in entities:
        rows.append(
            {
                "BusinessPartner": str(entity.BusinessPartner),
                "BusinessPartnerFullName": getattr(
                    entity, "BusinessPartnerFullName", None
                ),
            }
        )
    return rows


@onix.flow
def list_business_partners(
    *,
    api_key: str,
    service_url: str | None = None,
    top: int = 5,
):
    """
    Public API flow: returns a small page of Business Partners from SAP OData.
    """
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
    """
    Same as list_business_partners but catches errors and returns a structured body
    instead of failing the workflow (useful for sandbox connectivity checks).
    """
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
