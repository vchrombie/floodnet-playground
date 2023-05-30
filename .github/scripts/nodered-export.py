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

print("Obtaining access token")
response = requests.post(
    f'{args.nodered_api_endpoint}/auth/token',
    data={
        'client_id': 'node-red-admin',
        'grant_type': 'password',
        'scope': 'read',
        'username': args.nodered_username,
        'password': args.nodered_password,
    },
)

if response.status_code == 200:
    print("Access token obtained successfully.", end='\n\n')
else:
    print("Failed to obtain access token.")
    response.raise_for_status()  # Raise an exception if the request failed

# Set up headers
access_token = response.json()['access_token']
headers = {'Authorization': f'Bearer {access_token}'}

print("exporting flows started")

flows_response = requests.get(f'{args.nodered_api_endpoint}/flows', headers=headers)
if flows_response.status_code == 200:
    print("fetching flows.json successful")
else:
    print("fetching flows.json failed")
    flows_response.raise_for_status()  # Raise an exception if the request failed

flows = flows_response.json()

with open(f'{args.git_src}/flows.json', 'w') as file:
    json.dump(flows, file, indent=2)

print("exported flows.json")

print("exporting flows completed", end='\n\n')

print("Revoking access token")
response = requests.post(f"{args.nodered_api_endpoint}/auth/revoke", headers=headers)
if response.status_code == 200:
    print("Access token revoked successfully.")
else:
    print("Failed to revoke access token.")
    response.raise_for_status()  # Raise an exception if the request failed
