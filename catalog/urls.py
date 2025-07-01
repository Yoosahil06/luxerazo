from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Main catalog pages
    path('', views.product_catalog, name='product_catalog'),
    path('men/', views.men_catalog, name='men'),
    path('women/', views.women_catalog, name='women'),
    path('watches/', views.watches_catalog, name='watches'),
    path('rolex/', views.rolex_catalog, name='rolex'),
    path('accessories/', views.accessories, name='accessories'),
    path('bags/', views.bags, name='bags'),
    path('jewelry/', views.jewelry, name='jewelry'),
    path('sunglasses/', views.sunglasses, name='sunglasses'),
    path('patek-philippe/', views.patek_philippe, name='patek_philippe'),
    path('new-collection/', views.new_collection, name='new_collection'),
    path('audemars-piguet/', views.audemars_piguet, name='audemars_piguet'),
    path('richard-mille/', views.richard_mille, name='richard_mille'),
    path('gucci/', views.gucci, name='gucci'),
    path('louis-vuitton/', views.louis_vuitton, name='louis_vuitton'),
    path('handbags/', views.handbags, name='handbags'),
    path('scarves/', views.scarves, name='scarves'),
    path('perfumes/', views.perfumes, name='perfumes'),
    path('chanel/', views.chanel, name='chanel'),
    path('hermes/', views.hermes, name='hermes'),
    path('dior/', views.dior, name='dior'),
    path('cartier/', views.cartier, name='cartier'),
    path('prada/', views.prada, name='prada'),
    path('bottega-veneta/', views.bottega_veneta, name='bottega_veneta'),
    
    # Product detail
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart and wishlist actions
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('toggle-wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
]
