from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('orders/', views.dashboard_orders, name='orders'),
    path('products/', views.dashboard_products, name='products'),
    path('users/', views.dashboard_users, name='users'),
    path('order/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
]
