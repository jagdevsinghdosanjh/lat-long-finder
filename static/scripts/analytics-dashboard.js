function filterLogs() {
  const start = document.getElementById("startDate").value;
  const end = document.getElementById("endDate").value;

  fetch("/get-access-log-json")
    .then(res => res.json())
    .then(data => {
      let filtered = data;
      if (start && end) {
        filtered = data.filter(entry => {
          const date = new Date(entry.timestamp);
          return date >= new Date(start) && date <= new Date(end);
        });
      }

      const platformCount = {};
      const browserCount = {};

      filtered.forEach(entry => {
        const platform = entry.platform || "Unknown";
        const browser = parseBrowser(entry.agent);

        platformCount[platform] = (platformCount[platform] || 0) + 1;
        browserCount[browser] = (browserCount[browser] || 0) + 1;
      });

      updateChart("platformChart", platformCount, "Platform Usage", "bar");
      updateChart("browserChart", browserCount, "Browser Types", "pie");
    });
}

function updateChart(canvasId, data, label, type) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  new Chart(ctx, {
    type: type,
    data: {
      labels: Object.keys(data),
      datasets: [{
        label: label,
        data: Object.values(data),
        backgroundColor: ['#4ca1af', '#007BFF', '#74ebd5', '#ff6b6b', '#ffd700']
      }]
    }
  });
}

function parseBrowser(userAgent) {
  if (userAgent.includes("Chrome")) return "Chrome";
  if (userAgent.includes("Firefox")) return "Firefox";
  if (userAgent.includes("Safari") && !userAgent.includes("Chrome")) return "Safari";
  if (userAgent.includes("Edge")) return "Edge";
  return "Other";
}
