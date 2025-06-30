from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('men/', views.men_catalog, name='men'),
    path('watches/', views.watches_catalog, name='watches'),
    path('rolex/', views.rolex_catalog, name='rolex'),
]
