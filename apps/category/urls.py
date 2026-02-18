from django.urls import path
from . import views

app_name='categories'

urlpatterns=[
    path("<str:name>/",views.category_page, name='category'),
]