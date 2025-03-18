const API_BASE_URL = "https://stock-trading-system-production.up.railway.app/api/";  // Backend URL defined once

document.addEventListener("DOMContentLoaded", function() {
    fetch(`${API_BASE_URL}market-hours/`)  // Uses base URL dynamically
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            const startTimeInput = document.getElementById("startTime");
            const endTimeInput = document.getElementById("endTime");
            if (startTimeInput && endTimeInput) {
                startTimeInput.value = data.start_time;
                endTimeInput.value = data.end_time;
            }
        })
        .catch(error => console.error("Error fetching market hours:", error));
});

function updateMarketHours() {
    const startTimeInput = document.getElementById("startTime");
    const endTimeInput = document.getElementById("endTime");

    if (!startTimeInput || !endTimeInput) {
        console.error("Market hour input elements not found.");
        return;
    }

    const startTime = startTimeInput.value;
    const endTime = endTimeInput.value;

    fetch(`${API_BASE_URL}market-hours/`, {  // Uses base URL dynamically
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start_time: startTime, end_time: endTime })
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
    })
    .then(data => alert("Market hours updated successfully!"))
    .catch(error => console.error("Error updating market hours:", error));
}
