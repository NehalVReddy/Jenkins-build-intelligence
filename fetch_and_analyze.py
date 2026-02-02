import os
import sys
import requests
import json

JENKINS_URL = os.getenv("JENKINS_URL")
JOB_NAME = os.getenv("JOB_NAME")
USERNAME = os.getenv("USERNAME")
API_TOKEN = os.getenv("API_TOKEN")

if not JENKINS_URL or not JOB_NAME:
    print("❌ This container must be run from Jenkins.")
    print("❌ Docker Desktop execution is not supported.")
    sys.exit(1)

API_URL = f"{JENKINS_URL}/job/{JOB_NAME}/api/json?tree=builds[number,result,timestamp,duration,url]{{0,5}}"

response = requests.get(API_URL, auth=(USERNAME, API_TOKEN))
response.raise_for_status()

with open("/output/last5_builds.json", "w") as f:
    json.dump(response.json(), f, indent=4)

print("✅ Build Intelligence Generated Successfully")
