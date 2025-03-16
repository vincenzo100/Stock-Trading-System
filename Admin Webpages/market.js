document.addEventListener("DOMContentLoaded", function() {
    // Fetch existing market hours when page loads
    fetch("https://stock-trading-system-production.up.railway.app/api/market-hours/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("startTime").value = data.start_time;
            document.getElementById("endTime").value = data.end_time;
        })
        .catch(error => console.error("Error fetching market hours:", error));
});

function updateMarketHours() {
    const startTime = document.getElementById("startTime").value;
    const endTime = document.getElementById("endTime").value;

    fetch("https://stock-trading-system-production.up.railway.app/api/market-hours/", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start_time: startTime, end_time: endTime })
    })
    .then(response => response.json())
    .then(data => alert("Market hours updated successfully!"))
    .catch(error => console.error("Error updating market hours:", error));
}

function toggleMarketDay(day) {
    alert(`Market availability toggled for ${day}`); 
}
