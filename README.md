# Inventory Management System

This Inventory Management System is a Django-based web application that uses MongoDB for database storage. It provides RESTful APIs to manage products, suppliers, stock movements, and sale orders, and offers a user-friendly HTML interface for interacting with the system.

## Features

- **Add Product**: Add a new product to the inventory with validation for stock quantity, price, and product details.
- **List Products**: Retrieve a list of all products in the inventory, including name, description, price, stock quantity, and supplier details.
- **Add Supplier**: Add a new supplier to the system with validation for email and phone number format, ensuring no duplicate records exist.
- **List Suppliers**: Retrieve a list of all suppliers, including name, email, phone, and address details.
- **Add Stock Movement**: Record incoming or outgoing stock and update stock levels accordingly, ensuring proper validation of stock levels.
- **Create Sale Order**: Create sale orders by selecting products, verifying sufficient stock, and calculating the total price.
- **Cancel Sale Order**: Cancel an existing sale order, update the status to "Cancelled", and restore stock levels.
- **Complete Sale Order**: Mark an order as "Completed" and update the stock levels accordingly.
- **List Sale Orders**: Retrieve a list of all sale orders, including product name, quantity, total price, sale date, status, and additional notes.
- **Stock Level Check**: Check and return the current stock level for each product.

## URLs

### API Endpoints

- **Add Product**: `http://127.0.0.1:8000/inventory/add_product/`
- **List Products**: `http://127.0.0.1:8000/inventory/list_products/`
- **Add Supplier**: `http://127.0.0.1:8000/inventory/add_supplier/`
- **List Suppliers**: `http://127.0.0.1:8000/inventory/list_suppliers/`
- **Add Stock Movement**: `http://127.0.0.1:8000/inventory/add_stock_movement/`
- **Create Sale Order**: `http://127.0.0.1:8000/inventory/create_sale_order/`
- **Cancel Sale Order**: `http://127.0.0.1:8000/inventory/cancel_sale_order/<int:pk>/`
- **Complete Sale Order**: `http://127.0.0.1:8000/inventory/complete_sale_order/<int:pk>/`
- **List Sale Orders**: `http://127.0.0.1:8000/inventory/list_sale_orders/`
- **Check Stock Levels**: `http://127.0.0.1:8000/inventory/check_stock_levels/`


### HTML Templates 
- **Add Product Page**: `http://127.0.0.1:8000/add_product_page/` 
- **List Products Page**: `http://127.0.0.1:8000/list_products_page/` 
- **Add Supplier Page**: `http://127.0.0.1:8000/add_supplier_page/` 
- **List Suppliers Page**: `http://127.0.0.1:8000/list_suppliers_page/` 
- **Add Stock Movement Page**: `http://127.0.0.1:8000/add_stock_movement_page/` 
- **Create Sale Order Page**: `http://127.0.0.1:8000/create_sale_order_page/` 
- **Cancel Sale Order Page**: `http://127.0.0.1:8000/cancel_sale_order_page/` 
- **Complete Sale Order Page**: `http://127.0.0.1:8000/complete_sale_order_page/` 
- **List Sale Orders Page**: `http://127.0.0.1:8000/list_sale_orders_page/` 
- **Check Stock Levels Page**: `http://127.0.0.1:8000/check_stock_levels_page/`
