const loginPage = document.getElementById("loginPage");
const dashboard = document.getElementById("dashboard");
const loginBtn = document.getElementById("loginBtn");
const logoutBtn = document.getElementById("logoutBtn");
const loginError = document.getElementById("loginError");
const output = document.getElementById("output");

let accessToken = localStorage.getItem("accessToken");
let refreshToken = localStorage.getItem("refreshToken");

// 初始化 Chart
const ctx = document.getElementById("chart").getContext("2d");
const chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      { label: "CPU %", data: [], borderColor: "lime", tension: 0.2 },
      { label: "内存 %", data: [], borderColor: "cyan", tension: 0.2 },
      { label: "上传 KB/s", data: [], borderColor: "orange", tension: 0.2 },
      { label: "下载 KB/s", data: [], borderColor: "pink", tension: 0.2 },
    ],
  },
  options: { scales: { y: { beginAtZero: true } } },
});

async function api(path, opts = {}) {
  const res = await fetch(path, {
    ...opts,
    headers: {
      "Content-Type": "application/json",
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
  });

  if (res.status === 401 && refreshToken) {
    const ref = await fetch("/refresh", {
      method: "POST",
      headers: { Authorization: `Bearer ${refreshToken}` },
    });
    if (ref.ok) {
      const data = await ref.json();
      accessToken = data.access_token;
      localStorage.setItem("accessToken", accessToken);
      return api(path, opts);
    } else {
      logout();
    }
  }

  return res.ok ? res.json() : null;
}

loginBtn.onclick = async () => {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (res.ok) {
    const data = await res.json();
    accessToken = data.access_token;
    refreshToken = data.refresh_token;
    localStorage.setItem("accessToken", accessToken);
    localStorage.setItem("refreshToken", refreshToken);
    showDashboard();
  } else {
    loginError.classList.remove("hidden");
  }
};

logoutBtn.onclick = () => logout();

function logout() {
  localStorage.clear();
  location.reload();
}

function appendOutput(msg) {
  output.innerHTML += `<div>${msg}</div>`;
  output.scrollTop = output.scrollHeight;
}

async function updateMetrics() {
  const data = await api("/app/metrics");
  if (!data) return;
  document.getElementById("cpuPercent").innerText = data.cpu_percent + "%";
  document.getElementById("cpuFreq").innerText = data.cpu_freq.toFixed(0) + " MHz";
  document.getElementById("memPercent").innerText = data.memory_percent + "%";
  document.getElementById("diskPercent").innerText = data.disk_percent + "%";
  document.getElementById("uploadSpeed").innerText = (data.upload_speed / 1024).toFixed(1) + " KB/s";
  document.getElementById("downloadSpeed").innerText = (data.download_speed / 1024).toFixed(1) + " KB/s";

  chart.data.labels.push(data.timestamp);
  chart.data.datasets[0].data.push(data.cpu_percent);
  chart.data.datasets[1].data.push(data.memory_percent);
  chart.data.datasets[2].data.push((data.upload_speed / 1024).toFixed(1));
  chart.data.datasets[3].data.push((data.download_speed / 1024).toFixed(1));

  if (chart.data.labels.length > 30) {
    chart.data.labels.shift();
    chart.data.datasets.forEach(ds => ds.data.shift());
  }
  chart.update();
  appendOutput(`[${data.timestamp}] CPU ${data.cpu_percent}%, MEM ${data.memory_percent}%, NET ${(data.download_speed / 1024).toFixed(1)} KB/s`);
}

function showDashboard() {
  loginPage.classList.add("hidden");
  dashboard.classList.remove("hidden");
  appendOutput("✅ 登录成功，开始获取系统监控数据...");
  setInterval(updateMetrics, 2000);
}

if (accessToken) showDashboard();
