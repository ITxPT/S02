import requests
import msal
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

BI_USERNAME = os.getenv("BI_USERNAME")
BI_PASSWORD = os.getenv("BI_PASSWORD")
BI_APP_ID = os.getenv("BI_APP_ID")
BI_APP_DIRECTORY_TENANT_ID = os.getenv("BI_APP_DIRECTORY_TENANT_ID")


def request_access_token(): # Generate Power BI Access Token
    authority_url = 'https://login.microsoftonline.com/' + str(BI_APP_DIRECTORY_TENANT_ID)
    scopes = ['https://analysis.windows.net/powerbi/api/.default']


    client = msal.PublicClientApplication(str(BI_APP_ID), authority=authority_url)
    token_response = client.acquire_token_by_username_password(username=str(BI_USERNAME), password=str(BI_PASSWORD), scopes=scopes)
    if not 'access_token' in token_response:
        raise Exception(token_response['error_description'])

    access_id = token_response.get('access_token')
    return access_id

""" # use this if you want to use a client secret (service principal) instead of a username and password
BI_APP_CLIENT_ID = os.getenv("BI_APP_CLIENT_ID")
BI_APP_CLIENT_SECRET = os.getenv("BI_APP_CLIENT_SECRET")
BI_APP_ID = os.getenv("BI_APP_ID")
BI_APP_DIRECTORY_TENANT_ID = os.getenv("BI_APP_DIRECTORY_TENANT_ID")

def request_access_token(): # Generate Power BI Access Token
    authority_url = 'https://login.microsoftonline.com/' + str(BI_APP_DIRECTORY_TENANT_ID)
    scopes = ['https://analysis.windows.net/powerbi/api/.default']

    client = msal.ConfidentialClientApplication(str(BI_APP_ID), authority=authority_url, client_credential=str(BI_APP_CLIENT_SECRET))
    token_response = client.acquire_token_for_client(scopes)
    if not 'access_token' in token_response:
        raise Exception(token_response['error_description'])

    access_id = token_response.get('access_token')
    print(f'Access token: {access_id}')
    return access_id
    """

def push_results_to_power_bi(verdict: int, BI_DATASET_ID: str):
    if not isinstance(verdict, int):
        raise TypeError("verdict must be an integer")
    access_id = request_access_token()

    # Step 2. Send results to Power BI
    table_name = 'RealTimeData'
    endpoint = f'https://api.powerbi.com/v1.0/myorg/datasets/{BI_DATASET_ID}/tables/{table_name}/rows'
    headers = {
        'Authorization': f'Bearer ' + access_id
    }

    data = {
      "rows": [
        {
          "Verdict": verdict
        }
      ]
    }

    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        print('Dataset updated successfully')
    else:
        print(response.reason)
        print(response.json())