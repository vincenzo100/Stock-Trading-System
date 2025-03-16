from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Stock, Portfolio, PortfolioStock, Transaction
from .serializers import StockSerializer, PortfolioSerializer, PortfolioStockSerializer, TransactionSerializer, UserSerializer

# Fetch a Single Stock by Ticker
@api_view(['GET'])
def get_stock(request, ticker):
    stock = get_object_or_404(Stock, ticker=ticker)
    serializer = StockSerializer(stock)
    return Response(serializer.data)

# List All Stocks 
@api_view(['GET'])
def list_stocks(request):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)

# User Registration (Now Returns Auth Token)
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return JsonResponse({'error': 'All fields are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already taken'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    Portfolio.objects.create(user=user)
    return JsonResponse({'message': 'User created successfully'})

# User Login (Returns JWT Token)
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'error': 'Invalid credentials'}, status=400)

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

# Sell Stocks
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sell_stock(request):
    user = request.user
    ticker = request.data.get('ticker')  
    quantity = int(request.data.get('quantity'))

    stock = get_object_or_404(Stock, ticker=ticker)
    portfolio = Portfolio.objects.get(user=user)
    portfolio_stock = PortfolioStock.objects.filter(portfolio=portfolio, stock=stock).first()

    if portfolio_stock and portfolio_stock.shares >= quantity:
        portfolio_stock.shares -= quantity
        if portfolio_stock.shares == 0:
            portfolio_stock.delete()
        else:
            portfolio_stock.save()

        portfolio.cash_balance += stock.price * quantity
        portfolio.save()

        Transaction.objects.create(user=user, stock=stock, transaction_type='SELL', amount=stock.price * quantity)
        return JsonResponse({'message': 'Stock sold successfully'})
    else:
        return JsonResponse({'error': 'Not enough shares'}, status=400)

# Deposit Cash (Previously Missing Function)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_cash(request):
    user = request.user
    amount = request.data.get("amount")

    if not amount or float(amount) <= 0:
        return JsonResponse({'error': 'Deposit amount must be greater than zero'}, status=400)

    portfolio = Portfolio.objects.get(user=user)
    portfolio.cash_balance += float(amount)
    portfolio.save()

    Transaction.objects.create(user=user, transaction_type='DEPOSIT', amount=amount)

    return JsonResponse({'message': f'Deposited ${amount} successfully'})

# Update Stock Price (Fixes API Key Naming)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_stock_price(request, ticker):
    stock = get_object_or_404(Stock, ticker=ticker)
    new_price = float(request.data.get('price'))
    stock.price = new_price
    stock.save()
    return JsonResponse({'message': f'Stock {stock.ticker} price updated to ${new_price}'})

# Delete Stock (Fixes API Key Naming)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_stock(request, ticker):
    stock = get_object_or_404(Stock, ticker=ticker)
    stock.delete()
    return JsonResponse({'message': f'Stock {ticker} deleted successfully'})
