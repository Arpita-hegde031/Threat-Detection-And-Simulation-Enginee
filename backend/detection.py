import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from generator import generate_all_logs

# ── Step 1: Load logs from generator ──
def load_logs():
    logs = generate_all_logs(1000)
    df = pd.DataFrame(logs)
    return df

# ── Step 2: Rule Engine ──
def apply_rules(df):
    alerts = []

    # ── Rule 1: Brute Force Detection ──
    # Same IP, port 22, status 401, more than 5 times
    brute = df[(df["dst_port"] == 22) & (df["status"] == 401)]
    brute_counts = brute.groupby("src_ip").size()

    for ip, count in brute_counts.items():
        if count >= 5:
            alerts.append({
                "src_ip":      ip,
                "threat_type": "BRUTE_FORCE",
                "severity":    "High",
                "confidence":  min(100, count),
                "reason":      f"IP {ip} made {count} failed login attempts on port 22"
            })

    # ── Rule 2: C2 Beacon Detection ──
    # Multiple machines connecting to same external IP
    # with very small bytes on port 4444
    c2 = df[(df["bytes"] < 150) & (df["dst_port"] == 4444)]
    c2_counts = c2.groupby("dst_ip").size()  # ← FIXED (group by dst only)

    for dst, count in c2_counts.items():
        if count >= 3:
            alerts.append({
                "src_ip":      "Multiple Internal IPs",
                "threat_type": "C2_BEACON",
                "severity":    "Critical",
                "confidence":  min(100, count * 10),
                "reason":      f"{count} machines beaconing to external C2 server {dst}"
            })

    return alerts

# ── Step 3: Isolation Forest (ML) ──
def apply_ml(df):
    alerts = []

    # Convert text columns to numbers for ML
    le_protocol  = LabelEncoder()
    le_eventtype = LabelEncoder()

    df["protocol_enc"]   = le_protocol.fit_transform(df["protocol"])
    df["event_type_enc"] = le_eventtype.fit_transform(df["event_type"])

    # Features the model will learn from
    features = df[["dst_port", "bytes", "status", "protocol_enc"]]

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,   # Expects 10% anomalies
        random_state=42
    )
    df["anomaly_score"] = model.fit_predict(features)

    # -1 means anomaly, 1 means normal
    anomalies = df[df["anomaly_score"] == -1]

    # Deduplicate — one alert per IP only
    seen_ips = set()
    for _, row in anomalies.iterrows():

        # Skip if already caught by rules
        if row["event_type"] in ["BRUTE_FORCE", "C2_BEACON"]:
            continue

        # Skip duplicate IPs
        if row["src_ip"] in seen_ips:
            continue

        seen_ips.add(row["src_ip"])
        alerts.append({
            "src_ip":      row["src_ip"],
            "threat_type": "ANOMALY",
            "severity":    "Medium",
            "confidence":  75,
            "reason":      f"IP {row['src_ip']} showed unusual traffic on port {row['dst_port']}"
        })

    return alerts

# ── Step 4: Combine Everything ──
def run_detection():
    print("Loading logs...")
    df = load_logs()
    print(f"Total logs loaded: {len(df)}")

    print("\nRunning Rule Engine...")
    rule_alerts = apply_rules(df)
    print(f"Rule-based alerts found: {len(rule_alerts)}")

    print("\nRunning ML Detection...")
    ml_alerts = apply_ml(df)
    print(f"ML-based alerts found: {len(ml_alerts)}")

    all_alerts = rule_alerts + ml_alerts
    print(f"\nTotal alerts: {len(all_alerts)}")

    return df, all_alerts

# ── Test it ──
if __name__ == "__main__":
    df, alerts = run_detection()

    print("\n" + "="*60)
    print("THREAT ALERTS")
    print("="*60)

    for i, alert in enumerate(alerts):
        print(f"\n[{i+1}] {alert['threat_type']} | "
              f"Severity: {alert['severity']}")
        print(f"     IP: {alert['src_ip']}")
        print(f"     Reason: {alert['reason']}")
        print(f"     Confidence: {alert['confidence']}%")