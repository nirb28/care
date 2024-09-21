import requests
import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up the necessary scopes and credentials file path
SCOPES = ['https://www.googleapis.com/auth/sdm.service']
CREDENTIALS_FILE = 'credentials.json'


def get_access_token():
    creds = None
    if os.path.exists('credentials.json'):
        creds = Credentials.from_authorized_user_file('credentials.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds.token


def get_devices(project_id, access_token):
    url = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_camera_feed(project_id, device_id, access_token):
    url = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices/{device_id}:executeCommand"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "command": "sdm.devices.commands.CameraLiveStream.GenerateRtspStream"
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def main():
    project_id = "your_project_id"
    access_token = get_access_token()

    # Get list of devices
    devices = get_devices(project_id, access_token)
    print("Devices:", json.dumps(devices, indent=2))

    # Assuming the first device is a camera, get its ID
    if devices.get('devices'):
        device_id = devices['devices'][0]['name'].split('/')[-1]

        # Get camera feed
        camera_feed = get_camera_feed(project_id, device_id, access_token)
        print("Camera Feed:", json.dumps(camera_feed, indent=2))
    else:
        print("No devices found.")


if __name__ == "__main__":
    main()