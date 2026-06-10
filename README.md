# 🚑 Self.SRE (Human Site Reliability Engineering)
**Google Cloud Rapid Agent Hackathon (June 2026)**  
**Partner Track:** GitLab ($5,000 Bucket)  
**License:** [MIT License](LICENSE)  

## The Concept
If a production server crashes, Site Reliability Engineering (SRE) systems instantly reroute traffic and page developers via DevOps pipelines. But when a *human being* crashes (migraine, burnout, family emergency), our daily routines dissolve into chaos. 

**Self.SRE** treats you as a production server, and your daily life as a version-controlled repository. Using Google Cloud Agent Builder and the **GitLab MCP**, Gemini acts as your autonomous DevOps operations manager. 

When you declare a biological incident, it modifies your physical `schedule.json`, opens a GitLab Issue for triage, and prepares a Merge Request. Once you, the human, approve the MR, local webhooks execute the physical failover (Slack auto-replies, calendar shifts, client emails).

## The AI "God Prompt"
*We used the following system instructions in Google Cloud Agent Builder:*

> "You are Self.SRE, an autonomous Site Reliability Engineer for a human user. The user's life configuration is stored in a GitLab repository. When the user reports a physical disruption (e.g., illness, flat tire): 
> 1. Use the GitLab MCP to read `schedule.json` on the main branch. 
> 2. Create a GitLab Issue titled 'SEV-1 Incident: [Reason]' to track the disruption. 
> 3. Create a new Git branch (e.g., `hotfix/recovery`).
> 4. Modify the `schedule.json` to change `operational_status` to 'RECOVERY' and alter the tasks for the day (e.g., changing STATUS to CANCELLED).
> 5. Commit the changes and open a GitLab Merge Request so the human can review and approve the failover protocol."

## Demo Instructions (How to test locally)
1. Install dependencies: `pip install flask requests`
2. Run the local receiver: `python sre_webhook_receiver.py`
3. Open your Agent Builder chat, report an incident (e.g., *"I have a massive migraine."*)
4. Watch the Agent interact with the GitLab MCP to create the Issue, Branch, and Merge Request.
5. Go to GitLab and click "Merge" on the MR.
6. (For local testing) Run `python simulate_incident.py` to trigger the local webhook receiver and watch the terminal execute the Slack/Email failover!
