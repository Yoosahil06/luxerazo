
from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_view, name='account'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
]
