from django.urls import path
from . import views #KEA 03/20/2025

# Lazy Imports to Prevent Circular Dependencies
views = __import__("trade_app.views", fromlist=[
    "register_user", "login_user", "list_stocks", "get_stock", 
    "buy_stock", "sell_stock", "deposit_cash", "withdraw_cash", 
    "add_stock", "update_stock_price", "delete_stock"
])

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("stocks/", views.list_stocks, name="list_stocks"),
    path("stocks/<str:ticker>/", views.get_stock, name="get_stock"),
    path("buy/", views.buy_stock, name="buy_stock"),
    path("sell/", views.sell_stock, name="sell_stock"),
]
