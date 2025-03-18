const API_BASE_URL = "https://stock-trading-system-production.up.railway.app/api/";  // Set backend API URL

document.addEventListener("DOMContentLoaded", function() {
    fetch(`${API_BASE_URL}stocks/`)  // Fetch stock data
        .then(response => response.json())
        .then(data => {
            let stockList = "";
            data.forEach(stock => {
                stockList += `<tr>
                    <td>${stock.company_name}</td>
                    <td>${stock.ticker}</td>
                    <td>$${stock.price.toFixed(2)}</td>
                    <td>${stock.volume}</td>
                    <td><button onclick="deleteStock('${stock.ticker}')">Delete</button></td>
                </tr>`;
            });
            document.getElementById("admin-stock-list").innerHTML = stockList;
        })
        .catch(error => console.error("Error fetching stocks:", error));
});

function deleteStock(ticker) {
    fetch(`${API_BASE_URL}stocks/delete/${ticker}/`, {  // Uses dynamic API URL
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload(); // Refreshes page after deletion
    })
    .catch(error => console.error("Error deleting stock:", error));
}
