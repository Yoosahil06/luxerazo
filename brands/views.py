
from django.shortcuts import render
from .models import Brand

def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'brands/list.html', {'brands': brands})
