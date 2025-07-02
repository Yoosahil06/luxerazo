
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Wishlist
from products.models import Product

@login_required
def dashboard_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'users/dashboard.html', {
        'profile': profile,
        'wishlist': wishlist.products.all(),
    })

def account_view(request):
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        return render(request, 'users/account.html', {
            'profile': profile,
        })
    else:
        return render(request, 'users/account.html', {
            'profile': None,
        })

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if product in wishlist.products.all():
        wishlist.products.remove(product)
    else:
        wishlist.products.add(product)
    return redirect('dashboard')
