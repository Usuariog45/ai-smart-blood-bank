const API = "http://127.0.0.1:8000";

function openTab(id) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}

// 🔍 FIND BLOOD — WORKING
async function searchBlood() {
  const bloodGroup = encodeURIComponent(
  document.getElementById("blood_group").value
);
  const lat = document.getElementById("lat").value;
  const lng = document.getElementById("lng").value;

  const resultBox = document.getElementById("searchResult");
  resultBox.innerHTML = "Loading...";

  try {
    const res = await fetch(
      `${API}/blood/search?blood_group=${bloodGroup}&lat=${lat}&lng=${lng}&radius_km=10`
    );
    const data = await res.json();

    if (!data.length) {
      resultBox.innerHTML = "<p>No blood banks found</p>";
      return;
    }

    let html = `
      <table border="1" cellpadding="10">
        <tr>
          <th>Blood Bank</th>
          <th>Group</th>
          <th>Units</th>
          <th>Distance (km)</th>
        </tr>
    `;

    data.forEach(row => {
      html += `
        <tr>
          <td>${row.blood_bank_name}</td>
          <td>${row.blood_group}</td>
          <td>${row.units_available}</td>
          <td>${row.distance_km.toFixed(2)}</td>
        </tr>
      `;
    });

    html += "</table>";
    resultBox.innerHTML = html;

  } catch (err) {
    console.error(err);
    resultBox.innerHTML = "<p style='color:red'>Error fetching data</p>";
  }
}

// 👤 DONOR
async function registerDonor() {
  const payload = {
    name: donor_name.value.trim(),
    phone: donor_phone.value.trim(),
    blood_group: donor_group.value,
    city: donor_city.value.trim(),
    latitude: parseFloat(donor_lat.value),
    longitude: parseFloat(donor_lng.value)
  };

  // Basic validation
  if (
    !payload.name ||
    !/^\d{10}$/.test(payload.phone) ||
    !payload.city ||
    isNaN(payload.latitude) ||
    isNaN(payload.longitude)
  ) {
    donorMsg.innerText = "Please fill all fields correctly";
    return;
  }

  try {
    const res = await fetch(`${API}/donors/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.text();
      donorMsg.innerText = "❌ " + err;
      return;
    }

    donorMsg.innerText = "Registered successfully!";
  } catch (e) {
    donorMsg.innerText = " Server error";
  }
}


// CAMPS
async function loadCamps() {
  const res = await fetch(`${API}/camps/`);
  const data = await res.json();
  campTable.classList.remove("hidden");
  campTable.innerHTML = data.map(c =>
    `<tr><td>${c.name}</td><td>${c.location}</td><td>${c.date}</td></tr>`
  ).join("");
}

// ANALYTICS
async function loadAnalytics() {
  const res = await fetch(`${API}/analytics/inventory`);
  const data = await res.json();
  analyticsTable.classList.remove("hidden");
  analyticsTable.innerHTML = data.map(a =>
    `<tr><td>${a.blood_group}</td><td>${a.total_units}</td></tr>`
  ).join("");
}

async function loadLowStock() {
  const res = await fetch(`${API}/analytics/low-stock`);
  const data = await res.json();
  analyticsTable.classList.remove("hidden");
  analyticsTable.innerHTML = data.map(a =>
    `<tr><td>${a.blood_group}</td><td>${a.units_available}</td></tr>`
  ).join("");
}

// LOGS
async function loadLogs() {
  const res = await fetch(`${API}/inventory/logs`);
  const data = await res.json();
  logsTable.classList.remove("hidden");
  logsTable.innerHTML = data.map(l =>
    `<tr><td>${l.blood_group}</td><td>${l.change_type}</td><td>${l.units_changed}</td><td>${l.created_at}</td></tr>`
  ).join("");
}

// 🧠 AI PRIORITY DONORS
async function loadPriorityDonors() {
  const bg = document.getElementById("priority_group").value;
  const lat = document.getElementById("priority_lat").value;
  const lng = document.getElementById("priority_lng").value;

  const box = document.getElementById("priorityResult");
  box.innerHTML = "Loading AI-ranked donors...";

  try {
    const res = await fetch(
      `${API}/donors/priority?blood_group=${bg}&lat=${lat}&lng=${lng}`
    );
    const data = await res.json();

    if (!data.length) {
      box.innerHTML = "No donors found";
      return;
    }

    let html = `
      <table border="1" cellpadding="8">
        <tr>
          <th>Name</th>
          <th>Blood</th>
          <th>City</th>
          <th>Distance (km)</th>
          <th>AI Score</th>
        </tr>
    `;

    data.forEach(d => {
      html += `
        <tr>
          <td>${d.name}</td>
          <td>${d.blood_group}</td>
          <td>${d.city}</td>
          <td>${d.distance_km}</td>
          <td>${d.priority_score}</td>
        </tr>
      `;
    });

    html += "</table>";
    box.innerHTML = html;

  } catch (e) {
    box.innerHTML = "AI service unavailable";
  }
}
