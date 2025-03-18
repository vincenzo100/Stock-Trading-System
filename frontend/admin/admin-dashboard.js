const API_BASE_URL = "https://stock-trading-system-production.up.railway.app/api/";  // Backend URL defined once

document.addEventListener("DOMContentLoaded", function() {
    fetch(`${API_BASE_URL}stocks/`)  // Uses base URL dynamically
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            return response.json();
        })
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
    fetch(`${API_BASE_URL}stocks/delete/${ticker}/`, {  // Uses base URL dynamically
        method: "DELETE"
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        alert(data.message);
        location.reload(); // Refreshes the page after deleting a stock
    })
    .catch(error => console.error("Error deleting stock:", error));
}
