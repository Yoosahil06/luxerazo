from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile
from orders.models import Wishlist, Order
from products.models import Product

@login_required
def dashboard_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'users/dashboard.html', {
        'profile': profile,
        'wishlist': wishlist.product_wishlists.all(),
    })

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if wishlist.product_wishlists.filter(pk=product.pk).exists():
        wishlist.product_wishlists.remove(product)
    else:
        wishlist.product_wishlists.add(product)
    return redirect('dashboard')

@login_required
def account_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'wishlist': [item.product for item in wishlist_items],
        'recent_orders': recent_orders,
    }
    return render(request, 'users/account.html', context)
