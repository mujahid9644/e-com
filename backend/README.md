# E-Commerce Backend Setup Guide

## Overview

This is a modern Django REST Framework backend for a full-featured e-commerce platform with:
- JWT Authentication
- Product Management & Filtering
- Shopping Cart & Wishlist
- Order Management & Tracking
- Product Reviews & Ratings
- Payment Processing (Stripe, bKash, Nagad)
- Coupon/Discount System
- Admin API for management

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip & virtualenv
- Git

## Installation & Setup

### 1. Clone Project & Create Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
# IMPORTANT: Change SECRET_KEY and database credentials
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb ecommerce_db

# Run migrations
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser
# Follow prompts for username, email, password
```

### 5. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Server will be available at: http://localhost:8000

## API Documentation
                            http://localhost:8000/admin/
### Access API Docs

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Schema**: http://localhost:8000/api/schema/

## API Endpoints Overview

### Authentication (`/api/auth/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register new user |
| POST | `/auth/login/` | Login and get JWT tokens |
| GET | `/profile/me/` | Get current user profile |
| PUT | `/profile/update_profile/` | Update user profile |
| POST | `/profile/change_password/` | Change password |
| GET | `/addresses/` | List user addresses |
| POST | `/addresses/` | Create new address |
| POST | `/addresses/{id}/set_as_default/` | Set address as default |

### Products (`/api/products/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List products (with filters, search, pagination) |
| GET | `/?category__id=1` | Filter by category |
| GET | `/?brand__id=1` | Filter by brand |
| GET | `/?price__gte=100&price__lte=1000` | Filter by price range |
| GET | `/?search=laptop` | Search products |
| GET | `/?ordering=-price` | Sort by price (add `-` for descending) |
| GET | `/{slug}/` | Get product details |
| GET | `/{slug}/reviews/` | Get product reviews |
| GET | `/{slug}/related/` | Get related products |
| GET | `/categories/` | List all categories |
| GET | `/brands/` | List all brands |
| GET | `/featured/` | Get featured products |

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

### Shopping Cart (`/api/cart/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/view/` | Get current cart |
| POST | `/add/` | Add item to cart |
| POST | `/remove/` | Remove item from cart |
| POST | `/update/` | Update item quantity |
| POST | `/clear/` | Clear entire cart |

**Add to Cart Example:**
```json
POST /api/cart/add/
{
  "product_id": 1,
  "quantity": 2
}
```

### Wishlist (`/api/cart/wishlist/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/view/` | Get wishlist |
| POST | `/add/` | Add to wishlist |
| POST | `/remove/` | Remove from wishlist |
| POST | `/is_in_wishlist/` | Check if product in wishlist |

### Orders (`/api/orders/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List user's orders |
| GET | `/{id}/` | Get order details |
| POST | `/create/` | Create new order from cart |
| POST | `/{id}/cancel/` | Cancel pending order |
| GET | `/{id}/tracking/` | Get shipment tracking |
| POST | `/{id}/request_return/` | Request return |

**Create Order Example:**
```json
POST /api/orders/create/
{
  "shipping_address_id": 1,
  "payment_method": "stripe",
  "coupon_code": "SAVE10",
  "customer_notes": "Please deliver in the morning"
}
```

### Reviews (`/api/reviews/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List approved reviews |
| GET | `/{id}/` | Get review details |
| POST | `/` | Create new review (authenticated) |
| PUT | `/{id}/` | Update own review |
| DELETE | `/{id}/` | Delete own review |
| POST | `/{id}/mark_helpful/` | Mark review as helpful |
| POST | `/{id}/mark_unhelpful/` | Mark review as unhelpful |

**Create Review Example:**
```json
POST /api/reviews/
{
  "product": 1,
  "rating": 5,
  "title": "Excellent product!",
  "content": "Very satisfied with this purchase. Great quality and fast shipping."
}
```

### Payments & Coupons (`/api/payments/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/payments/{id}/` | Get payment details |
| POST | `/validate_coupon/` | Validate coupon code |
| POST | `/apply_coupon/` | Apply coupon to order |
| GET | `/coupons/` | List active coupons |
| GET | `/coupons/active/` | List currently valid coupons |

**Validate Coupon Example:**
```json
POST /api/payments/validate_coupon/
{
  "code": "SAVE10",
  "order_amount": 500.00
}
```

## Authentication

### Using JWT Tokens

1. **Register & Login**
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'

# Response includes tokens:
{
  "user": {...},
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

2. **Use Access Token in Headers**
```bash
curl -X GET http://localhost:8000/api/auth/profile/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

3. **Refresh Token When Expired**
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

## Database Models

### Users & Addresses
- `CustomUser`: Extended user model with phone, profile picture
- `Address`: Shipping and billing addresses for users
- `UserPreferences`: User settings and preferences
- `UserActivity`: Audit trail of user actions

### Products
- `Category`: Product categories with hierarchical support
- `Brand`: Product brands
- `Product`: Main product model with pricing, inventory, ratings
- `ProductImage`: Gallery images for products
- `ProductAttribute`: Flexible attributes (size, color, etc.)

### Orders & Payments
- `Order`: Main order tracking
- `OrderItem`: Individual items in an order
- `OrderShipment`: Shipment tracking information
- `OrderReturn`: Returns and refunds
- `Payment`: Payment transaction records
- `Coupon`: Discount codes
- `CouponUsage`: Track coupon usage per user

### Cart & Wishlist
- `Cart`: Shopping cart per user
- `CartItem`: Items in cart
- `Wishlist`: User's wishlist
- `WishlistItem`: Items in wishlist

### Reviews
- `ProductReview`: Customer reviews and ratings
- `ReviewImage`: Images attached to reviews
- `ReviewVote`: Helpful/unhelpful votes on reviews

## Configuration

### Important Settings in `settings.py`

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        # ... other settings
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Token Expiration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# CORS - Add frontend URL
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Frontend dev server
]
```

## Advanced Features

### Filtering & Search

```bash
# Filter by multiple criteria
curl "http://localhost:8000/api/products/?category__id=1&price__gte=100&price__lte=500"

# Search
curl "http://localhost:8000/api/products/?search=laptop"

# Ordering
curl "http://localhost:8000/api/products/?ordering=-price"  # Descending
curl "http://localhost:8000/api/products/?ordering=price"   # Ascending
```

### Pagination

```bash
# Get page 2 with 10 items per page
curl "http://localhost:8000/api/products/?page=2&page_size=10"
```

## Error Handling

All API responses follow a consistent format:

**Success (2xx):**
```json
{
  "id": 1,
  "name": "Product Name",
  ...
}
```

**Error (4xx/5xx):**
```json
{
  "error": "Error message",
  "detail": "Detailed error explanation"
}
```

## Admin Panel

Access Django admin at: http://localhost:8000/admin/

- Username: superuser username
- Password: superuser password

Manage:
- Users and permissions
- Products, categories, brands
- Orders and shipments
- Coupons and discounts
- Reviews and ratings

## Deployment

### Production Checklist

1. Set `DEBUG = False` in `.env`
2. Generate strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` with your domain
4. Set `SECURE_SSL_REDIRECT = True`
5. Use proper database (PostgreSQL)
6. Use environment variables for secrets
7. Set up proper logging
8. Use gunicorn or similar WSGI server
9. Configure nginx/apache as reverse proxy
10. Enable HTTPS/SSL

### Production Commands

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run with gunicorn
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
# Verify connection string in .env
# Run migrations: python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### CORS Errors
```python
# Add frontend URL to CORS_ALLOWED_ORIGINS in settings.py
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://yourdomain.com'
]
```

## Support & Documentation

- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- SimplJWT: https://django-rest-framework-simplejwt.readthedocs.io/
- PostgreSQL: https://www.postgresql.org/docs/

---

**Happy Coding!** 🚀
