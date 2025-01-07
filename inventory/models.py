from django.db import models
from db_connection import db

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, data):
        db.suppliers.insert_one(data)

    @classmethod
    def get_all(cls):
        return list(db.suppliers.find())

    @classmethod
    def get_by_id(cls, supplier_id):
        return db.suppliers.find_one({'supplier_id': supplier_id})

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, data):
        db.products.insert_one(data)

    @classmethod
    def get_all(cls):
        return list(db.products.find())

    @classmethod
    def get_by_id(cls, product_id):
        return db.products.find_one({'product_id': product_id})

class SaleOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'Order {self.order_id} for {self.product.name}'

    @classmethod
    def create(cls, data):
        db.sale_orders.insert_one(data)

    @classmethod
    def get_all(cls):
        return list(db.sale_orders.find())

    @classmethod
    def get_by_id(cls, order_id):
        return db.sale_orders.find_one({'order_id': order_id})

class StockMovement(models.Model):
    movement_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=50)
    movement_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.movement_type} for {self.product.name}'

    @classmethod
    def create(cls, data):
        db.stock_movements.insert_one(data)

    @classmethod
    def get_all(cls):
        return list(db.stock_movements.find())

    @classmethod
    def get_by_id(cls, movement_id):
        return db.stock_movements.find_one({'movement_id': movement_id})
