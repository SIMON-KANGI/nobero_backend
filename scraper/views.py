from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, SKU
from .serializers import ProductSerializer,SKUSerializer
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SKUViewSet(viewsets.ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer
