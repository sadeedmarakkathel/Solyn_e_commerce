from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'shipping_status', 'tracking_id', 'total_amount', 'created_at']
    list_filter = ['status', 'shipping_status', 'created_at']
    list_editable = ['status', 'shipping_status', 'tracking_id']
    inlines = [OrderItemInline]
