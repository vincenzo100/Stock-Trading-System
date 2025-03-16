from django.urls import path
from .views import (
    register_user, login_user, list_stocks, get_stock, buy_stock, sell_stock, 
    deposit_cash, withdraw_cash, add_stock, update_stock_price, delete_stock
)

urlpatterns = [
    # User Authentication Endpoints
    path("api/register/", register_user, name="register"),
    path("api/login/", login_user, name="login"),

    # Stock Listings & Trading Endpoints
    path("api/stocks/", list_stocks, name="list_stocks"),  
    path("api/stocks/<str:ticker>/", get_stock, name="get_stock"),  # Fetch single stock
    path("api/buy/", buy_stock, name="buy_stock"),
    path("api/sell/", sell_stock, name="sell_stock"),

    # User Account Transactions
    path("api/deposit/", deposit_cash, name="deposit_cash"),
    path("api/withdraw/", withdraw_cash, name="withdraw_cash"),

    # Admin Stock Management
    path("api/stocks/add/", add_stock, name="add_stock"),
    path("api/stocks/update/<str:ticker>/", update_stock_price, name="update_stock_price"),
    path("api/stocks/delete/<str:ticker>/", delete_stock, name="delete_stock"),
]

