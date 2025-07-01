from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from products.models import Product, Brand, Category
from orders.models import Cart, CartItem, Wishlist
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

def product_catalog(request):
    """Main product catalog with filtering and pagination"""
    products = Product.objects.filter(is_active=True)
    
    # Filtering
    brand_filter = request.GET.get('brand')
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    authenticity_filter = request.GET.get('authenticity')
    search_query = request.GET.get('search')
    
    if brand_filter:
        products = products.filter(brand__slug=brand_filter)
    
    if category_filter:
        products = products.filter(category__slug=category_filter)
    
    if price_min:
        products = products.filter(price_in_usd__gte=price_min)
    
    if price_max:
        products = products.filter(price_in_usd__lte=price_max)
    
    if authenticity_filter:
        products = products.filter(authenticity=authenticity_filter)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        products = products.order_by('price_in_usd')
    elif sort_by == 'price_high':
        products = products.order_by('-price_in_usd')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'popular':
        products = products.order_by('-is_featured', '-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    brands = Brand.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'brands': brands,
        'categories': categories,
        'current_filters': {
            'brand': brand_filter,
            'category': category_filter,
            'price_min': price_min,
            'price_max': price_max,
            'authenticity': authenticity_filter,
            'search': search_query,
            'sort': sort_by,
        },
        'page_title': 'Luxury Collection - Luxerazo',
        'meta_description': 'Discover our exclusive collection of luxury products from the world\'s most prestigious brands.'
    }
    return render(request, 'catalog/product_catalog.html', context)

def accessories(request):
    products = Product.objects.filter(is_active=True, category__name__iexact='Accessories')
    return render(request, 'catalog/accessories.html', {'products': products})

def bags(request):
    products = Product.objects.filter(is_active=True, category__name__iexact='Bags')
    return render(request, 'catalog/bags.html', {'products': products})

def jewelry(request):
    products = Product.objects.filter(is_active=True, category__name__iexact='Jewelry')
    return render(request, 'catalog/jewelry.html', {'products': products})

def sunglasses(request):
    products = Product.objects.filter(is_active=True, category__name__iexact='Sunglasses')
    return render(request, 'catalog/sunglasses.html', {'products': products})

def patek_philippe(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Patek Philippe')
    return render(request, 'catalog/patek_philippe.html', {'products': products})

def new_collection(request):
    products = Product.objects.filter(is_active=True, category__name__iexact='New Collection')
    return render(request, 'catalog/new_collection.html', {'products': products})

def audemars_piguet(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Audemars Piguet')
    return render(request, 'catalog/audemars_piguet.html', {'products': products})

def richard_mille(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Richard Mille')
    return render(request, 'catalog/richard_mille.html', {'products': products})

def gucci(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Gucci')
    return render(request, 'catalog/gucci.html', {'products': products})

def louis_vuitton(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Louis Vuitton')
    return render(request, 'catalog/louis_vuitton.html', {'products': products})

def handbags(request):
    products = Product.objects.filter(is_active=True, category__name__iexact='Handbags')
    return render(request, 'catalog/handbags.html', {'products': products})

def scarves(request):
    products = Product.objects.filter(is_active=True, category__name__iexact='Scarves')
    return render(request, 'catalog/scarves.html', {'products': products})

def perfumes(request):
    products = Product.objects.filter(is_active=True, category__name__iexact='Perfumes')
    return render(request, 'catalog/perfumes.html', {'products': products})

def chanel(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Chanel')
    return render(request, 'catalog/chanel.html', {'products': products})

def hermes(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Hermes')
    return render(request, 'catalog/hermes.html', {'products': products})

def dior(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Dior')
    return render(request, 'catalog/dior.html', {'products': products})

def cartier(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Cartier')
    return render(request, 'catalog/cartier.html', {'products': products})

def prada(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Prada')
    return render(request, 'catalog/prada.html', {'products': products})

def bottega_veneta(request):
    products = Product.objects.filter(is_active=True, brand__name__iexact='Bottega Veneta')
    return render(request, 'catalog/bottega_veneta.html', {'products': products})

def new_arrivals(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:24]
    return render(request, 'catalog/new_arrivals.html', {'products': products})

def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Check if in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user, 
            product=product
        ).exists()
    
    context = {
        'product': product,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
        'page_title': f"{product.name} - Luxerazo",
        'meta_description': product.description[:160] + '...' if len(product.description) > 160 else product.description
    }
    return render(request, 'catalog/product_detail.html', context)

def men_catalog(request):
    """Men's products catalog"""
    products = Product.objects.filter(gender='Men', is_active=True)
    
    # Apply filters
    brand_filter = request.GET.get('brand')
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    if brand_filter:
        products = products.filter(brand__slug=brand_filter)
    if category_filter:
        products = products.filter(category__slug=category_filter)
    if price_min:
        products = products.filter(price_in_usd__gte=price_min)
    if price_max:
        products = products.filter(price_in_usd__lte=price_max)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        products = products.order_by('price_in_usd')
    elif sort_by == 'price_high':
        products = products.order_by('-price_in_usd')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': "Men's Collection - Luxerazo",
        'meta_description': "Explore Luxerazo's exclusive men's collection featuring luxury watches, bags, and accessories.",
        'current_filters': {
            'brand': brand_filter,
            'category': category_filter,
            'price_min': price_min,
            'price_max': price_max,
            'sort': sort_by,
        }
    }
    return render(request, 'catalog/men.html', context)

def watches_catalog(request):
    """Watches category catalog"""
    watch_category = Category.objects.filter(name__icontains='watch').first()
    products = Product.objects.filter(is_active=True)
    
    if watch_category:
        products = products.filter(category=watch_category)
    else:
        products = products.filter(category__name__icontains='watch')
    
    # Apply filters
    brand_filter = request.GET.get('brand')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    authenticity_filter = request.GET.get('authenticity')
    
    if brand_filter:
        products = products.filter(brand__slug=brand_filter)
    if price_min:
        products = products.filter(price_in_usd__gte=price_min)
    if price_max:
        products = products.filter(price_in_usd__lte=price_max)
    if authenticity_filter:
        products = products.filter(authenticity=authenticity_filter)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        products = products.order_by('price_in_usd')
    elif sort_by == 'price_high':
        products = products.order_by('-price_in_usd')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get watch brands
    watch_brands = Brand.objects.filter(
        products__category=watch_category,
        is_active=True
    ).distinct() if watch_category else Brand.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'category': watch_category,
        'brands': watch_brands,
        'page_title': "Watches Collection - Luxerazo",
        'meta_description': "Explore Luxerazo's exclusive collection of luxury watches from the world's finest brands.",
        'current_filters': {
            'brand': brand_filter,
            'price_min': price_min,
            'price_max': price_max,
            'authenticity': authenticity_filter,
            'sort': sort_by,
        }
    }
    return render(request, 'catalog/watches.html', context)

def women_catalog(request):
    """Women's products catalog"""
    products = Product.objects.filter(gender='Women', is_active=True)
    
    # Apply filters
    brand_filter = request.GET.get('brand')
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    if brand_filter:
        products = products.filter(brand__slug=brand_filter)
    if category_filter:
        products = products.filter(category__slug=category_filter)
    if price_min:
        products = products.filter(price_in_usd__gte=price_min)
    if price_max:
        products = products.filter(price_in_usd__lte=price_max)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        products = products.order_by('price_in_usd')
    elif sort_by == 'price_high':
        products = products.order_by('-price_in_usd')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': "Women's Collection - Luxerazo",
        'meta_description': "Explore Luxerazo's exclusive women's collection featuring luxury watches, bags, and accessories.",
        'current_filters': {
            'brand': brand_filter,
            'category': category_filter,
            'price_min': price_min,
            'price_max': price_max,
            'sort': sort_by,
        }
    }
    return render(request, 'catalog/women.html', context)

def rolex_catalog(request):
    """Rolex brand catalog"""
    rolex_brand = Brand.objects.filter(name__iexact='Rolex').first()
    products = Product.objects.filter(is_active=True)
    
    if rolex_brand:
        products = products.filter(brand=rolex_brand)
    else:
        products = products.filter(brand__name__icontains='rolex')
    
    # Apply filters
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    authenticity_filter = request.GET.get('authenticity')
    
    if category_filter:
        products = products.filter(category__slug=category_filter)
    if price_min:
        products = products.filter(price_in_usd__gte=price_min)
    if price_max:
        products = products.filter(price_in_usd__lte=price_max)
    if authenticity_filter:
        products = products.filter(authenticity=authenticity_filter)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        products = products.order_by('price_in_usd')
    elif sort_by == 'price_high':
        products = products.order_by('-price_in_usd')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for Rolex products
    rolex_categories = Category.objects.filter(
        products__brand=rolex_brand,
        is_active=True
    ).distinct() if rolex_brand else Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'brand': rolex_brand,
        'categories': rolex_categories,
        'page_title': "Rolex Collection - Luxerazo",
        'meta_description': "Explore Luxerazo's exclusive collection of Rolex luxury watches.",
        'current_filters': {
            'category': category_filter,
            'price_min': price_min,
            'price_max': price_max,
            'authenticity': authenticity_filter,
            'sort': sort_by,
        }
    }
    return render(request, 'catalog/rolex.html', context)

@require_POST
@login_required
def add_to_cart(request):
    """Add product to cart via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart',
            'cart_total': cart.total_items
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@require_POST
@login_required
def toggle_wishlist(request):
    """Toggle product in wishlist via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if not created:
            wishlist_item.delete()
            in_wishlist = False
            message = f'{product.name} removed from wishlist'
        else:
            in_wishlist = True
            message = f'{product.name} added to wishlist'
        
        return JsonResponse({
            'success': True,
            'in_wishlist': in_wishlist,
            'message': message
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
