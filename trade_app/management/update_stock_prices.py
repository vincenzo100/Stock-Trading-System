import random
from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)  # Track last price update

    def update_price(self):
        """ Randomly increase or decrease the stock price within a small range. """
        price_change = random.uniform(-2.0, 2.0)  # Adjust price between -2.0 and +2.0
        new_price = max(1.0, self.price + price_change)  # Prevent negative prices
        self.price = round(new_price, 2)
        self.save()
