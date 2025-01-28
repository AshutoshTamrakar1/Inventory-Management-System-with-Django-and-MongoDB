from django.urls import path
from .views import (
    add_product,
    list_products,
    add_supplier,
    list_suppliers,
    add_stock_movement,
    create_sale_order,
    cancel_sale_order,
    complete_sale_order,
    list_sale_orders,
    check_stock_levels,
    remove_supplier,
)

urlpatterns = [
    path('add_product/', add_product, name='add_product'),
    path('list_products/', list_products, name='list_products'),
    path('add_supplier/', add_supplier, name='add_supplier'),
    path('list_suppliers/', list_suppliers, name='list_suppliers'),
    path('add_stock_movement/', add_stock_movement, name='add_stock_movement'),
    path('create_sale_order/', create_sale_order, name='create_sale_order'),
    path('cancel_sale_order/<str:pk>/', cancel_sale_order, name='cancel_sale_order'),
    path('complete_sale_order/<str:pk>/', complete_sale_order, name='complete_sale_order'),
    path('list_sale_orders/', list_sale_orders, name='list_sale_orders'),
    path('check_stock_levels/', check_stock_levels, name='check_stock_levels'),
    path('remove_supplier/<str:pk>/', remove_supplier, name='remove_supplier')
]