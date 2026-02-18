from django.shortcuts import render,redirect,get_object_or_404
from .cart import Cart
from apps.products.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def cart_page(request):
    cart=Cart(request)
    return render(request,'home/cart.html',{'cart': cart})

def cart_add(request,id):
    cart= Cart(request)
    product=get_object_or_404(Product, id=id)
    cart.add(product)
    return redirect('cart:cart')

def cart_clear(request):
    cart=Cart(request)
    cart.clear()
    return redirect('cart:cart')

def cart_remove(request, id):
    cart=Cart(request)
    cart.remove(id)
    return redirect('cart:cart')

def cart_remove_all(request, id):
    cart=Cart(request)
    cart.remove_all(id)
    return redirect('cart:cart')