# 🛡️ AI Threat Detection & SOC Dashboard

A full-stack **Security Operations Center (SOC)** dashboard that uses machine learning to detect, classify, and respond to network threats in real time. Built with Python (Flask) on the backend and vanilla JavaScript on the frontend.

---

## 📸 Preview

> Real-time dashboard showing live network logs, threat alerts, severity classification, and incident response playbooks.

---

## 🚀 Features

- 🔍 **ML-Based Threat Detection** — Automatically detects Brute Force attacks, C2 Beacons, and network anomalies from raw network logs
- 📊 **Live Dashboard** — Displays 1000+ network logs with real-time stats (total logs, alerts, critical/high/medium counts)
- 🚨 **Alert Management** — Filter alerts by severity (Critical, High, Medium) and threat type
- 📋 **Incident Playbooks** — Step-by-step response guide for each threat type, loaded dynamically per alert
- 📈 **Visual Analytics** — Donut chart for threat distribution + 12-hour alert timeline using Chart.js
- 🔐 **User Authentication** — Secure login and registration system with session management
- 🌐 **REST API** — Clean Flask API with endpoints for logs, alerts, and playbooks

---

## 🧠 Threat Types Detected

| Threat | Description | Severity |
|--------|-------------|----------|
| **Brute Force** | Repeated failed login attempts from a single IP | Critical / High |
| **C2 Beacon** | Command & Control communication to external IPs | Critical |
| **Anomaly** | Unusual traffic patterns flagged by ML model | Medium |

---

## 🗂️ Project Structure

```
Threat-Detection-And-Simulation-Enginee/
│
├── backend/
│   ├── app.py              # Flask REST API server
│   ├── detection.py        # ML-based threat detection engine
│   ├── generator.py        # Synthetic network log generator
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── index.html          # Main SOC dashboard
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── script.js           # Dashboard logic & API calls
│   ├── style.css           # Dashboard styles
│   └── auth.css            # Login/Register styles
│
└── README.md
```

---

## ⚙️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.12 | Core language |
| Flask | REST API framework |
| Flask-CORS | Cross-origin request handling |
| scikit-learn | Machine learning detection engine |
| pandas | Log data processing |
| numpy | Numerical computations |

### Frontend
| Technology | Purpose |
|------------|---------|
| HTML5 / CSS3 | Structure & styling |
| JavaScript (ES6+) | Dashboard logic |
| Chart.js | Donut & bar chart visualizations |
| LocalStorage | Session management |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/logs` | Returns all network logs |
| GET | `/api/alerts` | Returns all detected threat alerts |
| GET | `/api/playbook?type=BRUTE_FORCE` | Returns incident response steps for a threat type |

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10 or above
- pip

### 1. Clone the repository
```bash
git clone https://github.com/Arpita-hegde031/Threat-Detection-And-Simulation-Enginee.git
cd Threat-Detection-And-Simulation-Enginee
```

### 2. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the Flask server
```bash
python app.py
```
Server starts at `http://localhost:5000`

### 4. Open the dashboard
Open `frontend/index.html` in your browser — or use VS Code Live Server.

---

## 📡 How It Works

```
Network Logs (generator.py)
        ↓
Detection Engine (detection.py)
  - Applies ML model to classify each log
  - Labels: BRUTE_FORCE | C2_BEACON | ANOMALY | NORMAL
        ↓
Flask API (app.py)
  - Exposes logs, alerts, and playbooks via REST endpoints
        ↓
Dashboard (script.js + index.html)
  - Fetches data from API on load
  - Renders alerts, logs, charts in real time
  - Shows incident playbook on alert click
```

---

## 🔐 Authentication Flow

1. User registers with username, full name, and password
2. Credentials stored in browser `localStorage`
3. Login validates credentials and creates a session
4. Dashboard checks session on load — redirects to login if not authenticated
5. Logout clears session and redirects

---

## 📊 Sample Alert Response

```json
{
  "total": 12,
  "alerts": [
    {
      "src_ip": "172.17.249.52",
      "threat_type": "C2_BEACON",
      "severity": "Critical",
      "confidence": 94,
      "reason": "Repeated outbound connections to external IP on port 4444"
    }
  ]
}
```

---

## 🎯 Use Cases

- 🎓 **Students** — Learn how real SOC tools work
- 🔬 **Security Researchers** — Prototype threat detection pipelines
- 💼 **Portfolio** — Demonstrate full-stack + ML + cybersecurity skills
- 🏢 **Small Teams** — Lightweight internal network monitoring

---

## 🌱 Future Improvements

- [ ] Deploy on AWS / GCP / Render
- [ ] Replace synthetic logs with real PCAP / CICIDS dataset
- [ ] Add email alerting for Critical threats
- [ ] Role-based access (Admin / Analyst)
- [ ] Export alerts as PDF report
- [ ] Dark/light theme toggle

---

## 👩‍💻 Author

**Arpita Hegde**
- GitHub: [@Arpita-hegde031](https://github.com/Arpita-hegde031)

