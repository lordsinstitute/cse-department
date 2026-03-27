const BACKEND_HTTP = "http://127.0.0.1:9000";
const BACKEND_WS = "ws://127.0.0.1:9000/ws/alerts";

const kpiTotal = document.getElementById("kpi-total");
const kpiHigh = document.getElementById("kpi-high");
const kpiSrcIps = document.getElementById("kpi-src-ips");
const kpiStream = document.getElementById("kpi-stream");
const alertCountLabel = document.getElementById("alert-count-label");
const tableBody = document.getElementById("alert-table-body");
const wsStatusDot = document.getElementById("ws-status-dot");
const wsStatusText = document.getElementById("ws-status-text");
const btnPause = document.getElementById("btn-pause");
const btnResume = document.getElementById("btn-resume");
const btnClear = document.getElementById("btn-clear");
const filterAttack = document.getElementById("filter-attack");
const filterSeverity = document.getElementById("filter-severity");
const filterSearch = document.getElementById("filter-search");
const filterSort = document.getElementById("filter-sort");
const filterDedupe = document.getElementById("filter-dedupe");
const btnApplyFilters = document.getElementById("btn-apply-filters");
const btnRefreshStats = document.getElementById("btn-refresh-stats");
const statsBySeverity = document.getElementById("stats-by-severity");
const statsTopIps = document.getElementById("stats-top-ips");

let ws = null;
let paused = false;
let alerts = [];
const srcIpSet = new Set();

function setWsStatus(connected) {
  if (connected) {
    wsStatusDot.classList.remove("bg-red-500");
    wsStatusDot.classList.add("bg-emerald-400");
    wsStatusText.textContent = "Connected";
  } else {
    wsStatusDot.classList.remove("bg-emerald-400");
    wsStatusDot.classList.add("bg-red-500");
    wsStatusText.textContent = "Disconnected";
  }
}

function severityClass(severity) {
  switch (severity) {
    case "critical":
      return "text-red-400 bg-red-500/10 border border-red-500/40";
    case "high":
      return "text-orange-300 bg-orange-500/10 border border-orange-500/40";
    case "medium":
      return "text-amber-300 bg-amber-500/10 border border-amber-500/30";
    case "low":
      return "text-sky-300 bg-sky-500/10 border border-sky-500/30";
    default:
      return "text-slate-300 bg-slate-700/60 border border-slate-600/60";
  }
}

function formatTime(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleTimeString();
  } catch {
    return iso;
  }
}

function updateKpis() {
  kpiTotal.textContent = alerts.length.toString();
  const highCount = alerts.filter((a) =>
    ["high", "critical"].includes(a.severity)
  ).length;
  kpiHigh.textContent = highCount.toString();
  kpiSrcIps.textContent = srcIpSet.size.toString();
  alertCountLabel.textContent = `(${alerts.length})`;
  kpiStream.textContent = alerts.length ? "Streaming alerts" : "Waiting for data...";
}

function renderTable() {
  tableBody.innerHTML = "";
  for (const alert of alerts) {
    const tr = document.createElement("tr");
    tr.className = "border-b border-slate-800/80 hover:bg-slate-800/60 transition-colors";
    const conf = alert.confidence != null ? (alert.confidence * 100).toFixed(0) + "%" : "—";
    const mitre = (alert.mitre_techniques && alert.mitre_techniques.length)
      ? " " + alert.mitre_techniques.join(", ")
      : "";
    tr.innerHTML = `
      <td class="px-2 py-1 whitespace-nowrap text-slate-300">${formatTime(alert.created_at)}</td>
      <td class="px-2 py-1 whitespace-nowrap">
        <span class="px-1.5 py-0.5 rounded-full text-[10px] font-medium inline-flex items-center justify-center ${severityClass(alert.severity)}">
          ${(alert.severity || "").toUpperCase()}
        </span>
      </td>
      <td class="px-2 py-1 whitespace-nowrap text-slate-200">${alert.attack_type || "—"}</td>
      <td class="px-2 py-1 whitespace-nowrap text-slate-200">${alert.src_ip}</td>
      <td class="px-2 py-1 whitespace-nowrap text-slate-200">${alert.dst_ip}</td>
      <td class="px-2 py-1 whitespace-nowrap text-slate-300">${alert.protocol} : ${alert.dst_port}</td>
      <td class="px-2 py-1 whitespace-nowrap text-slate-300">${(alert.score != null ? alert.score : 0).toFixed(2)}</td>
      <td class="px-2 py-1 whitespace-nowrap text-slate-300" title="Confidence">${conf}</td>
      <td class="px-2 py-1 text-slate-400" title="${mitre}">${alert.summary || "—"}</td>
    `;
    tableBody.appendChild(tr);
  }
}

function addAlert(alert) {
  alerts.unshift(alert);
  srcIpSet.add(alert.src_ip);
  if (alerts.length > 500) alerts = alerts.slice(0, 500);
  updateKpis();
  if (!paused) renderTable();
}

function buildAlertsUrl() {
  const params = new URLSearchParams();
  params.set("limit", "500");
  if (filterAttack.value) params.set("attack_type", filterAttack.value);
  if (filterSeverity.value) params.set("severity", filterSeverity.value);
  if (filterSearch.value.trim()) params.set("search", filterSearch.value.trim());
  params.set("sort", filterSort.value);
  if (filterDedupe.checked) params.set("dedupe", "true");
  return `${BACKEND_HTTP}/api/alerts?${params.toString()}`;
}

async function fetchAlertsWithFilters() {
  try {
    const resp = await fetch(buildAlertsUrl());
    if (!resp.ok) return;
    const data = await resp.json();
    alerts = data;
    srcIpSet.clear();
    for (const a of alerts) srcIpSet.add(a.src_ip);
    updateKpis();
    renderTable();
  } catch (e) {
    console.warn("Failed to fetch alerts", e);
  }
}

async function fetchInitialAlerts() {
  await fetchAlertsWithFilters();
}

async function fetchStats() {
  try {
    const resp = await fetch(`${BACKEND_HTTP}/api/stats`);
    if (!resp.ok) return;
    const data = await resp.json();
    if (data.by_severity && Object.keys(data.by_severity).length) {
      statsBySeverity.innerHTML = Object.entries(data.by_severity)
        .map(([s, c]) => `<div><span class="text-slate-500">${s}</span>: ${c}</div>`)
        .join("");
    } else {
      statsBySeverity.textContent = "No data";
    }
    if (data.top_source_ips && data.top_source_ips.length) {
      statsTopIps.innerHTML = data.top_source_ips
        .slice(0, 8)
        .map((o) => `<div><span class="text-emerald-400">${o.ip}</span> ${o.count}</div>`)
        .join("");
    } else {
      statsTopIps.textContent = "No data";
    }
  } catch (e) {
    console.warn("Failed to fetch stats", e);
  }
}

function connectWebSocket() {
  try {
    ws = new WebSocket(BACKEND_WS);
  } catch (e) {
    console.error("Failed to create WebSocket", e);
    setWsStatus(false);
    return;
  }
  ws.onopen = () => {
    setWsStatus(true);
    ws.send("hello");
  };
  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data);
      if (msg.type === "alert" && msg.data) addAlert(msg.data);
    } catch (_) {}
  };
  ws.onclose = () => {
    setWsStatus(false);
    setTimeout(connectWebSocket, 3000);
  };
  ws.onerror = () => setWsStatus(false);
}

btnPause.addEventListener("click", () => {
  paused = true;
  btnPause.classList.add("hidden");
  btnResume.classList.remove("hidden");
});
btnResume.addEventListener("click", () => {
  paused = false;
  btnResume.classList.add("hidden");
  btnPause.classList.remove("hidden");
  renderTable();
});
btnClear.addEventListener("click", () => {
  alerts = [];
  srcIpSet.clear();
  updateKpis();
  renderTable();
});
btnApplyFilters.addEventListener("click", fetchAlertsWithFilters);
btnRefreshStats.addEventListener("click", fetchStats);

window.addEventListener("load", () => {
  fetchInitialAlerts();
  fetchStats();
  connectWebSocket();
});
