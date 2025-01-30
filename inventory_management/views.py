from django import db
from django.shortcuts import redirect, render
from django.urls import reverse

from inventory_management.forms import LoginForm, RegisterForm
from inventory_management.users import User
import bcrypt
from bson import ObjectId
from .decorators import role_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@role_required(['store_manager', 'staff'])
def add_product_page(request):
    return render(request, 'add_product.html')

@role_required(['store_manager', 'supplier', 'staff'])
def list_products_page(request):
    return render(request, 'list_products.html')

@role_required(['store_manager', 'staff'])
def add_supplier_page(request):
    return render(request, 'add_supplier.html')

@role_required(['store_manager', 'staff'])
def list_suppliers_page(request):
    return render(request, 'list_suppliers.html')

@role_required(['store_manager', 'staff'])
def add_stock_movement_page(request):
    return render(request, 'add_stock_movement.html')

@role_required(['store_manager', 'staff'])
def create_sale_order_page(request):
    return render(request, 'create_sale_order.html')

@role_required(['store_manager', 'staff'])
def cancel_sale_order_page(request):
    return render(request, 'cancel_sale_order.html')

@role_required(['store_manager', 'staff'])
def complete_sale_order_page(request):
    return render(request, 'complete_sale_order.html')

@role_required(['store_manager', 'staff'])
def list_sale_orders_page(request):
    return render(request, 'list_sale_order.html')

@role_required(['store_manager', 'staff'])
def check_stock_levels_page(request):
    return render(request, 'check_stock_levels.html')

@role_required(['store_manager', 'supplier', 'staff'])
def home(request):
    return render(request, 'home.html')

@role_required(['store_manager', 'staff'])
def products_page(request):
    return render(request, 'products.html')

@role_required(['store_manager', 'staff'])
def suppliers_page(request):
    return render(request, 'suppliers.html')

@role_required(['store_manager', 'supplier', 'staff'])
def orders_page(request):
    return render(request, 'orders.html')

@role_required(['store_manager', 'staff'])
def stock_page(request):
    return render(request, 'stock.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect authenticated users to home page
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            role = form.cleaned_data['role']

            if password != confirm_password:
                return render(request, 'register.html', {'form': form, 'error': 'Passwords do not match'})

            if User.get_by_username(username) or User.get_by_email(email):
                return render(request, 'register.html', {'form': form, 'error': 'Username or email already exists'})

            user = User(username=username, password=password, email=email, role=role)
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect authenticated users to home page
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.get_by_username(username)
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
                request.session['user_id'] = str(user['_id'])
                request.session['role'] = user['role']

                # Debug statements
                print(f"User ID: {request.session['user_id']}")
                print(f"User Role: {request.session['role']}")

                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    request.session.flush()
    return redirect('login')

def profile_view(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user_profile = User.get_by_id(ObjectId(user_id))
        return render(request, 'profile.html', {'user': user_profile})
    else:
        return redirect('login') 
