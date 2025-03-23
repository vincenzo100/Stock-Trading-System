const API_BASE_URL = "https://stock-trading-system-production.up.railway.app/api/";  // Backend API URL

// Listens for trade form submission
document.getElementById("tradeForm").addEventListener("tradeFormSubmit", function(event) {
    event.preventDefault();

    const ticker = document.getElementById("ticker").value;
    const action = document.getElementById("action").value;
    const shares = document.getElementById("shares").value;

    fetch(`${API_BASE_URL}${action}/`, {  // Uses dynamic API URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            ticker: ticker,
            quantity: parseInt(shares)
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById("tradeForm").reset();  // Clears form after submission
    })
    .catch(error => console.error("Error processing trade:", error));
});
