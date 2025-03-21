# Standard Django & DRF imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Delay importing models & serializers to prevent circular imports
Stock = None
Portfolio = None
PortfolioStock = None
Transaction = None
StockSerializer = None

def import_models():
    """ Dynamically imports models to prevent circular imports """
    global Stock, Portfolio, PortfolioStock, Transaction
    from .models import Stock, Portfolio, PortfolioStock, Transaction

def import_serializers():
    """ Dynamically imports serializers to prevent circular imports """
    global StockSerializer
    from .serializers import StockSerializer

# User Registration (Fixes Circular Import)
@api_view(['POST'])
def register_user(request):
    """ Registers a new user and creates their portfolio """
    import_models()  
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

# User Login (Fixes Circular Import)
@api_view(['POST'])
def login_user(request):
    """ Authenticates a user and returns a success message """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    user = authenticate(username=username, password=password)

    if user:
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'error': 'Invalid credentials'}, status=400)

# Get All Stocks
@api_view(['GET'])
def list_stocks(request):
    """ Retrieves all stocks from the database """
    import_models()  
    stocks = Stock.objects.all()
    import_serializers()  
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)

# Get a Single Stock by Ticker
@api_view(['GET'])
def get_stock(request, ticker):
    """ Retrieves a stock by ticker symbol """
    import_models()  
    stock = get_object_or_404(Stock, ticker=ticker)
    import_serializers()  
    serializer = StockSerializer(stock)
    return Response(serializer.data)

# Buy Stocks
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_stock(request):
    """ Allows users to buy stocks. """
    import_models()  

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
    """ Allows users to sell stocks from their portfolio. """
    import_models()  

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


