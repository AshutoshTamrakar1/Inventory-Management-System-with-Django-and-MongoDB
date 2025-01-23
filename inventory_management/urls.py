"""
URL configuration for inventory_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .views import home, orders_page, products_page, stock_page, suppliers_page, user_login, user_logout, register
from inventory_management.views import add_product_page, list_products_page, add_supplier_page, list_suppliers_page, add_stock_movement_page, create_sale_order_page, cancel_sale_order_page, complete_sale_order_page, list_sale_orders_page, check_stock_levels_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path('inventory/', include('inventory.urls')),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),
    path('products/', products_page, name='products_page'),
    path('suppliers/', suppliers_page, name='suppliers_page'),
    path('orders/', orders_page, name='orders_page'),
    path('stock/', stock_page, name='stock_page'),
    path('add_product_page/', add_product_page, name='add_product_page'),
    path('list_products_page/', list_products_page, name='list_products_page'),
    path('add_supplier_page/', add_supplier_page, name='add_supplier_page'),
    path('list_suppliers_page/', list_suppliers_page, name='list_suppliers_page'),
    path('add_stock_movement_page/', add_stock_movement_page, name='add_stock_movement_page'),
    path('create_sale_order_page/', create_sale_order_page, name='create_sale_order_page'),
    path('cancel_sale_order_page/', cancel_sale_order_page, name='cancel_sale_order_page'),
    path('complete_sale_order_page/', complete_sale_order_page, name='complete_sale_order_page'),
    path('list_sale_orders_page/', list_sale_orders_page, name='list_sale_orders_page'),
    path('check_stock_levels_page/', check_stock_levels_page, name='check_stock_levels_page')
]