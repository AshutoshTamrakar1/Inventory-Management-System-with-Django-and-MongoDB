from rest_framework import serializers
from .models import Product, Supplier, StockMovement, SaleOrder

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
    
    def validate_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value

    def validate_email(self, value):
        if not value.endswith("@example.com"):  # Customize this as needed
            raise serializers.ValidationError("Email must be a valid format.")
        return value
    

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = '__all__'

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive number.")
        return value


class SaleOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = SaleOrder
        fields = '__all__'

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive number.")
        return value



class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'stock_quantity']
