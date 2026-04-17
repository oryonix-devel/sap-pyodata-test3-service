import requests
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

API_KEY = 'HibHlLvSlHEAjBWRHKAmmUGs5Ns4SFDG'
SERVICE_URL = 'https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_BUSINESS_PARTNER'


def test_sap_connection():
    session = requests.Session()
    session.headers.update({
        'APIKey': API_KEY
    })

    print(f"Connecting to {SERVICE_URL}...")

    try:
        # 1. Fetch metadata (like pyodata does)
        metadata_url = f"{SERVICE_URL}/$metadata"
        metadata_headers = {
            'Accept': 'application/xml'
        }

        print("Fetching metadata...")
        meta_resp = session.get(metadata_url, headers=metadata_headers, timeout=10)

        if not meta_resp.ok:
            print(f"Metadata fetch failed: {meta_resp.status_code}")
            print(meta_resp.text)
            return

        print("Metadata fetched successfully.")

        # 2. Fetch Business Partners (same as pyodata query)
        data_url = f"{SERVICE_URL}/A_BusinessPartner"
        params = {
            '$top': 5,
            '$format': 'json'
        }

        data_headers = {
            'Accept': 'application/json'
        }

        print("Fetching data...")
        data_resp = session.get(data_url, headers=data_headers, params=params, timeout=10)

        if not data_resp.ok:
            print(f"Data fetch failed: {data_resp.status_code}")
            print(data_resp.text)
            return

        data = data_resp.json()

        # 3. Parse OData response
        # SAP OData typically wraps results like: {'d': {'results': [...]}}
        results = data.get('d', {}).get('results', [])

        for partner in results:
            bp_id = partner.get('BusinessPartner')
            name = partner.get('BusinessPartnerFullName')
            print(f"ID: {bp_id} | Name: {name}")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    test_sap_connection()