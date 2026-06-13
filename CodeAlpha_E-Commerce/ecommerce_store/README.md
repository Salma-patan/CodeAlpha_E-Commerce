# ShopZone - Django E-Commerce Store

A full-featured e-commerce store built with Django, featuring a White & Yellow theme.

## Features
- **Dual Login System**: Separate login for Customers and Product Owners
- **Product Listings**: Browse, search, and filter products by category
- **Product Detail Page**: Full product info with related products
- **Shopping Cart**: Add/remove items, update quantities
- **Order Processing**: Full checkout flow with shipping details
- **Order Tracking**: Customers can view order history and status
- **Owner Dashboard**: Manage products, view & update order statuses
- **Admin Panel**: Full Django admin for superusers

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser (optional)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

### 5. Access the App
- **Homepage**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/
- **Login Choice**: http://127.0.0.1:8000/accounts/login/

## User Types

### Customer
- Register/Login at `/accounts/customer/login/`
- Browse products, add to cart, checkout, track orders

### Product Owner
- Register/Login at `/accounts/owner/login/`
- Add/edit/delete products, manage orders & statuses

## Project Structure
```
ecommerce_store/
├── manage.py
├── requirements.txt
├── db.sqlite3         (created after migrate)
├── ecommerce_store/   (project config)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/          (user auth app)
│   ├── migrations/
│   ├── models.py      (CustomUser with user_type)
│   ├── views.py
│   └── templates/accounts/
├── store/             (main e-commerce app)
│   ├── migrations/
│   ├── models.py      (Product, Category, Order, Cart)
│   ├── views.py
│   ├── templates/store/
│   └── static/store/css/
├── templates/
│   └── base.html
└── media/             (uploaded product images)
```

## Theme
White (#FFFFFF) and Yellow (#FFD700) throughout — consistent and clean.
