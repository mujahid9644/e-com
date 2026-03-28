# E-Commerce Platform - Complete Setup Guide

## 📋 Overview

A modern, production-ready e-commerce platform built with:
- **Backend**: Django REST Framework + PostgreSQL + JWT Authentication + Google OAuth
- **Frontend**: Next.js 14 + TailwindCSS + Framer Motion
- **Payment**: Stripe, bKash, Nagad
- **Cloud Storage**: Cloudinary

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+
- PostgreSQL 12+ (running)
- Node.js 16+
- Git

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your PostgreSQL credentials and API keys

# Initialize database
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Start server
python manage.py runserver
```

**Backend URL**: http://localhost:8000
**API Documentation**: http://localhost:8000/api/docs/
**Django Admin**: http://localhost:8000/admin/

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
copy .env.example .env.local
# Update NEXT_PUBLIC_API_URL=http://localhost:8000/api (if needed)

# Start development server
npm run dev
```

**Frontend URL**: http://localhost:3000

---

## 📁 Project Structure

```
e-com/
├── backend/
│   ├── ecommerce/          # Django project settings
│   ├── apps/               # Django applications
│   │   ├── users/          # Authentication & profiles
│   │   ├── products/       # Product catalog
│   │   ├── cart/           # Shopping cart & wishlist
│   │   ├── orders/         # Order management
│   │   ├── payments/       # Payment processing
│   │   └── reviews/        # Product reviews
│   ├── media/              # User-uploaded files
│   ├── logs/               # Application logs
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── pages/              # Next.js routes
│   ├── components/         # React components
│   ├── store/              # Zustand state management
│   ├── utils/              # Helper functions
│   ├── styles/             # CSS/TailwindCSS
│   ├── public/             # Static assets
│   ├── package.json
│   └── README.md
├── README.md               # This file
├── SETUP_GUIDE.md          # Setup instructions
├── DEPLOYMENT.md           # Deployment guide
└── .env.example            # Environment template
```

---

## 🔐 Environment Configuration

### Backend .env

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-super-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Frontend URL
FRONTEND_URL=http://localhost:3000

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# JWT Authentication
JWT_SECRET=your-jwt-secret-key

# Google OAuth (Get from Google Cloud Console)
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

# Cloudinary (Image Storage)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Payment Gateways
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
```

---

## 🔑 API Endpoints

### Authentication

```
POST   /api/auth/register/          Register new user
POST   /api/auth/login/             Login with credentials
POST   /api/auth/google_login/      Login with Google OAuth (access_token)
POST   /api/auth/logout/            Logout user
GET    /api/auth/profile/me/        Get current user profile
PUT    /api/auth/profile/update_profile/  Update profile
POST   /api/auth/profile/change_password/ Change password
GET    /api/auth/addresses/         List user addresses
POST   /api/auth/addresses/         Create address
POST   /api/auth/addresses/{id}/set_as_default/ Set default address
```

### Products

```
GET    /api/products/               List products (with filters)
GET    /api/products/{id}/          Get product details
GET    /api/products/{id}/reviews/  Get product reviews
GET    /api/products/{id}/related/  Get related products
GET    /api/products/categories/    List categories
GET    /api/products/brands/        List brands
GET    /api/products/featured/      Get featured products
```

**Query Parameters**:
- `search=keyword` - Search products
- `category=1` - Filter by category
- `price__gte=100&price__lte=500` - Price range
- `ordering=-price` - Sort (add `-` for descending)

### Cart & Wishlist

```
GET    /api/cart/view/              Get cart items
POST   /api/cart/add/               Add to cart
POST   /api/cart/update/            Update quantity
POST   /api/cart/remove/            Remove item
POST   /api/cart/clear/             Clear cart
GET    /api/cart/wishlist/view/     Get wishlist
POST   /api/cart/wishlist/add/      Add to wishlist
POST   /api/cart/wishlist/remove/   Remove from wishlist
```

### Orders

```
GET    /api/orders/                 List user orders
GET    /api/orders/{id}/            Get order details
POST   /api/orders/create/          Create order
POST   /api/orders/{id}/cancel/     Cancel order
GET    /api/orders/{id}/tracking/   Track order
```

### Reviews

```
GET    /api/reviews/                List reviews
POST   /api/reviews/                Create review
PUT    /api/reviews/{id}/           Update review
DELETE /api/reviews/{id}/           Delete review
POST   /api/reviews/{id}/mark_helpful/  Mark as helpful
```

---

## 🔐 Google OAuth Setup

### Step 1: Get Google Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Go to "APIs & Services" → "Credentials"
4. Create "OAuth 2.0 Client ID" (Web application)
5. Add authorized redirect URIs:
   - `http://localhost:8000/`
   - `http://localhost:3000/`
   - Your production domain
6. Copy **Client ID** and **Client Secret**

### Step 2: Add to .env

```env
GOOGLE_OAUTH_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your_secret
```

### Step 3: Frontend Integration

```javascript
// Example: Send access token to backend
fetch('http://localhost:8000/api/auth/google_login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ access_token: googleToken })
})
.then(res => res.json())
.then(data => {
  localStorage.setItem('access_token', data.tokens.access);
  localStorage.setItem('refresh_token', data.tokens.refresh);
  // Redirect to dashboard
})
```

---

## 📦 Database Setup

### Create PostgreSQL Database

```bash
# Windows (Command Prompt as Admin)
psql -U postgres
CREATE DATABASE ecommerce_db;

# macOS/Linux
sudo -u postgres psql
CREATE DATABASE ecommerce_db;
```

### Run Migrations

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

---

## 🧪 Testing APIs

### Using Curl

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "Test@123",
    "password_confirm": "Test@123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Test@123"
  }'

# Get Products (with authorization)
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Using Swagger UI

Visit: http://localhost:8000/api/docs/

---

## 🚢 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for production setup with Gunicorn, Nginx, and environment configuration.

---

## 🐛 Troubleshooting

### PostgreSQL Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1;"

# Update .env with correct credentials
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
```

### Migrations Failed
```bash
# Reset migrations (development only)
python manage.py migrate zero
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### CORS Errors
Update `CORS_ALLOWED_ORIGINS` in `.env` with your frontend URL.

---

## 🔗 Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Stripe Documentation](https://stripe.com/docs)

---

## 📄 License

MIT License

---

## ✨ Features Implemented

✅ User Authentication (JWT + Google OAuth)
✅ Product Management & Filtering
✅ Shopping Cart & Wishlist
✅ Order Management & Tracking
✅ Product Reviews & Ratings
✅ Payment Processing (Stripe, bKash, Nagad)
✅ Admin Dashboard
✅ Real-time Search
✅ Cloud Image Storage (Cloudinary)
✅ Responsive Design

---

**Need Help?** Check the `/backend/README.md` or `/frontend/README.md` for specific details.
