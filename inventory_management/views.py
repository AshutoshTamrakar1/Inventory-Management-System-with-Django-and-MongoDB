from django.shortcuts import render

def add_product_page(request):
    return render(request, 'add_product.html')


def list_products_page(request):
    return render(request, 'list_products.html')


def add_supplier_page(request):
    return render(request, 'add_supplier.html')


def list_suppliers_page(request):
    return render(request, 'list_suppliers.html')


def add_stock_movement_page(request):
    return render(request, 'add_stock_movement.html')


def create_sale_order_page(request):
    return render(request, 'create_sale_order.html')


def cancel_sale_order_page(request):
    return render(request, 'cancel_sale_order.html')


def complete_sale_order_page(request):
    return render(request, 'complete_sale_order.html')


def list_sale_orders_page(request):
    return render(request, 'list_sale_orders.html')

from django.shortcuts import render

def check_stock_levels_page(request):
    return render(request, 'check_stock_levels.html')
