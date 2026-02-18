from django.urls import path
from . import views

app_name = 'products'

urlpatterns=[
        path("",views.product_page, name='products'),
        path("product-details/<int:id>/<slug:slug>/",views.product_details, name='product_details'),
        
]