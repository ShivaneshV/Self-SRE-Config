from flask import Flask, request, jsonify, send_from_directory
import time
import sys
import logging
import json

# Ensure terminal output supports Unicode (emojis) on all platforms, including Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    # Fallback for older Python versions
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    from flask_cors import CORS
except ImportError:
    print("Please install flask-cors: pip install flask-cors")
    sys.exit(1)

app = Flask(__name__)
CORS(app) # Allow local UI to poll this server

# Global state for Real-Time UI Sync
system_state = {
    "status": "OPERATIONAL",
    "scenario": "none",
    "logs": ["[INFO] SRE Webhook listener active on Port 5000.", "[INFO] Awaiting Chaos Monkey triggers..."],
    "schedule": []
}

class Colors:
    CYAN, RED, GREEN, YELLOW, PURPLE, RESET, BOLD = '\033[96m', '\033[91m', '\033[92m', '\033[93m', '\033[95m', '\033[0m', '\033[1m'

def log_event(text, color=Colors.CYAN):
    # Print to Terminal with immediate flush
    sys.stdout.write(color + text + Colors.RESET + '\n')
    sys.stdout.flush()
    # Save to state for the UI to fetch
    system_state["logs"].append(text)

def load_schedule():
    try:
        with open('schedule.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            system_state["schedule"] = data.get('commitments', [])
    except Exception as e:
        print(f"Error loading schedule.json: {e}", flush=True)

@app.route('/')
def serve_dashboard():
    # Serve index.html from root folder
    return send_from_directory('.', 'index.html')

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(system_state), 200

@app.route('/trigger', methods=['POST'])
def handle_chaos():
    data = request.json
    scenario = data.get('scenario', 'none')
    system_state["scenario"] = scenario
    
    # Reload schedule to clear previous scenario modifications
    load_schedule()
    
    print("\n" + Colors.YELLOW + "="*60 + Colors.RESET, flush=True)
    log_event(f"[CHAOS MONKEY] INJECTING SCENARIO: {scenario.upper()}", Colors.PURPLE)
    
    if scenario == 'burnout':
        system_state["status"] = "ANOMALY"
        log_event(">> Telemetry spiked. Dead Man's Switch armed.", Colors.RED)
    elif scenario == 'linter':
        system_state["status"] = "LINTER_FAIL"
        log_event(">> GitLab Bio-Linter pipeline triggered via API.", Colors.YELLOW)
        log_event(">> FATAL: Cognitive Overload detected in schedule.json", Colors.RED)
    elif scenario == 'rest':
        system_state["status"] = "SLA_BREACH"
        log_event(">> SLA Breach: Sleep Debt exceeds threshold (4.5h).", Colors.YELLOW)
        log_event(">> Auto-generating Merge Request for mandatory REST block.", Colors.CYAN)
        
        # Modify schedule: change gym or evening tasks to Rest
        for item in system_state["schedule"]:
            if item["id"] == "EVT-1003":
                item["task"] = "Mandatory Recovery Block (Rest)"
                item["status"] = "RESTING"
        
    print(Colors.YELLOW + "="*60 + Colors.RESET + "\n", flush=True)
    return jsonify({"status": "scenario_injected"}), 200

@app.route('/webhook', methods=['POST'])
def gitlab_webhook():
    data = request.json
    if data and data.get('object_kind') == 'merge_request' and data.get('object_attributes', {}).get('state') == 'merged':
        
        system_state["status"] = "SEV-1 OUTAGE"
        system_state["scenario"] = "failover"
        
        print("\n" + Colors.YELLOW + "="*60 + Colors.RESET, flush=True)
        log_event("[!] CRITICAL ALERT: HUMAN NODE FAILURE ACKNOWLEDGED", Colors.RED)
        log_event("[*] Action: GitLab Merge Request Approved by Human", Colors.YELLOW)
        log_event("[*] Initiating Self.SRE Failover Protocol...", Colors.CYAN)
        print(Colors.YELLOW + "="*60 + Colors.RESET + "\n", flush=True)
        
        log_event(">> Fetching updated schedule.json from main branch...", Colors.CYAN)
        time.sleep(1)
        log_event("[SUCCESS] System Status Updated: 🔴 OFFLINE / RECOVERY", Colors.GREEN)
        log_event("[SUCCESS] P2 Task Delegated via Slack API.", Colors.GREEN)
        log_event("[WARNING] P1 Task Detected. Executing AI Proxy Auto-Scale...", Colors.PURPLE)
        log_event("[SUCCESS] Gemini Digital Twin spun up and attached to Google Meet.", Colors.GREEN)
        
        # Modify schedule to match recovery state
        for item in system_state["schedule"]:
            if item["id"] == "EVT-1001":
                item["status"] = "DELEGATED"
            elif item["id"] == "EVT-1002":
                item["status"] = "AI PROXY LIVE"
            elif item["id"] == "EVT-1003":
                item["status"] = "CANCELLED"
                
        print("\n" + Colors.BOLD + Colors.CYAN + "[+] FAILOVER COMPLETE. BLAMELESS POSTMORTEM GENERATED." + Colors.RESET + "\n", flush=True)
        return jsonify({"status": "failover_executed"}), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Load commitments from schedule.json
    load_schedule()
    
    print(Colors.BOLD + Colors.CYAN + "Self.SRE Webhook & API Receiver Active [Port 5000]..." + Colors.RESET, flush=True)
    app.run(port=5000)
