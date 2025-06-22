from django.urls import path
from .views import catalog_view, product_detail_view

urlpatterns = [
    path('', catalog_view, name='catalog'),
    path('<int:pk>/', product_detail_view, name='product_detail'),
]
