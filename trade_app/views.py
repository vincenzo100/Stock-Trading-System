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
    stock = get_object_or_404(Stock, ticker=ticker)  # Prevents 404 issues
    serializer = StockSerializer(stock)
    return Response(serializer.data)

# List All Stocks (Now Updates Prices Before Sending to Frontend)
@api_view(['GET'])
def list_stocks(request):
    stocks = Stock.objects.all()
    for stock in stocks:
        stock.update_price()  # Update stock prices before sending to frontend
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)

# User Registration
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already taken'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    Portfolio.objects.create(user=user)  # Create portfolio for new user
    return JsonResponse({'message': 'User created successfully'})

# User Login
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
    stock_ticker = request.data.get('stock_ticker')
    quantity = int(request.data.get('quantity'))

    stock = get_object_or_404(Stock, ticker=stock_ticker)

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
    stock_ticker = request.data.get('stock_ticker')
    quantity = int(request.data.get('quantity'))

    stock = get_object_or_404(Stock, ticker=stock_ticker)
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

# Deposit Cash
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_cash(request):
    user = request.user
    amount = float(request.data.get('amount'))

    if amount <= 0:
        return JsonResponse({'error': 'Deposit amount must be greater than zero'}, status=400)

    portfolio = Portfolio.objects.get(user=user)
    portfolio.cash_balance += amount
    portfolio.save()

    Transaction.objects.create(user=user, transaction_type='DEPOSIT', amount=amount)

    return JsonResponse({'message': f'Deposited ${amount} successfully'})

# Withdraw Cash
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_cash(request):
    user = request.user
    amount = float(request.data.get('amount'))
    portfolio = Portfolio.objects.get(user=user)

    if amount <= 0:
        return JsonResponse({'error': 'Withdrawal amount must be greater than zero'}, status=400)
    if portfolio.cash_balance < amount:
        return JsonResponse({'error': 'Insufficient funds'}, status=400)

    portfolio.cash_balance -= amount
    portfolio.save()

    Transaction.objects.create(user=user, transaction_type='WITHDRAW', amount=amount)

    return JsonResponse({'message': f'Withdrew ${amount} successfully'})

# Add New Stock (Admin Only)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_stock(request):
    ticker = request.data.get('ticker')
    company_name = request.data.get('company_name')
    price = float(request.data.get('price'))
    volume = int(request.data.get('volume'))

    if Stock.objects.filter(ticker=ticker).exists():
        return JsonResponse({'error': 'Stock ticker already exists'}, status=400)

    stock = Stock.objects.create(ticker=ticker, company_name=company_name, price=price, volume=volume)
    return JsonResponse({'message': f'Stock {stock.ticker} added successfully'})

# Update Stock Price (Admin Only)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_stock_price(request, ticker):
    stock = get_object_or_404(Stock, ticker=ticker)
    new_price = float(request.data.get('price'))
    stock.price = new_price
    stock.save()

    return JsonResponse({'message': f'Stock {stock.ticker} price updated to ${new_price}'})

#  Delete Stock (Admin Only)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_stock(request, ticker):
    stock = get_object_or_404(Stock, ticker=ticker)
    stock.delete()
    return JsonResponse({'message': f'Stock {ticker} deleted successfully'})


