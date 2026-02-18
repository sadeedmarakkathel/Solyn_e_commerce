from django.shortcuts import render, get_object_or_404, redirect
from apps.products.models import Product
from apps.category.models import Category
from .models import Hero
from django.contrib import messages
from apps.cart.cart import Cart
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def home_page(request):

    featured_products=Product.objects.filter(featured=True)
    categories=Category.objects.all()
    hero=Hero.objects.all()
    return render(request,'home/home.html', {'products' : featured_products,
                                            'categories' : categories,
                                            'hero': hero})

