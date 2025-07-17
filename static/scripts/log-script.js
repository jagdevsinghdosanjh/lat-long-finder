window.addEventListener("load", () => {
  const userAgent = navigator.userAgent;
  const platform = navigator.platform || "Unknown";

  function sendLog(locationStr) {
    fetch("/log-access", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        agent: userAgent,
        platform: platform,
        location: locationStr
      })
    });
  }

  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude.toFixed(5);
        const lng = pos.coords.longitude.toFixed(5);
        sendLog(`${lat},${lng}`);
      },
      () => sendLog("Permission denied")
    );
  } else {
    sendLog("Not supported");
  }
});



// window.addEventListener("load", () => {
//   const userAgent = navigator.userAgent;
//   const platform = navigator.platform || "Unknown";

//   function sendLog(locationStr) {
//     fetch("/log-access", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({
//         agent: userAgent,
//         location: locationStr,
//         platform: platform
//       })
//     });
//   }

//   if ("geolocation" in navigator) {
//     navigator.geolocation.getCurrentPosition(
//       (pos) => {
//         const lat = pos.coords.latitude.toFixed(5);
//         const lng = pos.coords.longitude.toFixed(5);
//         sendLog(`${lat},${lng}`);
//       },
//       () => sendLog("Permission denied")
//     );
//   } else {
//     sendLog("Geolocation not supported");
//   }
// });
