import requests
import time

url = "http://localhost:5000/webhook"

# Exact payload structure GitLab sends on a merge
payload = {
    "object_kind": "merge_request",
    "object_attributes": {
        "state": "merged",
        "action": "merge",
        "title": "SEV-1 Incident: Migraine Recovery Protocol"
    }
}

print("Simulating User clicking 'Approve & Merge' in GitLab...")
time.sleep(1) # Dramatic pause

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"\n[OK] Mock webhook delivered successfully. Status: {response.status_code}")
        print(f"Response: {response.json()}")
except Exception as e:
    print(f"\n[ERROR] Connection failed. Is sre_webhook_receiver.py running on port 5000?\nDetails: {e}")
