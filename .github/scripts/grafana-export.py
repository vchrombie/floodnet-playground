#!/usr/bin/env python3

import os
import argparse
import requests
import json

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--grafana-api-key', default=os.getenv('GRAFANA_API_KEY'))
parser.add_argument('--grafana-url', default=os.getenv('GRAFANA_URL'))
parser.add_argument('--git-src', default=os.getenv('GIT_SRC'))
args = parser.parse_args()

# Set up headers
headers = {"Authorization": f"Bearer {args.grafana_api_key}", "Content-type": "application/json"}

print(f"Exporting Grafana dashboards and alerts from {args.grafana_url}")
print(f"Saving to {args.git_src}", end='\n\n')

# Define dashboard & alerts paths
dashboards_path = f"{args.git_src}/dashboards"
alerts_path = f"{args.git_src}/alerts"

os.makedirs(dashboards_path, exist_ok=True)
os.makedirs(alerts_path, exist_ok=True)

print("exporting dashboards started")

response = requests.get(f"{args.grafana_url}/api/search?query=&", headers=headers)
dashboards = response.json()

for dash in dashboards:
    if dash.get('type') == 'dash-db':
        dash_uid = dash.get('uid')

        response = requests.get(f"{args.grafana_url}/api/dashboards/uid/{dash_uid}", headers=headers)
        dashboard_details = response.json()

        title = dashboard_details['dashboard']['title'].replace('/', '-')
        folder = dashboard_details['meta']['folderTitle'].replace('/', '-')

        os.makedirs(f"{dashboards_path}/{folder}", exist_ok=True)

        with open(f"{dashboards_path}/{folder}/{dash_uid}.json", 'w') as f:
            json.dump(dashboard_details, f, indent=2)

        print(f"exported `{title}` to {dashboards_path}/{folder}/{dash_uid}.json")

print("exporting dashboards completed", end='\n\n')

print("exporting alerts started")

response = requests.get(f"{args.grafana_url}/api/ruler/grafana/api/v1/rules", headers=headers)
alerts = response.json()

with open(f"{alerts_path}/alerts.json", 'w') as f:
    json.dump(alerts, f, indent=2)

print(f"exported {alerts_path}/alerts.json")

print("exporting alerts completed")
