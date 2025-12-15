from google.oauth2 import service_account
import google.auth.transport.requests
import requests

SCOPES = ["https://www.googleapis.com/auth/chat.bot"]
SERVICE_ACCOUNT_FILE = "/home/kim/app/airflow/keys/application_default_credentials.json      "

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
token = credentials.token

url = "https://chat.googleapis.com/v1/spaces/SPACE_ID/messages"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
data = {"text": "테스트 메시지"}
requests.post(url, headers=headers, json=data)