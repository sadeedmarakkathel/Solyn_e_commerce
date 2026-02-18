from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'inventory', 'featured', 'created_at']
    list_filter = ['category', 'featured', 'created_at']
    list_editable = ['price', 'inventory', 'featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}