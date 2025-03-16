from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Stock, Portfolio, PortfolioStock, Transaction
from .serializers import StockSerializer, PortfolioSerializer, PortfolioStockSerializer, TransactionSerializer, UserSerializer

# Add New Stock (Admin Only)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_stock(request):
    """
    Allows admin to add a new stock.
    Ensures ticker, company_name, price, and volume are provided.
    Returns an error if stock already exists.
    """
    ticker = request.data.get('ticker')
    company_name = request.data.get('company_name')
    price = request.data.get('price')
    volume = request.data.get('volume')

    if not ticker or not company_name or not price or not volume:
        return JsonResponse({'error': 'All fields are required'}, status=400)

    if Stock.objects.filter(ticker=ticker).exists():
        return JsonResponse({'error': 'Stock ticker already exists'}, status=400)

    stock = Stock.objects.create(
        ticker=ticker, company_name=company_name, price=float(price), volume=int(volume)
    )
    return JsonResponse({'message': f'Stock {stock.ticker} added successfully'})
