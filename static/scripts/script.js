// Main script logic
// static/scripts/script.js
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(sendPosition, showError);
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}

function sendPosition(position) {
  fetch("/geo", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      latitude: position.coords.latitude,
      longitude: position.coords.longitude
    })
  })
  .then(response => response.json())
  .then(data => {
    alert(`Your location: Lat ${data.latitude}, Long ${data.longitude}`);
  });
}

function showError(error) {
  alert("Error getting location: " + error.message);
}
