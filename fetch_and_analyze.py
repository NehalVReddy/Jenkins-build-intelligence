import os
import json
import requests
from datetime import datetime

JENKINS_URL = os.getenv("JENKINS_URL")
JOB_NAME    = os.getenv("JOB_NAME")
USERNAME    = os.getenv("USERNAME")
API_TOKEN   = os.getenv("API_TOKEN")

API_URL = f"{JENKINS_URL}/job/{JOB_NAME}/api/json?tree=builds[number,result,timestamp,duration,url]{{0,5}}"

response = requests.get(API_URL, auth=(USERNAME, API_TOKEN))
response.raise_for_status()

data = response.json()
builds = data.get("builds", [])

# Save raw builds
with open("raw_builds.json", "w") as f:
    json.dump(builds, f, indent=2)

# ---- ANALYTICS ----
success = sum(1 for b in builds if b["result"] == "SUCCESS")
failed  = sum(1 for b in builds if b["result"] == "FAILURE")
avg_duration = sum(b["duration"] for b in builds) / len(builds)

health_score = 100
health_score -= failed * 15
health_score -= 10 if avg_duration > 120000 else 0
health_score = max(0, health_score)

analysis = {
    "total_builds": len(builds),
    "success": success,
    "failed": failed,
    "average_duration_ms": int(avg_duration),
    "health_score": health_score,
    "generated_at": datetime.now().isoformat()
}

with open("analysis.json", "w") as f:
    json.dump(analysis, f, indent=2)

# ---- VERSIONED FILE ----
existing = [f for f in os.listdir(".") if f.startswith("last5_builds_")]
version = len(existing) + 1

with open(f"last5_builds_{version}.json", "w") as f:
    json.dump(builds, f, indent=2)

print("Build Intelligence Generated Successfully")
