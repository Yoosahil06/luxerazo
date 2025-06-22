
from django.shortcuts import render, get_object_or_404
from .models import Product, Brand, Category
from django.core.paginator import Paginator
from decimal import Decimal

def catalog_view(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()

    brand_ids = request.GET.getlist("brand")
    gender = request.GET.getlist("gender")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort_by = request.GET.get("sort", "newest")

    if brand_ids:
        products = products.filter(brand__id__in=brand_ids)
    if gender:
        products = products.filter(gender__in=gender)
    if min_price:
        products = products.filter(price_in_usd__gte=Decimal(min_price))
    if max_price:
        products = products.filter(price_in_usd__lte=Decimal(max_price))

    if sort_by == "price-asc":
        products = products.order_by("price_in_usd")
    elif sort_by == "price-desc":
        products = products.order_by("-price_in_usd")
    else:
        products = products.order_by("-created_at")

    currency = "USD"
    fx_rate = 1.0
    symbol = "$"

    if "IN" in request.META.get("HTTP_CF_IPCOUNTRY", ""):
        currency = "INR"
        fx_rate = 83.0
        symbol = "₹"

    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "brands": brands,
        "categories": categories,
        "currency": symbol,
        "fx_rate": fx_rate,
        "page_obj": page_obj,
    }
    return render(request, "products/catalog.html", context)

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    currency = "USD"
    fx_rate = 1.0
    symbol = "$"

    if "IN" in request.META.get("HTTP_CF_IPCOUNTRY", ""):
        currency = "INR"
        fx_rate = 83.0
        symbol = "₹"

    price_converted = round(product.price_in_usd * fx_rate, 2)

    return render(request, "products/detail.html", {
        'product': product,
        'currency': symbol,
        'converted_price': price_converted,
    })
