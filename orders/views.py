
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from products.models import Product
from .cart import Cart

stripe.api_key = 'sk_test_XXXXXXXXXXXXXXXXXXXXXXXX'  # Replace with your actual Stripe test secret key

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    cart.add(product)
    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})

def checkout_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        line_items = []
        for item in cart:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['product'].name,
                    },
                    'unit_amount': int(float(item['product'].price_in_usd) * 100),
                },
                'quantity': item['quantity'],
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cart/',
        )
        return redirect(session.url, code=303)

    return render(request, 'orders/checkout.html', {'cart': cart})

def success_view(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'orders/success.html')
