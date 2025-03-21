from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  

def home(request):
    """ Displays a simple homepage message for the API root """
    return HttpResponse("<h1>Welcome to the Stock Trading System API</h1>")

urlpatterns = [
    path('', home),  # Default API Home Route
    path('admin/', admin.site.urls),  # Admin Panel
    path('api/', include('trade_app.urls')),  # Includes API routes from trade_app
    path('', include('stock_trading.urls')), #KEA 03/20/2025 - needed to display webpages
]

# Debugging Check: Ensure `trade_app.urls` is correctly loaded
try:
    import trade_app.urls
except ImportError as e:
    raise ImportError(f"Error importing trade_app.urls: {e}")
