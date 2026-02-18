from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def product_page(request):
    products = Product.objects.all()
    return render(request, 'home/product_list.html', {'products': products})

def product_details(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, "home/product_details.html", {'product': product})