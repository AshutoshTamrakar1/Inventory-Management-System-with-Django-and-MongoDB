from pyexpat.errors import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Product, Supplier, StockMovement, SaleOrder
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer, SupplierSerializer, StockMovementSerializer, SaleOrderSerializer, ProductStockSerializer


#Add_Product_API
@api_view(['POST'])
def add_product(request):
    # Assuming supplier info is provided as a name; adjust if necessary
    supplier_name = request.data.get('supplier')
    supplier, created = Supplier.objects.get_or_create(name=supplier_name)
    request.data['supplier'] = supplier.id
    
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # Check for duplicate product
        if Product.objects.filter(name=serializer.validated_data['name']).exists():
            return Response({"error": "Product already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#List_Product_API
@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



#Add_Supplier_API
@api_view(['POST'])
def add_supplier(request):
    serializer = SupplierSerializer(data=request.data)
    if serializer.is_valid():
        # Check for duplicate supplier
        if Supplier.objects.filter(email=serializer.validated_data['email']).exists():
            return Response({"error": "Supplier with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#List_Supplier_API
@api_view(['GET'])
def list_suppliers(request):
    suppliers = Supplier.objects.all()
    serializer = SupplierSerializer(suppliers, many=True)
    return Response(serializer.data)



#Add_Stock_Movement_API
@api_view(['POST'])
def add_stock_movement(request):
    serializer = StockMovementSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        movement_type = serializer.validated_data['movement_type']

        if movement_type == 'In':
            product.stock_quantity += quantity
        elif movement_type == 'Out':
            if product.stock_quantity < quantity:
                return Response({"error": "Insufficient stock for this operation"}, status=status.HTTP_400_BAD_REQUEST)
            product.stock_quantity -= quantity
        else:
            return Response({"error": "Invalid movement type"}, status=status.HTTP_400_BAD_REQUEST)

        product.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Create_Sale_Order_API
@api_view(['POST'])
def create_sale_order(request):
    serializer = SaleOrderSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        # Verify sufficient stock
        if product.stock_quantity < quantity:
            return Response({"error": "Insufficient stock for this order"}, status=status.HTTP_400_BAD_REQUEST)

        # Update stock levels
        product.stock_quantity -= quantity
        product.save()

        # Calculate total price
        total_price = product.price * quantity
        serializer.save(total_price=total_price)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Cancel_Sale_Order_API
@api_view(['POST'])
def cancel_sale_order(request, pk):
    try:
        sale_order = SaleOrder.objects.get(pk=pk)
        if sale_order.status == "Cancelled":
            return Response({"error": "Sale order is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        # Update stock levels
        product = sale_order.product
        product.stock_quantity += sale_order.quantity
        product.save()

        # Update sale order status
        sale_order.status = "Cancelled"
        sale_order.save()

        return Response({"message": "Sale order cancelled successfully"}, status=status.HTTP_200_OK)
    except SaleOrder.DoesNotExist:
        return Response({"error": "Sale order not found"}, status=status.HTTP_404_NOT_FOUND)



#Complete_Sale_Order_API
@api_view(['POST'])
def complete_sale_order(request, pk):
    try:
        sale_order = SaleOrder.objects.get(pk=pk)
        if sale_order.status != "Pending":
            return Response({"error": "Only pending orders can be completed"}, status=status.HTTP_400_BAD_REQUEST)

        # Update sale order status
        sale_order.status = "Completed"
        sale_order.save()

        return Response({"message": "Sale order completed successfully"}, status=status.HTTP_200_OK)
    except SaleOrder.DoesNotExist:
        return Response({"error": "Sale order not found"}, status=status.HTTP_404_NOT_FOUND)



#List Sale_order_API
@api_view(['GET'])
def list_sale_orders(request):
    sale_orders = SaleOrder.objects.all()
    serializer = SaleOrderSerializer(sale_orders, many=True)
    return Response(serializer.data)



#Stoct_Level_Check_API
@api_view(['GET'])
def check_stock_levels(request):
    products = Product.objects.all()
    serializer = ProductStockSerializer(products, many=True)
    return Response(serializer.data)
