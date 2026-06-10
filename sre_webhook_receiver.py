from flask import Flask, request, jsonify, send_from_directory
import time
import sys
import logging
import json
import os

# Ensure terminal output supports Unicode (emojis) on all platforms, including Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    # Fallback for older Python versions
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

app = Flask(__name__)

# ANSI escape codes for terminal styling
class Colors:
    CYAN = '\033[96m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Global state for dashboard telemetry
operational_status = "HEALTHY"
logs_list = ["[INFO] Awaiting GitLab Merge Request signals..."]
current_schedule = []

def load_schedule():
    global current_schedule
    try:
        with open('schedule.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            current_schedule = data.get('commitments', [])
    except Exception as e:
        print(f"Error loading schedule.json: {e}", flush=True)

def typing_effect(text, color=Colors.CYAN, delay=0.03):
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Colors.RESET + '\n')
    time.sleep(0.3)

@app.route('/')
def serve_dashboard():
    # Serve index.html from root folder
    return send_from_directory('.', 'index.html')

@app.route('/status', methods=['GET'])
def get_status():
    global operational_status, logs_list, current_schedule
    return jsonify({
        "status": operational_status,
        "logs": logs_list,
        "schedule": current_schedule
    }), 200

@app.route('/webhook', methods=['POST'])
def gitlab_webhook():
    global operational_status, logs_list, current_schedule
    data = request.json
    
    # Verify it's a merge request event and it's been merged
    if data and data.get('object_kind') == 'merge_request':
        state = data.get('object_attributes', {}).get('state')
        
        if state == 'merged':
            # Update local memory SRE telemetry states
            operational_status = 'RECOVERY_MODE'
            
            for item in current_schedule:
                item['status'] = 'CANCELLED'
            
            logs_list = [
                "[!] CRITICAL ALERT: HUMAN NODE FAILURE ACKNOWLEDGED",
                "[*] Action: GitLab Merge Request Approved by Human",
                "[*] Initiating Self.SRE Failover Protocol...",
                ">> Fetching updated schedule.json from master branch...",
                ">> Diff analyzed: 3 high-priority blocks shifted.",
                "[SUCCESS] System Status Updated: 🔴 OFFLINE / RECOVERY_MODE",
                "[SUCCESS] Google Calendar API: Wiped afternoon blocks.",
                "[SUCCESS] Slack API: Set status to 🤒 'SEV-1 Biological Incident'",
                "[SUCCESS] Gmail API: Dispatched cancellation to Client Q3 Review.",
                "[SUCCESS] Teams API: Delegated Daily Standup to sarah.dev@company.com.",
                "[+] ALL FAILOVER TASKS COMPLETED. HUMAN NODE IS CLEARED FOR REST."
            ]

            # Trigger sci-fi terminal typing animation on the server console
            print("\n" + Colors.YELLOW + "="*60 + Colors.RESET, flush=True)
            typing_effect("[!] CRITICAL ALERT: HUMAN NODE FAILURE ACKNOWLEDGED", Colors.RED)
            typing_effect("[*] Action: GitLab Merge Request Approved by Human", Colors.YELLOW)
            typing_effect("[*] Initiating Self.SRE Failover Protocol...", Colors.CYAN)
            print(Colors.YELLOW + "="*60 + Colors.RESET + "\n", flush=True)
            
            typing_effect(">> Fetching updated schedule.json from master branch...", Colors.CYAN, 0.01)
            typing_effect(">> Diff analyzed: 3 high-priority blocks shifted.", Colors.CYAN, 0.01)
            
            print(flush=True)
            typing_effect("[SUCCESS] System Status Updated: 🔴 OFFLINE / RECOVERY_MODE", Colors.GREEN)
            typing_effect("[SUCCESS] Google Calendar API: Wiped afternoon blocks.", Colors.GREEN)
            typing_effect("[SUCCESS] Slack API: Set status to 🤒 'SEV-1 Biological Incident'", Colors.GREEN)
            typing_effect("[SUCCESS] Gmail API: Dispatched cancellation to Client Q3 Review.", Colors.GREEN)
            typing_effect("[SUCCESS] Teams API: Delegated Daily Standup to sarah.dev@company.com.", Colors.GREEN)
            
            print("\n" + Colors.BOLD + Colors.CYAN + "[+] ALL FAILOVER TASKS COMPLETED. HUMAN NODE IS CLEARED FOR REST." + Colors.RESET + "\n", flush=True)
            
            return jsonify({"status": "failover_executed"}), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    # Disable default Flask logging for a cleaner terminal visual
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Load initial commitments
    load_schedule()
    
    print(Colors.BOLD + Colors.CYAN + "Self.SRE Webhook Receiver & Dashboard Serve Active [Port 5000]..." + Colors.RESET, flush=True)
    print("Awaiting GitLab Merge Request signals...\n", flush=True)
    app.run(port=5000)
