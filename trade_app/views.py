from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Stock, Portfolio, PortfolioStock, Transaction
from .serializers import StockSerializer, PortfolioSerializer, PortfolioStockSerializer, TransactionSerializer, UserSerializer

# Debugging: Ensure models are properly imported
try:
    from .models import Stock, Portfolio
except ImportError as e:
    raise ImportError(f"Error importing models: {e}")

# User Registration
@api_view(['POST'])
def register_user(request):
    """
    Allows a new user to register an account.
    Ensures username, email, and password are provided.
    Returns an error if the username is already taken.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return JsonResponse({'error': 'All fields are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already taken'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    Portfolio.objects.create(user=user)  # Automatically create a portfolio for new users
    return JsonResponse({'message': 'User created successfully'})

# User Login
@api_view(['POST'])
def login_user(request):
    """
    Authenticates user login credentials.
    Returns a success message if authentication is successful.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    user = authenticate(username=username, password=password)

    if user:
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'error': 'Invalid credentials'}, status=400)

# List All Stocks
@api_view(['GET'])
def list_stocks(request):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)

# Fetch a Single Stock by Ticker
@api_view(['GET'])
def get_stock(request, ticker):
    stock = get_object_or_404(Stock, ticker=ticker)
    serializer = StockSerializer(stock)
    return Response(serializer.data)

# Buy Stocks
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_stock(request):
    user = request.user
    ticker = request.data.get('ticker')
    quantity = int(request.data.get('quantity'))

    stock = get_object_or_404(Stock, ticker=ticker)

    total_price = stock.price * quantity
    portfolio = Portfolio.objects.get(user=user)

    if portfolio.cash_balance >= total_price:
        portfolio.cash_balance -= total_price
        portfolio.save()

        portfolio_stock, created = PortfolioStock.objects.get_or_create(portfolio=portfolio, stock=stock)
        portfolio_stock.shares += quantity
        portfolio_stock.save()

        Transaction.objects.create(user=user, stock=stock, transaction_type='BUY', amount=total_price)
        return JsonResponse({'message': 'Stock purchased successfully'})
    else:
        return JsonResponse({'error': 'Insufficient funds'}, status=400)

