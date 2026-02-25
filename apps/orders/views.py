from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Order, OrderItem
from apps.cart.cart import Cart
from django.views.decorators.http import require_POST
from apps.products.models import Product

# Create your views here.

@login_required
def orders_page(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "orders/order_list.html", {'orders': orders})

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect("home")

    user = request.user
    profile = user.profile
    
    if not user.first_name or not user.last_name or not hasattr(user, 'profile') or not user.profile.address:
        messages.warning(request, "Please complete your profile!")
        return redirect("cart:cart")
        
    return render(request, "orders/checkout.html")

@login_required
@require_POST
def create_order(request):
    cart = Cart(request)

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("home")
        
    user = request.user
    if not user.first_name or not user.last_name or not user.profile.address:
        messages.warning(request, "Please complete your profile before placing an order.")
        return redirect("users:profile")

    payment_method = request.POST.get('payment_method', 'card')

    if payment_method=='card' or payment_method=='paypal':
        messages.warning(request, "Payment Issue")
        return redirect("home")

    try:
        with transaction.atomic():

            for item in cart:
                product = Product.objects.select_for_update().get(id=item["product"].id)
                if product.inventory < item["quantity"]:
                    messages.error(request, f"Sorry, only {product.inventory} units of {product.name} are available.")
                    return redirect("cart:cart")
                
                product.inventory -= item["quantity"]
                product.save()

            order = Order.objects.create(
                user=request.user,
                total_amount=cart.get_total_price(),
                payment_method=payment_method
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"]
                )

            cart.clear()
            request.session['last_order_id'] = order.id
            return redirect("orders:completed")

    except Exception as e:
        messages.error(request, f"An error occurred while processing your order: {str(e)}")
        return redirect("cart:cart")

@login_required
def order_completed(request):
    order_id = request.session.get('last_order_id')
    if not order_id:
        return redirect("home")
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/created.html", {"order": order})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        # Return inventory on cancellation
        with transaction.atomic():
            for item in order.items.all():
                item.product.inventory += item.quantity
                item.product.save()
            
            order.status = 'cancelled'
            order.shipping_status = 'Cancelled'
            order.save()
            messages.success(request, f"Order #{order.id} has been cancelled and stock returned.")
    else:
        messages.error(request, "This order cannot be cancelled.")
    return redirect("orders:orders")
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})
