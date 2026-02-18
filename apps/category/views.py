from django.shortcuts import render, get_object_or_404
from apps.products.models import Product
from .models import Category

# Create your views here.
def category_page(request, name):
    category = get_object_or_404(Category, name=name)
    products = Product.objects.filter(category=category)
    return render(request, 'home/category_detail.html', {'products': products, 'category': category})