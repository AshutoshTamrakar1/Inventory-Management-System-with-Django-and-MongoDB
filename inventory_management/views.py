import bcrypt
import logging
from django.shortcuts import redirect, render
from bson import ObjectId
from inventory.models import Supplier
from inventory_management.forms import LoginForm, RegisterForm
from user_management.decorators import role_required
from user_management.models import User
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('inventory_management')


@role_required(['store_manager', 'staff'])
def add_product_page(request):
    return render(request, 'add_product.html')

@role_required(['store_manager', 'supplier', 'staff'])
def list_products_page(request):
    user_role = request.session.get('role')
    return render(request, 'list_products.html', {'role': user_role})

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

@role_required(['store_manager', 'staff', 'supplier'])
def list_sale_orders_page(request):
    user_role = request.session.get('role')
    return render(request, 'list_sale_order.html', {'role': user_role})

@role_required(['store_manager', 'staff'])
def check_stock_levels_page(request):
    return render(request, 'check_stock_levels.html')

def home(request):
    return render(request, 'home.html')

@role_required(['store_manager' , 'supplier',  'staff'])
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
    logger.info("Accessed register page")
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
            logger.info(f"Registering user: {username}")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    logger.info("Accessed login page")
    if request.user.is_authenticated:
        return redirect('home')  # Redirect authenticated users to home page
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.get_by_username(username)
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
                request.session['user_id'] = str(user._id)
                request.session['role'] = user.role
                request.session['username'] = user.username  # Store username in session
                logger.info(f"User logged in: {username}")
                return redirect('home')
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logger.info("User logged out")
    request.session.flush()
    return redirect('login')

def profile_view(request):
    logger.info("Accessed profile view")
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user_profile = User.get_by_id(ObjectId(user_id))

        if request.method == 'POST':
            user_profile.username = request.POST['username']
            user_profile.email = request.POST['email']
            user_profile.bio = request.POST['bio']
            user_profile.location = request.POST['location']
            user_profile.birth_date = request.POST['birth_date']
            user_profile.save()
            return redirect('profile')

        return render(request, 'profile.html', {'user': user_profile})
    else:
        return redirect('login')