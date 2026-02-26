from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from apps.orders.models import Order
from apps.products.models import Product
from django.contrib.auth.models import User
from django.db.models import Sum

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@superuser_required
def dashboard_home(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_products = Product.objects.count()
    total_users = User.objects.count()
    
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    low_stock = Product.objects.filter(inventory__lt=10).order_by('inventory')[:5]
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_users': total_users,
        'recent_orders': recent_orders,
        'low_stock': low_stock,
    }
    return render(request, 'dashboard/home.html', context)

@superuser_required
def dashboard_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/orders.html', {'orders': orders})

@superuser_required
def dashboard_products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/products.html', {'products': products})

@superuser_required
def dashboard_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users.html', {'users': users})

@superuser_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        shipping_status = request.POST.get('shipping_status')
        tracking_id = request.POST.get('tracking_id')
        
        if shipping_status:
            order.shipping_status = shipping_status
        if tracking_id:
            order.tracking_id = tracking_id
            
        order.save()
    return redirect('dashboard:orders')

@superuser_required
def update_product_stock(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        inventory = request.POST.get('inventory')
        if inventory is not None:
            product.inventory = int(inventory)
            product.save()
    return redirect('dashboard:products')