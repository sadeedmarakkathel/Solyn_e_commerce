from django.urls import path
from . import views

app_name='users'

urlpatterns=[
    path("register/",views.register_view, name='registeration'),
    path("login/",views.login_page, name='login'),
    path("profile/",views.profile, name='profile'),
    path("password-change/",views.password_change, name='password-change'),
    path("logout/",views.logout_function, name='logout'),
]