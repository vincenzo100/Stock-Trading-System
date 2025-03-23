const API_BASE_URL = "https://stock-trading-system-production.up.railway.app/api/";  // Backend API URL

// Listens for deposit/withdraw transactions
document.getElementById("cashForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const amount = document.getElementById("amount").value;
    const action = document.getElementById("action").value;

    fetch(`${API_BASE_URL}${action}/`, {  // Uses dynamic API URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount: parseFloat(amount) })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById("cashForm").reset();  // Clears form after submission
    })
    .catch(error => console.error("Error processing transaction:", error));
});
