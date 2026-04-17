from __future__ import annotations
import requests
from typing import Any, Optional

class ODataQuery:
    def __init__(self, client: ODataClient, entity_set: str):
        self.client = client
        self.entity_set = entity_set
        self.params: dict[str, Any] = {'$format': 'json'}

    def top(self, n: int) -> ODataQuery:
        self.params['$top'] = n
        return self

    def skip(self, n: int) -> ODataQuery:
        self.params['$skip'] = n
        return self

    def select(self, fields: list[str]) -> ODataQuery:
        self.params['$select'] = ','.join(fields)
        return self

    def filter(self, expression: str) -> ODataQuery:
        self.params['$filter'] = expression
        return self

    def expand(self, navigation: str) -> ODataQuery:
        self.params['$expand'] = navigation
        return self

    def execute(self) -> list[dict[str, Any]]:
        return self.client._get(self.entity_set, params=self.params)

class ODataClient:
    """
    A lightweight OData client that mimics pyodata's fluent interface 
    but uses requests and is compatible with Oryonix constraints.
    """
    def __init__(self, service_url: str, api_key: Optional[str] = None):
        self.service_url = service_url.rstrip('/')
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if api_key:
            # We strictly use 'APIKey' as per SAP Sandbox documentation
            self.headers['APIKey'] = api_key

    def _get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        url = f"{self.service_url}/{path}"
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        
        if not response.ok:
            try:
                error_data = response.json()
                # Extract structured OData error messages
                error_obj = error_data.get('error', {})
                message = error_obj.get('message', {}).get('value', response.text)
            except Exception:
                message = response.text
            raise RuntimeError(f"OData Error ({response.status_code}): {message}")
            
        data = response.json()
        
        # OData V2 uses a 'd' wrapper, V4 uses 'value' for collections
        if 'd' in data:
            d = data['d']
            if isinstance(d, dict) and 'results' in d:
                return d['results']
            return d
        
        # OData V4 or simple V2 response
        if isinstance(data, dict) and 'value' in data:
            return data['value']
            
        return data

    @property
    def entity_sets(self):
        """Allows for fluent access like client.entity_sets.A_BusinessPartner"""
        class EntitySetProxy:
            def __init__(self, client: ODataClient):
                self.client = client
            def __getattr__(self, name: str) -> ODataQuery:
                return ODataQuery(self.client, name)
        return EntitySetProxy(self)
