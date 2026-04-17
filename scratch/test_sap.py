import requests
import logging

# Set up logging to see details
logging.basicConfig(level=logging.DEBUG)

API_KEY = 'HibHlLvSlHEAjBWRHKAmmUGs5Ns4SFDG'
SERVICE_URL = 'https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_BUSINESS_PARTNER'

def test_raw_requests():
    print("--- Testing with raw requests ---")
    headers = {
        'APIKey': API_KEY,
        'Accept': 'application/json'
    }
    url = f"{SERVICE_URL}/A_BusinessPartner"
    params = {'$top': 1, '$format': 'json'}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        if response.ok:
            print("Success!")
            # print(response.json())
        else:
            print(f"Failed: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_raw_requests()
