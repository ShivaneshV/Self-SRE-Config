# 🚑 Self.SRE (Human Site Reliability Engineering)
**Google Cloud Rapid Agent Hackathon (June 2026)**  
**Partner Track:** GitLab Track ($5,000 Bucket)  
**License:** [MIT License](LICENSE)  

---

## 💡 The Concept
When a production server crashes, Site Reliability Engineering (SRE) systems instantly reroute traffic, spin up standby resources, and page developers via DevOps pipelines. But when a **human engineer** crashes (burnout, migraine, family emergency), our calendars collapse into chaos.

**Self.SRE** treats the human as a production cluster, and their daily life schedule as configuration code. Stored as `schedule.json` in a GitLab repository, your schedule is linted, merged, and failed over GitOps-style. 

Using Google Cloud Agent Builder and the **GitLab MCP**, Gemini acts as your autonomous SRE manager:
1. **Lints schedules** through GitLab CI/CD to prevent cognitive overload.
2. **Deploys hotfix MRs** to reschedule tasks if a conflict is detected.
3. **Executes failovers** when biometrics spike (canceling low-priority tasks, setting Slack OOO statuses, and auto-scaling workload to a Gemini Digital Twin Proxy).

---

## 🖥️ The Interactive Dashboard Features
The dashboard serves as a high-fidelity Mission Control Center with dual operation modes (Graceful Degrading Sync):
- **LIVE API SYNC**: When run alongside the Python receiver, the UI polls local biometrics, syncs GitLab webhook logs, and updates schedules in real-time.
- **LOCAL UI SIMULATION**: Hosted statically on Netlify/Vercel, the dashboard falls back to a browser simulation so judges can interact with all SRE scenario workflows locally.

### Tabs & Command Panels
- **Live Mission Control**: Glowing HTML5 Canvas ECG heartbeat line, biometrics (Heart Rate, Stress Index), log stream, and target schedule.
- **CI/CD Bio-Pipeline**: Visualizes parser validation checks. Shows linter compilation logs and lets you merge hotfix Merge Requests to resolve overload conflicts.
- **SLA Policies (YAML)**: Displays your `self-sre.config.yaml` SRE policy parameters (max heart rate thresholds, sleep budget targets, escalation targets).
- **Incident Hub**: List of past incidents. Click on any log entry (`INC-9012`, `INC-9011`, `INC-9010`) to print its Blameless Postmortem (RCA, actions taken, and commit logs) inside a mock terminal.
- **Operations Guide**: Architectural briefs explaining the GitOps flow, GitLab MCP configurations, and biological terminology mapping.

---

## 🤖 The AI "God Prompt"
*We configured the Google Cloud Agent Builder with the following system instructions:*

> "You are Self.SRE, an autonomous Site Reliability Engineer for a human user. The user's life configuration is stored in a GitLab repository. When the user reports a physical disruption (e.g., illness, flat tire): 
> 1. Use the GitLab MCP to read `schedule.json` on the main branch. 
> 2. Create a GitLab Issue titled 'SEV-1 Incident: [Reason]' to track the disruption. 
> 3. Create a new Git branch (e.g., `hotfix/recovery`).
> 4. Modify the `schedule.json` to change `operational_status` to 'RECOVERY' and alter the tasks for the day (e.g., changing STATUS to CANCELLED).
> 5. Commit the changes and open a GitLab Merge Request so the human can review and approve the failover protocol."

---

## 🛠️ Demo Instructions (Local Testing)
1. **Install Dependencies**:
   ```bash
   pip install flask flask-cors requests
   ```
2. **Launch Receiver**:
   ```bash
   python sre_webhook_receiver.py
   ```
3. **Open Dashboard**:
   Open `index.html` in Chrome. You will see `LIVE API SYNC` (green) in the top left.
4. **Trigger Incidents (Hacker CLI)**:
   - *Linter Warning*: `python simulate_incident.py --linter` (Updates badge to yellow; inspect pipeline tab and click "Merge MR" to solve).
   - *Burnout Outage*: `python simulate_incident.py --burnout` (Spikes ECG canvas to red tachycardia; counts down 5s to trigger failover).
   - *SLA Sleep Deficit*: `python simulate_incident.py --rest` (Slows ECG to blue sine wave; inserts mandatory recovery blocks).
   - *Webhook Merge MR*: `python simulate_incident.py --merge` (Simulates a merged GitLab MR, updating the UI schedule list to delegated/AI-scaled states).
