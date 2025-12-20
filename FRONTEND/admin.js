const API = "http://127.0.0.1:8000";

/* ================== HELPERS ================== */
function getToken() {
  return localStorage.getItem("admin_token");
}

function authHeaders() {
  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${getToken()}`
  };
}

/* ================== UI ================== */
function showTab(tab) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.getElementById(tab).classList.add("active");
}

function showLogin() {
  document.getElementById("loginBox").style.display = "block";
  document.getElementById("adminPanel").style.display = "none";
}

function showAdmin() {
  document.getElementById("loginBox").style.display = "none";
  document.getElementById("adminPanel").style.display = "block";
}

/* ================== LOGIN ================== */
document.getElementById("loginBtn").addEventListener("click", loginAdmin);

function loginAdmin() {
  const u = document.getElementById("adminUser").value.trim();
  const p = document.getElementById("adminPass").value.trim();
  const err = document.getElementById("loginError");

  if (!u || !p) {
    err.innerText = "Username and password required";
    return;
  }

  fetch(`${API}/admin/login?username=${encodeURIComponent(u)}&password=${encodeURIComponent(p)}`, {
    method: "POST"
  })
  .then(res => {
    if (!res.ok) throw new Error("Invalid credentials");
    return res.json();
  })
  .then(data => {
    localStorage.setItem("admin_token", data.access_token);
    location.reload();
  })
  .catch(() => {
    err.innerText = "Invalid username or password";
  });
}

/* ================== AUTH CHECK ================== */
function checkAuth() {
  const token = getToken();
  if (!token) {
    showLogin();
    return;
  }

  fetch(`${API}/admin/dashboard`, {
    headers: authHeaders()
  })
  .then(res => {
    if (!res.ok) throw new Error();
    showAdmin();
    loadAllAdminData();
  })
  .catch(() => {
    localStorage.removeItem("admin_token");
    showLogin();
  });
}

/* ================== DATA LOADERS ================== */
function loadAllAdminData() {
  loadBloodBanks();
  loadInventory();
  loadCamps();
  loadLogs();
}

function loadBloodBanks() {
  fetch(`${API}/admin/blood-banks`, { headers: authHeaders() })
    .then(res => res.json())
    .then(data => renderTable("banksTable", data));
}

function loadInventory() {
  fetch(`${API}/admin/inventory`, { headers: authHeaders() })
    .then(res => res.json())
    .then(data => renderTable("inventoryTable", data));
}

function loadCamps() {
  fetch(`${API}/admin/camps`, { headers: authHeaders() })
    .then(res => res.json())
    .then(data => renderTable("campsTable", data));
}

function loadLogs() {
  fetch(`${API}/admin/inventory/logs`, { headers: authHeaders() })
    .then(res => res.json())
    .then(data => renderTable("logsTable", data));
}

/* ================== TABLE ================== */
function renderTable(id, data) {
  const table = document.getElementById(id);
  if (!data || data.length === 0) {
    table.innerHTML = "<tr><td>No data</td></tr>";
    return;
  }

  const headers = Object.keys(data[0]);
  table.innerHTML = `
    <tr>${headers.map(h => `<th>${h}</th>`).join("")}</tr>
    ${data.map(row =>
      `<tr>${headers.map(h => `<td>${row[h]}</td>`).join("")}</tr>`
    ).join("")}
  `;
}

/* ================== INIT ================== */
checkAuth();
