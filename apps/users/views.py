from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import RegisterForm, ProfileForm, UserEditForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile

@never_cache
def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account is created.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})

@never_cache
def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "users/login.html")

@login_required
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        u_form = UserEditForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, instance=profile_obj)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:profile")
    else:
        u_form = UserEditForm(instance=request.user)
        p_form = ProfileForm(instance=profile_obj)

    return render(request, "users/profile.html", {"u_form": u_form, "p_form": p_form})

@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was changed successfully.")
            return redirect("users:profile")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "users/password_change.html", {"form": form})

@login_required
def logout_function(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("home")
