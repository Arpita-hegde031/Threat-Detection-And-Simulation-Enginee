📌 Overview
Organizations face an ever-growing threat surface — from brute force attacks to sophisticated Command & Control (C2) beaconing. This project simulates a mini Security Operations Center that:

Ingests and analyzes network log data in real time
Detects threats using a dual-layer approach — rule-based engine + ML anomaly detection
Displays live alerts on a custom SOC-style dashboard
Provides plain-English explanations for every alert raised


✨ Features
FeatureDescription🔴 Brute Force DetectionFlags IPs with repeated failed login attempts on SSH (port 22)🟣 C2 Beacon DetectionIdentifies machines periodically connecting to external C2 servers🟡 ML Anomaly DetectionUses Isolation Forest to flag statistically unusual traffic📊 Live DashboardReal-time alert feed with severity badges and reasons📖 PlaybooksClick any alert to see recommended incident response steps⚡ High ThroughputHandles 1000+ log events per simulation run

🎥 Demo

Dashboard screenshot coming soon


🧱 Tech Stack
Backend

Python 3.10+ — Core language
Flask — REST API server
Flask-CORS — Cross-origin support
Scikit-learn — Isolation Forest ML model
Pandas — Log normalization and analysis
Faker — Synthetic log generation

Frontend

HTML5 + CSS3 — Custom SOC-style dark UI
Vanilla JavaScript — Live data fetching every 3 seconds

DevOps

GitHub Actions — CI/CD pipeline
Render.com — Free cloud deployment


📁 Project Structure
ai-threat-detection-dashboard/
│
├── backend/
│   ├── generator.py       → Synthetic network log generator
│   ├── detection.py       → Rule engine + ML threat detection
│   └── app.py             → Flask REST API (3 endpoints)
│
├── frontend/
│   ├── index.html         → SOC dashboard layout
│   ├── style.css          → Dark theme SOC styling
│   └── script.js          → Live API fetching + UI updates
│
├── .github/
│   └── workflows/
│       └── deploy.yml     → GitHub Actions CI/CD
│
├── .gitignore
├── requirements.txt
└── README.md

⚙️ Installation
Prerequisites

Python 3.10+
pip
Git

1. Clone the Repository
bashgit clone https://github.com/Arpita-hegde031/ai-threat-detection-dashboard.git
cd ai-threat-detection-dashboard
2. Install Dependencies
bashpip install -r requirements.txt
3. Run the Backend
bashcd backend
python app.py
4. Open the Frontend
bash# Just open this file in your browser
frontend/index.html

🔍 How It Works
┌─────────────────┐
│  generator.py   │  →  Creates 1000 fake network logs
│  (Fake Logs)    │     80% Normal | 10% Brute Force | 10% C2 Beacon
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  detection.py   │  →  Layer 1: Rule Engine
│  (Brain)        │     Layer 2: Isolation Forest ML
└────────┬────────┘     Tags each log: threat_type + severity + reason
         │
         ▼
┌─────────────────┐
│    app.py       │  →  Flask serves 3 REST endpoints
│  (Flask API)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │  →  JS fetches every 3 seconds
│  (Frontend)     │     Live log feed + alert panel + playbook modal
└─────────────────┘

🚨 Threat Detection Logic
Rule Engine
ThreatRuleSeverityBrute ForceSame IP with 5+ failed logins (status 401) on port 22🔴 HighC2 Beaconing3+ connections to same external IP on port 4444 with <150 bytes🟣 Critical
ML Detection (Isolation Forest)

Trains on features: dst_port, bytes, status, protocol
Contamination rate: 10% (expects ~10% anomalies)
Flags statistically unusual events as Medium severity anomalies
Deduplicates alerts — one alert per unique IP


🌐 API Endpoints
EndpointMethodDescription/api/logsGETReturns last 1000 normalized log events/api/alertsGETReturns all active threat alerts/api/playbook?type=BRUTE_FORCEGETReturns response steps for threat type
Example Response — /api/alerts
json[
  {
    "src_ip": "45.33.32.156",
    "threat_type": "BRUTE_FORCE",
    "severity": "High",
    "confidence": 100,
    "reason": "IP 45.33.32.156 made 100 failed login attempts on port 22"
  },
  {
    "src_ip": "Multiple Internal IPs",
    "threat_type": "C2_BEACON",
    "severity": "Critical",
    "confidence": 100,
    "reason": "100 machines beaconing to external C2 server 185.220.101.45"
  }
]

📋 Requirements
flask
flask-cors
scikit-learn
pandas
numpy
faker
Install all at once:
bashpip install flask flask-cors scikit-learn pandas numpy faker

🗺️ Roadmap

 Synthetic log generator
 Rule-based threat detection
 ML anomaly detection (Isolation Forest)
 Flask REST API
 Live SOC dashboard (HTML/CSS/JS)
 Incident playbooks
 GitHub Actions CI/CD
 Render deployment


👩‍💻 Author
Arpita Hegde

📧 arpitahegde0312004@gmail.com
💼 LinkedIn
🐙 GitHub
