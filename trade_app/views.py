from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Stock, Portfolio, PortfolioStock, Transaction
from .serializers import StockSerializer, PortfolioSerializer, PortfolioStockSerializer, TransactionSerializer, UserSerializer

# Debugging to detect circular imports
try:
    from .views import login_user
except ImportError as e:
    raise ImportError(f"Error importing login_user: {e}")

# User Login 
@api_view(['POST'])
def login_user(request):
    """
    ✅ Allows a user to log in.
    ✅ Authenticates username and password.
    ✅ Returns a success message if authentication is successful.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    user = authenticate(username=username, password=password)

    if user:
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'error': 'Invalid credentials'}, status=400)
