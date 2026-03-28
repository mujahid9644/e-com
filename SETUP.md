# E-Commerce Project - Complete Setup Guide

## 💡 Overview

This project has been upgraded to use **PostgreSQL** (removed SQLite) and includes **Google OAuth** for easy login.

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+
- PostgreSQL 12+ (installed and running)
- Node.js 16+

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env

# IMPORTANT: Edit .env with your PostgreSQL credentials:
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=ecommerce_db
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432

# Initialize database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

**Backend URL**: http://localhost:8000
**API Docs**: http://localhost:8000/api/docs/
**Admin Panel**: http://localhost:8000/admin/

### Frontend Setup

```bash
cd frontend

npm install
copy .env.example .env.local
npm run dev
```

**Frontend URL**: http://localhost:3000

---

## 📋 Step-by-Step PostgreSQL Setup

### Option 1: Windows PowerShell

```powershell
# 1. Start PostgreSQL service
Start-Service postgresql-x64-15  # Replace 15 with your version

# 2. Connect to PostgreSQL
psql -U postgres

# 3. Create database (in psql)
CREATE DATABASE ecommerce_db;

# 4. View databases
\l

# 5. Exit psql
\q
```

### Option 2: Windows Command Prompt

```cmd
REM Start PostgreSQL
net start postgresql-x64-15

REM Connect
psql -U postgres

REM Create database
CREATE DATABASE ecommerce_db;

REM Exit
\q
```

### Option 3: macOS/Linux

```bash
# Start PostgreSQL (if using Homebrew)
brew services start postgresql

# Connect
psql -U postgres

# Create database
CREATE DATABASE ecommerce_db;

# Exit
\q
```

---

## ⚙️ Environment Configuration

### Backend .env Template

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-super-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# Frontend URL
FRONTEND_URL=http://localhost:3000

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# JWT Authentication
JWT_SECRET=your-jwt-secret-key-here

# Google OAuth (From Google Cloud Console)
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

# Cloudinary (Image Storage)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Stripe Payment Gateway
STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxx
```

### Frontend .env.local Template

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=E-Commerce Store
```

---

## 🔐 Google OAuth Setup

### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Go to "APIs & Services" → "Credentials"
4. Click "Create Credentials" → "OAuth 2.0 Client ID"
5. Select **Web Application**
6. Add authorized redirect URIs:
   - `http://localhost:8000/`
   - `http://localhost:3000/`
   - Your production domain (e.g., `https://yourdomain.com/`)
7. Copy **Client ID** and **Client Secret** to your `.env`

### Step 2: Frontend Implementation

```javascript
// Example: Using Google button to login
import { GoogleLogin } from '@react-oauth/google';

const handleSuccess = async (credentialResponse) => {
  const response = await fetch('http://localhost:8000/api/auth/google_login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      access_token: credentialResponse.credential 
    })
  });
  
  const data = await response.json();
  
  // Save tokens
  localStorage.setItem('access_token', data.tokens.access);
  localStorage.setItem('refresh_token', data.tokens.refresh);
  
  // Redirect to dashboard
  window.location.href = '/dashboard';
};

export default function LoginPage() {
  return (
    <GoogleLogin onSuccess={handleSuccess} />
  );
}
```

---

## 🗄️ Database Verification

```bash
# Check if database exists
psql -U postgres -c "\l"

# Connect to database
psql -U postgres -d ecommerce_db

# List tables (in psql)
\dt

# Exit
\q
```

---

## 🧪 Test API Endpoints

### Register New User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "Test@123",
    "password_confirm": "Test@123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Test@123"
  }'
```

### Get Profile
```bash
curl -X GET http://localhost:8000/api/auth/profile/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### List Products
```bash
curl -X GET "http://localhost:8000/api/products/?page=1&page_size=10"
```

---

## 🚨 Common Issues & Solutions

### Issue 1: PostgreSQL Connection Error
```
Error: could not connect to server: Connection refused
```

**Solution:**
```bash
# Check if PostgreSQL is running
Test-NetConnection localhost -Port 5432

# Start PostgreSQL
Start-Service postgresql-x64-15

# Update .env with correct credentials
DB_HOST=localhost
DB_PORT=5432
```

### Issue 2: Migrations Failed
```
Error: django.db.utils.ProgrammingError
```

**Solution:**
```bash
# Verify database exists
psql -U postgres -c "\l"

# If not, create it
psql -U postgres -c "CREATE DATABASE ecommerce_db;"

# Try migrations again
python manage.py migrate
```

### Issue 3: Google OAuth Not Working
**Solution:**
- Verify Client ID and Client Secret in `.env`
- Check redirect URIs in Google Cloud Console
- Ensure `FRONTEND_URL` is correct in `.env`

### Issue 4: CORS Errors
**Solution:**
Update `CORS_ALLOWED_ORIGINS` in `.env`:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,https://yourdomain.com
```

### Issue 5: Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

---

## 🧹 Clean Installation

If you need to start fresh:

```bash
# Backend cleanup
cd backend
Remove-Item -Recurse -Force migrations/__pycache__
Remove-Item db.sqlite3 -Force -ErrorAction SilentlyContinue

# Database reset (PostgreSQL)
psql -U postgres -c "DROP DATABASE IF EXISTS ecommerce_db;"
psql -U postgres -c "CREATE DATABASE ecommerce_db;"

# Fresh migrations
python manage.py migrate

# Recreate superuser
python manage.py createsuperuser
```

---

## 📚 Next Steps

1. ✅ Database configured and running
2. ✅ Backend API running on http://localhost:8000
3. ✅ Frontend running on http://localhost:3000
4. 📖 Read [SETUP_GUIDE.md](./SETUP_GUIDE.md) for advanced configuration
5. 🚀 See [DEPLOYMENT.md](./DEPLOYMENT.md) for production setup

---

## 🎯 Key Endpoints to Test

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Register new user |
| `/api/auth/login/` | POST | Login with email/password |
| `/api/auth/google_login/` | POST | Login with Google OAuth |
| `/api/products/` | GET | List all products |
| `/api/cart/view/` | GET | View shopping cart |
| `/api/orders/` | GET | List user orders |
| `/admin/` | GET | Django admin panel |
| `/api/docs/` | GET | API documentation |

---

## ✅ Checklist

- [ ] PostgreSQL installed and running
- [ ] Backend virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with correct database credentials
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Backend running on http://localhost:8000
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Frontend running on http://localhost:3000
- [ ] Google OAuth credentials added to `.env`
- [ ] API endpoints tested in Swagger UI

---

## 🆘 Need More Help?

- Check [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed API documentation
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for production setup
- Check `/backend/README.md` for backend-specific issues
- Check `/frontend/README.md` for frontend-specific issues

**Happy coding!** 🎉
```powershell
psql -U postgres
```

3. **Enter PostgreSQL shell and run:**
```sql
-- Create database
CREATE DATABASE ecommerce_db;

-- Create user
CREATE USER ecommerce_user WITH PASSWORD 'password123';

-- Configure user
ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read_committed';
ALTER ROLE ecommerce_user SET default_transaction_deferrable TO on;
ALTER ROLE ecommerce_user SET timezone TO 'UTC';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;

-- Exit
\q
```

#### macOS / Linux:

```bash
# Connect to PostgreSQL
psql postgres

# Run the same SQL commands as above
```

---

### Step 2: Backend Configuration

#### 2.1 Navigate to Backend:
```bash
cd e-com/backend
```

#### 2.2 Create Virtual Environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 Install Dependencies:
```bash
pip install -r requirements.txt
```

#### 2.4 Configure Environment Variables:

**Create `.env` file:**
```env
# ============================================
# DJANGO SETTINGS
# ============================================
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production-12345678901234567
ALLOWED_HOSTS=localhost,127.0.0.1

# ============================================
# DATABASE CONFIGURATION (PostgreSQL Only)
# ============================================
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=password123
DB_HOST=localhost
DB_PORT=5432

# ============================================
# CORS SETTINGS (Frontend URL)
# ============================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# ============================================
# JWT SECRET
# ============================================
JWT_SECRET=your-jwt-secret-key

# ============================================
# PAYMENT GATEWAY (Optional for testing)
# ============================================
STRIPE_PUBLIC_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key

# ============================================
# EMAIL SETTINGS (Optional)
# ============================================
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### 2.5 Run Database Migrations:
```bash
# Create migration files from models
python manage.py makemigrations

# Apply migrations to PostgreSQL
python manage.py migrate
```

**Expected Output:**
```
Applying sessions.0001_initial... OK
Applying admin.0001_initial... OK
Applying admin.0002_logentry_remove_auto_add... OK
...
Applying users.0001_initial... OK
...
```

#### 2.6 Create Superuser (Admin Account):
```bash
python manage.py createsuperuser
```

**Example:**
```
Username: admin
Email: admin@example.com
Password: ••••••••
Password (again): ••••••••
Superuser created successfully.
```

#### 2.7 (Optional) Load Sample Data:
```bash
python manage.py loaddata fixtures/sample_data.json
```

#### 2.8 Run Development Server:
```bash
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### Step 3: Access Django Admin

1. **Go to:** http://localhost:8000/admin/
2. **Login with superuser credentials** created in Step 2.6
3. **You should see:**
   - Users
   - Products
   - Orders
   - Payments
   - Reviews
   - Cart Items
   - All other models

### Step 4: Frontend Configuration

#### 4.1 Navigate to Frontend:
```bash
cd ../frontend
```

#### 4.2 Install Dependencies:
```bash
npm install
```

#### 4.3 Check `api.js` Configuration:

File: `/frontend/utils/api.js`

Verify backend URL is correct:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

#### 4.4 Run Development Server:
```bash
npm run dev
```

**Expected Output:**
```
> next dev

ready - started server at 0.0.0.0:3000, url: http://localhost:3000
```

#### 4.5 Access Frontend:
1. **Go to:** http://localhost:3000
2. **Browse products, add to cart, checkout**
3. **Use Django admin to manage inventory**

---

## 🛠️ Common Commands

### Django Backend Commands:

```bash
# Navigate to backend
cd backend

# Activate virtual environment
venv\Scripts\activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Create new migration files
python manage.py makemigrations

# Show migration status
python manage.py showmigrations

# Check Django setup
python manage.py check

# Create dummy data
python manage.py shell
# Then in Python shell:
# from apps.products.models import Product, Category
# Category.objects.create(name='Electronics')
```

### Next.js Frontend Commands:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Format code
npm run format
```

### PostgreSQL Commands:

```bash
# Connect to PostgreSQL
psql -U postgres

# List all databases
\l

# Connect to database
\c ecommerce_db

# List all tables
\dt

# Describe table structure
\d products_product

# Exit
\q
```

---

## 🧪 Testing the Setup

### 1. Test Backend:
```bash
cd backend
python manage.py check

# Expected: System check identified no issues (0 silenced).
```

### 2. Test Database Connection:
```bash
python manage.py shell
```

In Python shell:
```python
from apps.products.models import Product
Product.objects.count()
# Should return: 0 (or number of products if sample data loaded)

exit()
```

### 3. Test Frontend API Call:
In browser console (http://localhost:3000):
```javascript
fetch('http://localhost:8000/api/products/')
  .then(r => r.json())
  .then(data => console.log(data))
```

---

## 📊 User Roles

### 1. **Website Visitors (No account)**
- Browse products
- View product details
- Add to cart (local storage only)

### 2. **Registered Users**
- Create account (sign up)
- Login
- Persistent cart
- Wishlist
- Order history
- Reviews and ratings
- Saved addresses

### 3. **Admin Users**
- Create/Edit/Delete products
- Manage categories and brands
- View and manage orders
- Track payments
- Manage customers
- View analytics
- Moderate reviews
- Create coupons

---

## 🔐 Security Checklist

### Before Production:

- [ ] Change SECRET_KEY in `.env`
- [ ] Set `DEBUG = False` in `.env`
- [ ] Create strong database password
- [ ] Use environment-specific `.env` files
- [ ] Setup HTTPS/SSL certificate
- [ ] Enable CSRF protection
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Use strong admin password
- [ ] Setup email service
- [ ] Enable rate limiting on APIs
- [ ] Configure security headers
- [ ] Use PostgreSQL (not SQLite)
- [ ] Backup database regularly

---

## 📁 Project Structure

```
e-com/
├── backend/
│   ├── ecommerce/           # Django project settings
│   ├── apps/                # Django applications
│   │   ├── products/        # Product management
│   │   ├── orders/          # Order management
│   │   ├── payments/        # Payment processing
│   │   ├── users/           # User authentication
│   │   ├── cart/            # Shopping cart
│   │   ├── reviews/         # Product reviews
│   │   └── ...
│   ├── static/              # Static files
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
└── frontend/
    ├── pages/               # Next.js pages
    ├── components/          # Reusable components
    ├── store/               # Zustand state management
    ├── utils/               # Utility functions
    ├── styles/              # Tailwind CSS
    ├── public/              # Static assets
    ├── package.json
    └── next.config.js
```

---

## 🐛 Troubleshooting

### Problem: "Database connection refused"

**Solution:**
1. Verify PostgreSQL is running
2. Check database credentials in `.env`
3. Ensure database exists:
   ```bash
   psql -U postgres -c "\l"
   ```

### Problem: "Port 8000 already in use"

**Solution:**
```bash
# Use different port
python manage.py runserver 8001
```

### Problem: "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# For frontend
npm install --force
```

### Problem: "No products showing in admin"

**Solution:**
1. Run migrations: `python manage.py migrate`
2. Create sample data via Django shell
3. Reload admin page

### Problem: Frontend can't connect to backend

**Solution:**
1. Verify backend is running on http://localhost:8000
2. Check CORS settings in `.env`
3. Check browser console for CORS errors
4. Verify API endpoint in `/frontend/utils/api.js`

---

## 📞 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

## ✅ Setup Complete!

Your e-commerce project is now ready for development and testing!

**Quick Links:**
- Frontend: http://localhost:3000
- Backend Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/

Happy coding! 🚀

