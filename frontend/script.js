const API = "http://localhost:5000";

// ── Auth Check ────────────────────────────────
const currentUser = JSON.parse(localStorage.getItem("soc_user"));
if (!currentUser) {
  window.location.href = "login.html";
}

// Show username in header
document.getElementById("user-info").textContent =
  "👤 " + currentUser.fullname;

// ── Logout ────────────────────────────────────
function logout() {
  localStorage.removeItem("soc_user");
  window.location.href = "login.html";
}

// ── Fetch Alerts ──────────────────────────────
async function fetchAlerts() {
  try {
    const res  = await fetch(`${API}/api/alerts`);
    const data = await res.json();
    renderAlerts(data.alerts);
    updateStats(data.alerts);
  } catch (e) {
    console.error("Error fetching alerts:", e);
    document.getElementById("alert-list").innerHTML =
      '<div class="loading">⚠️ Cannot connect to backend. Make sure Flask is running.</div>';
  }
}

// ── Fetch Logs ────────────────────────────────
async function fetchLogs() {
  try {
    const res  = await fetch(`${API}/api/logs`);
    const data = await res.json();
    renderLogs(data.logs.slice(0, 100));
    document.getElementById("total-logs").textContent = data.total;
    document.getElementById("log-badge").textContent  = data.total;
    document.getElementById("last-updated").textContent =
      "Updated: " + new Date().toLocaleTimeString();
  } catch (e) {
    console.error("Error fetching logs:", e);
  }
}

// ── Render Alerts ─────────────────────────────
function renderAlerts(alerts) {
  const list = document.getElementById("alert-list");
  list.innerHTML = "";

  if (alerts.length === 0) {
    list.innerHTML = '<div class="loading">No alerts detected.</div>';
    return;
  }

  alerts.forEach(alert => {
    const card = document.createElement("div");
    card.className = `alert-card ${alert.severity}`;
    card.innerHTML = `
      <div class="alert-top">
        <span class="threat-type">${alert.threat_type}</span>
        <span class="severity-badge sev-${alert.severity}">${alert.severity}</span>
      </div>
      <div class="alert-ip">📍 ${alert.src_ip}</div>
      <div class="alert-reason">${alert.reason}</div>
      <div class="confidence-bar">
        <div class="confidence-fill" style="width:${alert.confidence}%"></div>
      </div>
      <div class="confidence-label">Confidence: ${alert.confidence}%</div>
      <div class="playbook-hint">Click to view playbook →</div>
    `;
    card.addEventListener("click", () => openPlaybook(alert));
    list.appendChild(card);
  });
}

// ── Render Logs ───────────────────────────────
function renderLogs(logs) {
  const tbody = document.getElementById("log-body");
  tbody.innerHTML = "";

  logs.forEach(log => {
    const row = document.createElement("tr");
    row.className = log.event_type;
    const time = log.timestamp.split(" ")[1].split(".")[0];
    row.innerHTML = `
      <td>${time}</td>
      <td>${log.src_ip}</td>
      <td>${log.dst_ip || "--"}</td>
      <td>${log.dst_port}</td>
      <td>${log.status}</td>
      <td>${log.bytes}</td>
      <td>${log.protocol}</td>
      <td>
        <span class="type-badge type-${log.event_type}">
          ${log.event_type}
        </span>
      </td>
    `;
    tbody.appendChild(row);
  });
}

// ── Update Stats ──────────────────────────────
function updateStats(alerts) {
  document.getElementById("total-alerts").textContent  = alerts.length;
  document.getElementById("alert-badge").textContent   = alerts.length;
  document.getElementById("critical-count").textContent =
    alerts.filter(a => a.severity === "Critical").length;
  document.getElementById("high-count").textContent =
    alerts.filter(a => a.severity === "High").length;
  document.getElementById("medium-count").textContent =
    alerts.filter(a => a.severity === "Medium").length;
}

// ── Playbook Modal ────────────────────────────
async function openPlaybook(alert) {
  try {
    const res  = await fetch(`${API}/api/playbook?type=${alert.threat_type}`);
    const data = await res.json();

    document.getElementById("modal-title").textContent =
      `📋 Playbook — ${alert.threat_type}`;
    document.getElementById("modal-subtitle").textContent =
      `Severity: ${alert.severity}  |  Confidence: ${alert.confidence}%`;
    document.getElementById("modal-reason").textContent =
      `🔍 ${alert.reason}`;

    const stepsList = document.getElementById("playbook-steps");
    stepsList.innerHTML = "";
    data.steps.forEach(step => {
      const li = document.createElement("li");
      li.textContent = step;
      stepsList.appendChild(li);
    });

    document.getElementById("modal-overlay").classList.add("active");
  } catch (e) {
    console.error("Error fetching playbook:", e);
  }
}

function closeModal() {
  document.getElementById("modal-overlay").classList.remove("active");
}

// Close modal on Escape key
document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeModal();
});

// ── Auto Refresh Every 5 Seconds ─────────────
function refresh() {
  fetchAlerts();
  fetchLogs();
}

refresh();
setInterval(refresh, 5000);