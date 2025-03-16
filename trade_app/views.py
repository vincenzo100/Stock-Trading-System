from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Stock, Portfolio, PortfolioStock, Transaction
from .serializers import StockSerializer, PortfolioSerializer, PortfolioStockSerializer, TransactionSerializer, UserSerializer

# Sell Stocks 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sell_stock(request):
    """
    Allows users to sell stocks from their portfolio.
    Ensures user owns enough shares before selling.
    Updates portfolio and transaction records.
    """
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
