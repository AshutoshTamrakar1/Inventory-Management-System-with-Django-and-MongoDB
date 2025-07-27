# Inventory Management System

This Inventory Management System is a Django-based web application using MongoDB for database storage. It provides RESTful APIs and a user-friendly HTML interface for managing products, suppliers, stock movements, sale orders, and users.

## Features

- **User Authentication & Roles**
  - Register, login, logout, and profile management
  - Role-based access: Store Manager, Supplier, Staff

- **Product Management**
  - Add new products with validation
  - List all products with details
  - Edit product information
  - Check product stock levels

- **Supplier Management**
  - Add new suppliers with validation
  - List all suppliers with details
  - Edit and remove suppliers

- **Stock Movement**
  - Record incoming and outgoing stock
  - Update and validate stock levels

- **Sale Order Management**
  - Create sale orders with product selection and stock verification
  - Cancel sale orders (restores stock)
  - Complete sale orders (updates stock)
  - List all sale orders with status and details

- **RESTful API Endpoints**
  - CRUD operations for products and suppliers
  - Stock movement and sale order APIs
  - Stock level check API

- **HTML Interface**
  - Pages for all major operations (add/list/edit products, suppliers, stock, orders)
  - Role-based navigation and access

- **Logging**
  - Centralized logging for all major actions and errors

- **Testing**
  - Unit tests for models and views 

## API Endpoints

- **Add Product:** `/inventory/add_product/`
- **List Products:** `/inventory/list_products/`
- **Add Supplier:** `/inventory/add_supplier/`
- **List Suppliers:** `/inventory/list_suppliers/`
- **Add Stock Movement:** `/inventory/add_stock_movement/`
- **Create Sale Order:** `/inventory/create_sale_order/`
- **Cancel Sale Order:** `/inventory/cancel_sale_order/<int:pk>/`
- **Complete Sale Order:** `/inventory/complete_sale_order/<int:pk>/`
- **List Sale Orders:** `/inventory/list_sale_orders/`
- **Check Stock Levels:** `/inventory/check_stock_levels/`

## HTML Pages

- **Add Product Page:** `/add_product_page/`
- **List Products Page:** `/list_products_page/`
- **Add Supplier Page:** `/add_supplier_page/`
- **List Suppliers Page:** `/list_suppliers_page/`
- **Add Stock Movement Page:** `/add_stock_movement_page/`
- **Create Sale Order Page:** `/create_sale_order_page/`
- **Cancel Sale Order Page:** `/cancel_sale_order_page/`
- **Complete Sale Order Page:** `/complete_sale_order_page/`
- **List Sale Orders Page:** `/list_sale_orders_page/`
- **Check Stock Levels Page:** `/check_stock_levels_page/`
- **User Registration/Login/Profile:** `/register/`, `/login/`, `/profile/`

## Getting Started

1. Clone the repository
2. Install dependencies
3. Configure MongoDB connection
4. Run migrations and start the server
5. Access the app via browser or API tools

---