const API_BASE_URL = "https://stock-trading-system-production.up.railway.app/api/";  // Define API base URL

// Listen for form submission to send data to Django API
document.getElementById("stockForm").addEventListener("stockFormSubmit", function(event) {
    event.preventDefault();
    
    const company = document.getElementById("company").value;
    const ticker = document.getElementById("ticker").value;
    const initialPrice = document.getElementById("initial").value;

    fetch(`${API_BASE_URL}stocks/add/`, {  // Uses base URL dynamically
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            company_name: company,
            ticker: ticker,
            price: parseFloat(initialPrice),
            volume: 1000
        })
    })
    .then(response => response.json())
    .then(data => {
        alert("Stock added successfully!");
        document.getElementById("stockForm").reset();  // Clears form after submission
    })
    .catch(error => console.error("Error adding stock:", error));
});