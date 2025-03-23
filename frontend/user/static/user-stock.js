const API_BASE_URL = "https://stock-trading-system-production.up.railway.app/api/";  // Backend API URL

document.addEventListener("DOMContentLoaded", function() {
    fetch(`${API_BASE_URL}stocks/`)  // Uses base URL dynamically
        .then(response => response.json())
        .then(data => {
            let stocksList = "";
            if (data.length === 0) {
                document.getElementById("no-stocks").style.display = "block"; // Show message if empty
            } else {
                data.forEach(stock => {
                    stocksList += `<tr>
                        <td>${stock.company_name}</td>
                        <td>${stock.ticker}</td>
                        <td>$${stock.price.toFixed(2)}</td>
                        <td>${stock.volume}</td>
                    </tr>`;
                });
                document.getElementById("stocks-list").innerHTML = stocksList;
            }
        })
        .catch(error => console.error("Error fetching stocks:", error));
});