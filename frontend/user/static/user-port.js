const API_BASE_URL = "https://stock-trading-system-production.up.railway.app/api/";  // Backend API URL

document.addEventListener("DOMContentLoaded", function() {
    fetch(`${API_BASE_URL}portfolio/`)  // Uses base URL dynamically
        .then(response => response.json())
        .then(data => {
            let portfolioList = "";
            if (data.length === 0) {
                document.getElementById("no-stocks").style.display = "block"; // Show message if empty
            } else {
                data.forEach(stock => {
                    let totalValue = stock.quantity * stock.current_price;
                    portfolioList += `<tr>
                        <td>${stock.ticker}</td>
                        <td>${stock.quantity}</td>
                        <td>$${stock.current_price.toFixed(2)}</td>
                        <td>$${totalValue.toFixed(2)}</td>
                    </tr>`;
                });
                document.getElementById("portfolio-list").innerHTML = portfolioList;
            }
        })
        .catch(error => console.error("Error fetching portfolio:", error));
});