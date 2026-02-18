from django.urls import path
from . import views

app_name='cart'

urlpatterns=[
    path("",views.cart_page,name='cart'),
    path("add/<int:id>/",views.cart_add,name='cart_add'),
    path("remove/<int:id>/",views.cart_remove,name='cart_remove'),
    path("remove_all/<int:id>/",views.cart_remove_all,name='cart_remove_all'),
    path('clear/',views.cart_clear, name='clear')
]