from pyexpat.errors import messages
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse

from user_management.decorators import role_required
from .models import Product, Supplier, StockMovement, SaleOrder
from rest_framework import status
from datetime import datetime, timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer, SupplierSerializer, StockMovementSerializer, SaleOrderSerializer, ProductStockSerializer
from db_connection import db
from bson import ObjectId


#Add_Product_API
@api_view(['POST'])
def add_product(request):
    try:
        supplier_name = request.data.get('supplier')
        supplier = db.suppliers.find_one({'name': supplier_name})
        
        if not supplier:
            return Response({"error": "Supplier does not exist. Please add the supplier first."}, status=status.HTTP_400_BAD_REQUEST)
        
        supplier_id = str(supplier['_id'])
        product_name = request.data.get('name')
        price = float(request.data.get('price'))
        stock_quantity = int(request.data.get('stock_quantity'))

        # Prepare the new product data
        new_product_data = {
            'name': product_name,
            'description': request.data.get('description'),
            'category': request.data.get('category'),
            'price': price,
            'stock_quantity': stock_quantity,
            'supplier': supplier_name,
            'supplier_id': supplier_id
        }

        # Check for duplicate product with the same supplier and price
        existing_product = db.products.find_one({'name': product_name, 'supplier_id': supplier_id, 'price': price})
        if existing_product:
            # Increase the quantity of the existing product
            new_quantity = int(existing_product['stock_quantity']) + stock_quantity
            db.products.update_one({'_id': existing_product['_id']}, {'$set': {'stock_quantity': new_quantity}})
            return Response({"message": "Product quantity updated successfully"}, status=status.HTTP_200_OK)
        
        # Check for duplicate product with the same name but different supplier or price
        if db.products.find_one({'name': product_name}):
            product_id = db.products.insert_one(new_product_data).inserted_id
            new_product_data['_id'] = str(product_id)
            return Response(new_product_data, status=status.HTTP_201_CREATED)

        # Add new product
        product_id = db.products.insert_one(new_product_data).inserted_id
        new_product_data['_id'] = str(product_id)
        return Response(new_product_data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



#List_Product_API
@api_view(['GET'])
def list_products(request):
    user_role = request.session.get('role')
    user_name = request.session.get('username')  # Retrieve the username from the session
    
    if user_role == 'supplier':
        products = list(db.products.find({'supplier': user_name}))  # Match supplier_name with logged-in user's name
        
    else:
        products = list(db.products.find())  # Show all products for store managers and staff
        
    
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
    product_name = data.get('product_name')
    quantity = int(data.get('quantity'))  # Ensure quantity is an integer
    movement_type = data.get('movement_type')

    # Check if product exists by name
    product = db.products.find_one({'name': product_name})
    if not product:
        return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)

    product_id = product['_id']
    product_stock_quantity = int(product['stock_quantity'])  # Convert stock_quantity to integer

    # Update stock quantity based on movement type
    if movement_type == 'In':
        new_quantity = product_stock_quantity + quantity
    elif movement_type == 'Out':
        if product_stock_quantity < quantity:
            return Response({"error": "Insufficient stock for this operation"}, status=status.HTTP_400_BAD_REQUEST)
        new_quantity = product_stock_quantity - quantity
    else:
        return Response({"error": "Invalid movement type"}, status=status.HTTP_400_BAD_REQUEST)

    # Update the product's stock quantity
    db.products.update_one({'_id': product_id}, {'$set': {'stock_quantity': new_quantity}})

    # Add the stock movement record
    data['product_id'] = str(product_id)  # Add product_id to the movement data
    movement_id = db.stock_movements.insert_one(data).inserted_id
    data['_id'] = str(movement_id)  # Convert ObjectId to string
    return Response(data, status=status.HTTP_201_CREATED)




#Create_Sale_Order_API
@api_view(['POST'])
def create_sale_order(request):
    data = request.data
    product_name = data.get('product_name')
    quantity = int(data.get('quantity'))

    # Check if product exists by name
    product = db.products.find_one({'name': product_name})
    if not product:
        return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)

    product_id = product['_id']
    product_stock_quantity = int(product['stock_quantity'])

    # Verify sufficient stock
    if product_stock_quantity < quantity:
        return Response({"error": "Insufficient stock for this order"}, status=status.HTTP_400_BAD_REQUEST)

    # Update stock levels
    new_quantity = product_stock_quantity - quantity
    db.products.update_one({'_id': product_id}, {'$set': {'stock_quantity': new_quantity}})

    # Calculate total price
    total_price = float(product['price']) * int(quantity)
    data['total_price'] = total_price
    data['product_id'] = str(product_id)
    data['status'] = 'Pending'
    data['sale_date'] = datetime.now(timezone.utc)
    data['sale_date'] = data['sale_date'].strftime('%Y-%m-%d %H:%M:%S')

    # Add the sale order record
    order_id = db.sale_orders.insert_one(data).inserted_id
    data['_id'] = str(order_id)  # Convert ObjectId to string
    data['product_id'] = str(product_id)  # Convert ObjectId to string
    return Response(data, status=status.HTTP_201_CREATED)



#Cancel_Sale_Order_API
@role_required(['store_manager', 'staff'])
@api_view(['POST'])
def cancel_sale_order(request, pk):
    user_role = request.session.get('role')

    if user_role == 'supplier':
        return HttpResponseForbidden("You do not have permission to cancel this order.")

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
        new_quantity = int(product['stock_quantity']) + int(sale_order['quantity'])
        db.products.update_one({'_id': ObjectId(product_id)}, {'$set': {'stock_quantity': new_quantity}})

        # Update sale order status
        db.sale_orders.update_one({'_id': ObjectId(pk)}, {'$set': {'status': "Cancelled"}})

        return Response({"message": "Sale order cancelled successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




#Complete_Sale_Order_API
@role_required(['store_manager', 'staff'])
@api_view(['POST'])
def complete_sale_order(request, pk):
    user_role = request.session.get('role')
    user_name = request.session.get('username')  # Retrieve the username from the session

    if user_role != 'supplier':
        return HttpResponseForbidden("You do not have permission to complete this order.")

    try:
        # Retrieve sale order by ObjectId
        sale_order = db.sale_orders.find_one({'_id': ObjectId(pk)})
        if not sale_order:
            return Response({"error": "Sale order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if sale_order['status'] != "Pending":
            return Response({"error": "Only pending orders can be completed"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve product by ObjectId
        product_id = sale_order['product_id']
        product = db.products.find_one({'_id': ObjectId(product_id)})
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        if product['supplier_name'] != user_name:
            return HttpResponseForbidden("You do not have permission to complete this order.")

        # Update stock levels
        new_quantity = int(product['stock_quantity']) - int(sale_order['quantity'])
        db.products.update_one({'_id': ObjectId(product_id)}, {'$set': {'stock_quantity': new_quantity}})

        # Update sale order status
        db.sale_orders.update_one({'_id': ObjectId(pk)}, {'$set': {'status': "Completed"}})

        return Response({"message": "Sale order completed successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




#List Sale_order_API
@api_view(['GET'])
def list_sale_orders(request):
    user_role = request.session.get('role')
    user_name = request.session.get('username')  # Retrieve the username from the session

    if user_role == 'supplier' and user_name:
        # Fetch products supplied by the logged-in supplier
        products = list(db.products.find({'supplier': user_name}))
        product_ids = [str(product['_id']) for product in products]  # Convert ObjectIds to strings
        
        # Fetch orders for products supplied by the logged-in supplier
        sale_orders = list(db.sale_orders.find({'product_id': {'$in': product_ids}}))  # Match product_id as string

        # Ensure all matching sale orders are retrieved correctly
        for order in sale_orders:
            order['_id'] = str(order['_id'])
            order['product_id'] = str(order['product_id'])

    else:
        # Fetch all sale orders for store_manager and staff roles
        sale_orders = list(db.sale_orders.find())
        

        # Ensure all sale orders are correctly retrieved and converted
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



#Remove_Suplier_API
@role_required(['store_manager'])
@api_view(['DELETE'])
def remove_supplier(request, pk):
    try:
        db.suppliers.delete_one({'_id': ObjectId(pk)})
        return Response({"message": "Supplier removed successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

#Edit_Supplier_API
@role_required(['store_manager','staff'])
@api_view(['GET', 'POST'])
def edit_supplier_api(request, pk):
    if request.method == 'GET':
        supplier = db.suppliers.find_one({'_id': ObjectId(pk)})
        return render(request, 'edit_supplier.html', {'supplier': supplier})
    elif request.method == 'POST':
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            phone = request.data.get('phone')
            address = request.data.get('address')
            
            db.suppliers.update_one({'_id': ObjectId(pk)}, {'$set': {
                'name': name,
                'email': email,
                'phone': phone,
                'address': address
            }})
            
            return Response({"message": "Supplier updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)