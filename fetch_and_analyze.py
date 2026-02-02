import os
import requests
import sys

JENKINS_URL = os.getenv("JENKINS_URL")
JOB_NAME = os.getenv("JOB_NAME")
USERNAME = os.getenv("USERNAME")
API_TOKEN = os.getenv("API_TOKEN")

if not all([JENKINS_URL, JOB_NAME, USERNAME, API_TOKEN]):
    print("ERROR: Missing required environment variables.")
    print("This container must be run from Jenkins, not Docker Desktop.")
    sys.exit(1)

API_URL = f"{JENKINS_URL}/job/{JOB_NAME}/api/json?tree=builds[number,result,timestamp,duration,url]{{0,5}}"

response = requests.get(API_URL, auth=(USERNAME, API_TOKEN))
response.raise_for_status()

data = response.json()

with open("/output/last5_builds.json", "w") as f:
    import json
    json.dump(data, f, indent=4)

print("Build Intelligence Generated Successfully")
