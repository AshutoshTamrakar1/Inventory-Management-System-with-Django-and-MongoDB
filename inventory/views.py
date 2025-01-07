from pyexpat.errors import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Product, Supplier, StockMovement, SaleOrder
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer, SupplierSerializer, StockMovementSerializer, SaleOrderSerializer, ProductStockSerializer
from db_connection import db
from bson import ObjectId


#Add_Product_API
@api_view(['POST'])
def add_product(request):
    supplier_name = request.data.get('supplier')
    supplier = db.suppliers.find_one({'name': supplier_name})
    
    if not supplier:
        supplier_id = db.suppliers.insert_one({'name': supplier_name}).inserted_id
    else:
        supplier_id = supplier['_id']
    
    request.data['supplier_id'] = str(supplier_id)  # Convert ObjectId to string
    
    # Check for duplicate product
    if db.products.find_one({'name': request.data.get('name')}):
        return Response({"error": "Product already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    product_id = db.products.insert_one(request.data).inserted_id
    request.data['_id'] = str(product_id)  # Convert ObjectId to string
    return Response(request.data, status=status.HTTP_201_CREATED)



#List_Product_API
@api_view(['GET'])
def list_products(request):
    products = list(db.products.find())
    # Convert ObjectId to string for JSON serialization
    for product in products:
        product['_id'] = str(product['_id'])
        product['supplier_id'] = str(product['supplier_id'])
    return Response(products, status=status.HTTP_200_OK)




#Add_Supplier_API
@api_view(['POST'])
def add_supplier(request):
    supplier_data = request.data
    
    # Check for duplicate supplier
    if db.suppliers.find_one({'email': supplier_data.get('email')}):
        return Response({"error": "Supplier with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    supplier_id = db.suppliers.insert_one(supplier_data).inserted_id
    supplier_data['_id'] = str(supplier_id)  # Convert ObjectId to string
    return Response(supplier_data, status=status.HTTP_201_CREATED)




#List_Supplier_API
@api_view(['GET'])
def list_suppliers(request):
    suppliers = list(db.suppliers.find())
    # Convert ObjectId to string for JSON serialization
    for supplier in suppliers:
        supplier['_id'] = str(supplier['_id'])
    return Response(suppliers, status=status.HTTP_200_OK)




#Add_Stock_Movement_API
@api_view(['POST'])
def add_stock_movement(request):
    data = request.data
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    movement_type = data.get('movement_type')

    # Check if product exists
    product = db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Update stock quantity based on movement type
    if movement_type == 'In':
        new_quantity = product['stock_quantity'] + quantity
    elif movement_type == 'Out':
        if product['stock_quantity'] < quantity:
            return Response({"error": "Insufficient stock for this operation"}, status=status.HTTP_400_BAD_REQUEST)
        new_quantity = product['stock_quantity'] - quantity
    else:
        return Response({"error": "Invalid movement type"}, status=status.HTTP_400_BAD_REQUEST)

    # Update the product's stock quantity
    db.products.update_one({'_id': ObjectId(product_id)}, {'$set': {'stock_quantity': new_quantity}})

    # Add the stock movement record
    movement_id = db.stock_movements.insert_one(data).inserted_id
    data['_id'] = str(movement_id)  # Convert ObjectId to string
    data['product_id'] = str(product_id)  # Convert ObjectId to string
    return Response(data, status=status.HTTP_201_CREATED)



#Create_Sale_Order_API
@api_view(['POST'])
def create_sale_order(request):
    data = request.data
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Check if product exists
    product = db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Verify sufficient stock
    if product['stock_quantity'] < quantity:
        return Response({"error": "Insufficient stock for this order"}, status=status.HTTP_400_BAD_REQUEST)

    # Update stock levels
    new_quantity = product['stock_quantity'] - quantity
    db.products.update_one({'_id': ObjectId(product_id)}, {'$set': {'stock_quantity': new_quantity}})

    # Calculate total price
    total_price = product['price'] * quantity
    data['total_price'] = total_price

    # Add the sale order record
    order_id = db.sale_orders.insert_one(data).inserted_id
    data['_id'] = str(order_id)  # Convert ObjectId to string
    data['product_id'] = str(product_id)  # Convert ObjectId to string
    return Response(data, status=status.HTTP_201_CREATED)



#Cancel_Sale_Order_API
@api_view(['POST'])
def cancel_sale_order(request, pk):
    try:
        # Retrieve sale order by ObjectId
        sale_order = db.sale_orders.find_one({'_id': ObjectId(pk)})
        if not sale_order:
            return Response({"error": "Sale order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if sale_order['status'] == "Cancelled":
            return Response({"error": "Sale order is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve product by ObjectId
        product_id = sale_order['product_id']
        product = db.products.find_one({'_id': ObjectId(product_id)})
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update stock levels
        new_quantity = product['stock_quantity'] + sale_order['quantity']
        db.products.update_one({'_id': ObjectId(product_id)}, {'$set': {'stock_quantity': new_quantity}})

        # Update sale order status
        db.sale_orders.update_one({'_id': ObjectId(pk)}, {'$set': {'status': "Cancelled"}})

        return Response({"message": "Sale order cancelled successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




#Complete_Sale_Order_API
@api_view(['POST'])
def complete_sale_order(request, pk):
    try:
        # Retrieve sale order by ObjectId
        sale_order = db.sale_orders.find_one({'_id': ObjectId(pk)})
        if not sale_order:
            return Response({"error": "Sale order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if sale_order['status'] != "Pending":
            return Response({"error": "Only pending orders can be completed"}, status=status.HTTP_400_BAD_REQUEST)

        # Update sale order status
        db.sale_orders.update_one({'_id': ObjectId(pk)}, {'$set': {'status': "Completed"}})

        return Response({"message": "Sale order completed successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




#List Sale_order_API
@api_view(['GET'])
def list_sale_orders(request):
    sale_orders = list(db.sale_orders.find())
    # Convert ObjectId to string for JSON serialization
    for order in sale_orders:
        order['_id'] = str(order['_id'])
        order['product_id'] = str(order['product_id'])
    return Response(sale_orders, status=status.HTTP_200_OK)




#Stoct_Level_Check_API
@api_view(['GET'])
def check_stock_levels(request):
    products = list(db.products.find())
    # Convert ObjectId to string for JSON serialization
    for product in products:
        product['_id'] = str(product['_id'])
        product['supplier_id'] = str(product['supplier_id'])
    return Response(products, status=status.HTTP_200_OK)

