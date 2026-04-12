import random
import datetime
from faker import Faker

fake = Faker()

# ── Fixed attacker IPs for patterns ──
BRUTE_FORCE_IP = "45.33.32.156"
C2_IP          = "185.220.101.45"
NORMAL_IPS     = [fake.ipv4_private() for _ in range(10)]

def random_time():
    return datetime.datetime.now() + datetime.timedelta(
        seconds=random.randint(1, 10))

def generate_normal_log():
    return {
        "timestamp":  str(random_time()),
        "src_ip":     random.choice(NORMAL_IPS),
        "dst_ip":     fake.ipv4_public(),
        "dst_port":   random.choice([80, 443, 3306, 8080]),
        "protocol":   random.choice(["TCP", "UDP", "HTTP"]),
        "bytes":      random.randint(200, 3000),
        "status":     random.choice([200, 201, 204, 301]),
        "event_type": "NORMAL"
    }

def generate_brute_force_log():
    return {
        "timestamp":  str(random_time()),
        "src_ip":     BRUTE_FORCE_IP,
        "dst_ip":     fake.ipv4_private(),
        "dst_port":   22,
        "protocol":   "TCP",
        "bytes":      random.randint(100, 200),
        "status":     401,
        "event_type": "BRUTE_FORCE"
    }

def generate_c2_beacon_log():
    return {
        "timestamp":  str(random_time()),
        "src_ip":     random.choice(NORMAL_IPS),  # ← FIXED (reuse fixed IPs)
        "dst_ip":     C2_IP,
        "dst_port":   4444,
        "protocol":   "TCP",
        "bytes":      random.randint(40, 100),
        "status":     200,
        "event_type": "C2_BEACON"
    }

def generate_all_logs(total=1000):
    logs = []

    for _ in range(int(total * 0.80)):
        logs.append(generate_normal_log())

    for _ in range(int(total * 0.10)):
        logs.append(generate_brute_force_log())

    for _ in range(int(total * 0.10)):
        logs.append(generate_c2_beacon_log())

    random.shuffle(logs)
    return logs


# ── Test it ──
if __name__ == "__main__":
    logs = generate_all_logs(1000)
    for i, log in enumerate(logs):
        print(f"[{i+1}] {log['event_type']:12} | "
              f"IP: {log['src_ip']:16} | "
              f"Port: {log['dst_port']:5} | "
              f"Status: {log['status']} | "
              f"Bytes: {log['bytes']}")