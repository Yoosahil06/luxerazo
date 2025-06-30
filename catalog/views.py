from django.shortcuts import render

def men_catalog(request):
    """
    View for the men's catalog page.
    """
    context = {
        'page_title': "Men's Collection - Luxerazo",
        'meta_description': "Explore Luxerazo's exclusive men's collection featuring luxury watches, bags, and accessories.",
    }
    return render(request, 'catalog/men.html', context)

def watches_catalog(request):
    """
    View for the watches catalog page.
    """
    context = {
        'page_title': "Watches Collection - Luxerazo",
        'meta_description': "Explore Luxerazo's exclusive collection of luxury watches from the world's finest brands.",
    }
    return render(request, 'catalog/watches.html', context)

from products.models import Product, Brand

def rolex_catalog(request):
    """
    View for the Rolex catalog page.
    """
    rolex_brand = Brand.objects.filter(name__iexact='Rolex').first()
    products = Product.objects.filter(brand=rolex_brand) if rolex_brand else []

    context = {
        'page_title': "Rolex Collection - Luxerazo",
        'meta_description': "Explore Luxerazo's exclusive collection of Rolex luxury watches.",
        'products': products,
    }
    return render(request, 'catalog/rolex.html', context)
