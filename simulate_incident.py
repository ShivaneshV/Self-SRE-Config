import requests
import argparse

def trigger(scenario):
    url = "http://localhost:5000/trigger"
    try:
        response = requests.post(url, json={"scenario": scenario})
        if response.status_code == 200:
            print(f"[OK] Chaos Monkey injected scenario: {scenario.upper()}")
        else:
            print(f"[ERROR] Failed. Server returned: {response.text}")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Self.SRE Chaos Monkey Simulator")
    parser.add_argument('--burnout', action='store_true', help="Trigger Sev-1 Heart Rate Spike")
    parser.add_argument('--linter', action='store_true', help="Trigger Bio-Linter Fail")
    parser.add_argument('--rest', action='store_true', help="Trigger SLA Sleep Recovery")
    parser.add_argument('--merge', action='store_true', help="Trigger MR Approval Webhook")
    
    args = parser.parse_args()

    if args.burnout: trigger('burnout')
    elif args.linter: trigger('linter')
    elif args.rest: trigger('rest')
    elif args.merge:
        try:
            requests.post("http://localhost:5000/webhook", json={"object_kind": "merge_request", "object_attributes": {"state": "merged"}})
            print("[OK] Simulated GitLab MR Approval Webhook")
        except:
            print("[ERROR] Could not connect to Webhook receiver.")
    else:
        print("Specify a flag: --burnout, --linter, --rest, or --merge")
