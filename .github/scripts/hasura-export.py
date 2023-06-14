#!/usr/bin/env python3

import os
import argparse
import requests
import json

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--hasura-url', default=os.getenv('HASURA_URL'))
parser.add_argument('--hasura-admin-secret', default=os.getenv('HASURA_ADMIN_SECRET'))
parser.add_argument('--git-src', default=os.getenv('GIT_SRC'))
args = parser.parse_args()

# Set up headers
headers = {
    "X-Hasura-Admin-Secret": args.hasura_admin_secret,
    "Content-Type": "application/json",
}

print(f"Exporting Hasura metadata from {args.hasura_url}")
print(f"Saving to {args.git_src}", end='\n\n')

body = {
    "type": "export_metadata",
    "args": {}
}

metadata_response = requests.post(
    f"{args.hasura_url}/v1/query",
    headers=headers,
    data=json.dumps(body)
)

metadata_response.raise_for_status()

metadata = metadata_response.json()

with open(f"{args.git_src}/metadata.json", 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"Exported metadata to {args.git_src}/metadata.json")
