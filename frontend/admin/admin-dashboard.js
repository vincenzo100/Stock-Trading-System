document.addEventListener("DOMContentLoaded", function() {
    // Fetch all stocks from Django backend when the page loads
    fetch("https://stock-trading-system-production.up.railway.app/api/stocks/")
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

// Function to delete a stock using Django API
function deleteStock(ticker) {
    fetch(`https://stock-trading-system-production.up.railway.app/api/stocks/delete/${ticker}/`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error("Error deleting stock:", error));
}