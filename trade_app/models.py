from decimal import Decimal
import random
from django.db import models
from django.contrib.auth.models import User


# Ensure Django uses the correct table name in MySQL
class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)  # Fix: Ensures last_updated is always set

    class Meta:
        db_table = "stocks"  #  Ensure Django uses "stocks" table in MySQL

    def update_price(self):
        """ Randomly increase or decrease the stock price within a small range. """
        price_change = Decimal(str(random.uniform(-2.0, 2.0)))  # Convert float to Decimal
        new_price = max(Decimal('1.00'), self.price + price_change)  # Prevents negative price
        self.price = new_price.quantize(Decimal('0.01'))  # Rounds to 2 decimal places
        self.save()

    def __str__(self):
        return f"{self.company_name} ({self.ticker})"


# User Portfolio - Tracks cash balance & stocks owned
class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        db_table = "portfolios"  # Ensure Django uses "portfolios"

    def __str__(self):
        return f"Portfolio of {self.user.username}"


# Tracks stocks within a user's portfolio
class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.PositiveIntegerField()

    class Meta:
        db_table = "portfolio_stocks"  #  Ensure Django uses "portfolio_stocks"

    def __str__(self):
        return f"{self.shares} shares of {self.stock.ticker} in {self.portfolio.user.username}'s portfolio"


# Tracks all transactions (Buy, Sell, Deposit, Withdraw)
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
    timestamp = models.DateTimeField(auto_now_add=True)  # Ensures transactions are timestamped

    class Meta:
        db_table = "transactions"  #  Ensure Django uses "transactions"

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} by {self.user.username}"
