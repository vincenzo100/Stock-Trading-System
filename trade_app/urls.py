from django.urls import path
from .views import (
    register_user, login_user, list_stocks, get_stock, buy_stock, sell_stock, 
    deposit_cash, withdraw_cash, add_stock, update_stock_price, delete_stock
)

urlpatterns = [
    # User Authentication Endpoints
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),

    # Stock Listings & Trading Endpoints
    path("stocks/", list_stocks, name="list_stocks"),
    path("stocks/<str:ticker>/", get_stock, name="get_stock"),
    path("buy/", buy_stock, name="buy_stock"),
    path("sell/", sell_stock, name="sell_stock"),

    # User Account Transactions
    path("deposit/", deposit_cash, name="deposit_cash"),
    path("withdraw/", withdraw_cash, name="withdraw_cash"),

    # Admin Stock Management
    path("stocks/add/", add_stock, name="add_stock"),
    path("stocks/update/<str:ticker>/", update_stock_price, name="update_stock_price"),
    path("stocks/delete/<str:ticker>/", delete_stock, name="delete_stock"),
]

# Debugging: Ensure all views are properly imported
try:
    from .views import register_user, login_user
except ImportError as e:
    raise ImportError(f"Error importing views: {e}")
