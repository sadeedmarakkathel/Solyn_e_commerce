from django.urls import path
from .import views

app_name='orders'

urlpatterns=[
    path("orders/",views.orders_page, name='orders'),
    path("create/",views.create_order, name="create"),
    path("checkout/",views.checkout, name='checkout'),
    path("cancel/<int:order_id>/", views.cancel_order, name='cancel_order'),
    path("completed/", views.order_completed, name='completed'),
    path("detail/<int:order_id>/", views.order_detail, name='order_detail'),
]
