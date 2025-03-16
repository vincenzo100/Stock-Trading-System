from django.urls import path

# Delay import of views to avoid circular imports
views = __import__("trade_app.views", fromlist=["register_user", "login_user"])

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("stocks/", views.list_stocks, name="list_stocks"),
    path("stocks/<str:ticker>/", views.get_stock, name="get_stock"),
    path("buy/", views.buy_stock, name="buy_stock"),
    path("sell/", views.sell_stock, name="sell_stock"),
    path("deposit/", views.deposit_cash, name="deposit_cash"),
    path("withdraw/", views.withdraw_cash, name="withdraw_cash"),
    path("stocks/add/", views.add_stock, name="add_stock"),
    path("stocks/update/<str:ticker>/", views.update_stock_price, name="update_stock_price"),
    path("stocks/delete/<str:ticker>/", views.delete_stock, name="delete_stock"),
]
