from flask import Flask, jsonify, request
from flask_cors import CORS
from detection import run_detection

app = Flask(__name__)
CORS(app)  # Allows frontend to call this API

# ── Run detection once when server starts ──
print("Starting detection engine...")
df, alerts = run_detection()
logs = df.to_dict(orient="records")
print(f"Server ready! {len(logs)} logs | {len(alerts)} alerts")

# ── Playbooks ──
PLAYBOOKS = {
    "BRUTE_FORCE": [
        "Block the attacking IP immediately in firewall",
        "Reset passwords for all targeted accounts",
        "Enable account lockout after 5 failed attempts",
        "Check if any login succeeded before blocking",
        "Report IP to threat intelligence platform"
    ],
    "C2_BEACON": [
        "Isolate the infected machine from network immediately",
        "Block the external C2 IP in firewall",
        "Run full malware scan on infected machine",
        "Check all outbound connections from that machine",
        "Rebuild the machine if malware is confirmed"
    ],
    "ANOMALY": [
        "Investigate the flagged IP manually",
        "Check if this is a known admin or service IP",
        "Monitor the IP for next 24 hours",
        "Cross-check with user activity logs",
        "Escalate to senior analyst if suspicious"
    ]
}

# ──────────────────────────────────────────
# API Endpoint 1 — Get all logs
# ──────────────────────────────────────────
@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify({
        "total": len(logs),
        "logs": logs
    })

# ──────────────────────────────────────────
# API Endpoint 2 — Get all alerts
# ──────────────────────────────────────────
@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    return jsonify({
        "total": len(alerts),
        "alerts": alerts
    })

# ──────────────────────────────────────────
# API Endpoint 3 — Get playbook by threat
# ──────────────────────────────────────────
@app.route("/api/playbook", methods=["GET"])
def get_playbook():
    threat_type = request.args.get("type", "ANOMALY").upper()
    steps = PLAYBOOKS.get(threat_type, PLAYBOOKS["ANOMALY"])
    return jsonify({
        "threat_type": threat_type,
        "steps": steps
    })

# ──────────────────────────────────────────
# Run the server
# ──────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
