from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, OwnerRegistrationForm, CustomLoginForm
from .models import CustomUser


def login_choice(request):
    return render(request, 'accounts/login_choice.html')


def customer_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.user_type == 'customer':
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('store:home')
            else:
                messages.error(request, 'This account is not a customer account. Please use Owner Login.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/customer_login.html', {'form': form})


def owner_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.user_type == 'owner' or user.is_superuser:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('store:owner_dashboard')
            else:
                messages.error(request, 'This account is not a product owner account. Please use Customer Login.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/owner_login.html', {'form': form})


def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to ShopEasy.')
            return redirect('store:home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/customer_register.html', {'form': form})


def owner_register(request):
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Owner account created successfully!')
            return redirect('store:owner_dashboard')
    else:
        form = OwnerRegistrationForm()
    return render(request, 'accounts/owner_register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login_choice')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
