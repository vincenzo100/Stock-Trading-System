const API_BASE_URL = "https://stock-trading-system-production.up.railway.app/api/";  // Backend API URL

document.addEventListener("DOMContentLoaded", function() {
    fetch(`${API_BASE_URL}transactions/`)  // Uses base URL dynamically
        .then(response => response.json())
        .then(data => {
            let transactionList = "";
            if (data.length === 0) {
                document.getElementById("no-transactions").style.display = "block"; // Show message if empty
            } else {
                data.forEach(transaction => {
                    transactionList += `<tr>
                        <td>${transaction.ticker}</td>
                        <td>${transaction.transaction_type}</td>
                        <td>${transaction.quantity}</td>
                        <td>$${transaction.price_at_transaction.toFixed(2)}</td>
                        <td>${new Date(transaction.date).toLocaleDateString()}</td>
                    </tr>`;
                });
                document.getElementById("transaction-list").innerHTML = transactionList;
            }
        })
        .catch(error => console.error("Error fetching transactions:", error));
});