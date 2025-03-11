import random
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal  # Import Decimal to handle price calculations

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)  # Track last price update  

    def update_price(self):
        """ Randomly increase or decrease the stock price within a small range. """
        price_change = Decimal(str(random.uniform(-2.0, 2.0)))  
        new_price = max(Decimal("1.0"), self.price + price_change)  
        self.price = new_price.quantize(Decimal("0.01"))  
        self.save()

    def __str__(self):
        return f"{self.company_name} ({self.ticker})"

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return f"Portfolio of {self.user.username}"

class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.shares} shares of {self.stock.ticker} in {self.portfolio.user.username}'s portfolio"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} by {self.user.username}"

