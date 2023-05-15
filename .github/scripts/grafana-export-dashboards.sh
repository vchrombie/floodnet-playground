#!/bin/bash

# Exit script on error, pipefail or unset variable
set -o errexit
set -o pipefail
set -o nounset

# Set up headers and input path
headers="Authorization: Bearer $GRAFANA_API_KEY"
in_path="$GIT_SRC/dashboards_raw"

echo "Exporting Grafana dashboards from $GRAFANA_URL"

# Create the input directory if it doesn't exist
mkdir -p $in_path

# Get all dashboards from Grafana and write to temporary file
curl -H "$headers" -s "$GRAFANA_URL/api/search?query=&" > tmp.json

# Loop over each dashboard
for dash in $(curl -H "$headers" -s "$GRAFANA_URL/api/search?query=&" | jq -r '.[] | try select(.type == "dash-db") catch false | .uid'); do
    # Define the path for the dashboard json
    dash_path="$in_path/$dash.json"

    # Get the dashboard details and write to file
    curl -H "$headers" -s "$GRAFANA_URL/api/dashboards/uid/$dash" | jq -r . > $dash_path
    jq -r .dashboard $dash_path > $in_path/dashboard.json
    title=$(jq -r .dashboard.title $dash_path | sed "s/\//-/g")
    folder="$(jq -r '.meta.folderTitle' $dash_path | sed "s/\//-/g")"

    # Create the destination directory if it doesn't exist
    mkdir -p "$GIT_SRC/$folder"

    # Move the dashboard json to the destination directory
    mv -f $in_path/dashboard.json "$GIT_SRC/$folder/${title}.json"
    echo "exported $GIT_SRC/$folder/${title}.json"
done

# Remove the input directory
rm -r $in_path
