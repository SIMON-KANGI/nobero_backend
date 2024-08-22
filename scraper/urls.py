from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, SKUViewSet

router=DefaultRouter()
router.register(r'products', ProductViewSet,  basename='product')
router.register(r'skus', SKUViewSet,  basename='sku')

urlpatterns=[
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]