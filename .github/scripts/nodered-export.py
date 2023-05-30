#!/usr/bin/env python3

import os
import argparse
import requests
import json

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--nodered-api-endpoint', default=os.getenv('NODERED_API_ENDPOINT'))
parser.add_argument('--nodered-username', default=os.getenv('NODERED_USERNAME'))
parser.add_argument('--nodered-password', default=os.getenv('NODERED_PASSWORD'))
parser.add_argument('--git-src', default=os.getenv('GIT_SRC'))
args = parser.parse_args()

print(f"Exporting Node-RED flows from {args.nodered_api_endpoint}")
print(f"Saving to {args.git_src}", end='\n\n')

# Obtain an access token
auth_response = requests.post(
    f'{args.nodered_api_endpoint}/auth/token',
    data={
        'client_id': 'node-red-admin',
        'grant_type': 'password',
        'scope': 'read',
        'username': args.nodered_username,
        'password': args.nodered_password,
    },
)
auth_response.raise_for_status()  # Raise an exception if the request failed
access_token = auth_response.json()['access_token']

# Use the access token to authenticate the next requests
headers = {'Authorization': f'Bearer {access_token}'}

print(f"exporting flows started")

# Retrieve the flows
flows_response = requests.get(f'{args.nodered_api_endpoint}/flows', headers=headers)
flows_response.raise_for_status()  # Raise an exception if the request failed
flows = flows_response.json()

# Save the flows to a JSON file
with open(f'{args.git_src}/flows.json', 'w') as file:
    json.dump(flows, file, indent=2)

print(f"exported flows.json")

print(f"exporting flows completed")

print(f"Revoking API token")
response = requests.post(f"{args.nodered_api_endpoint}/auth/revoke", headers=headers)
if response.status_code == 200:
    print(f"API token revoked successfully")
else:
    print(f"Failed to revoke API token")

