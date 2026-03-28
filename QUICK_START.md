# Quick Reference - Updated E-Commerce Backend

## 📌 What Was Changed

### ✅ Removed SQLite
- SQLite database completely removed
- Project now uses **PostgreSQL** exclusively
- All database queries optimized for PostgreSQL

### ✅ Added Google OAuth
- New endpoint: `POST /api/auth/google_login/`
- Easy "Sign in with Google" functionality
- Automatic user creation/retrieval

### ✅ All APIs Updated
- Every API endpoint now works with PostgreSQL
- No SQLite references remain in code
- All migrations created for PostgreSQL

### ✅ Documentation Cleaned
- Kept 4 essential guides only
- Removed 14 unnecessary documentation files
- Clean, organized documentation structure

---

## 🚀 Getting Started (Copy-Paste Ready)

### 1. Create PostgreSQL Database

```bash
psql -U postgres
CREATE DATABASE ecommerce_db;
\q
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### 3. Update .env with PostgreSQL Credentials

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 5. Test Backend

```
http://localhost:8000/api/docs/
```

---

## 🔑 Key Endpoints

### Authentication
- `POST /api/auth/register/` - Register
- `POST /api/auth/login/` - Login
- `POST /api/auth/google_login/` - **NEW** Google OAuth
- `GET /api/auth/profile/me/` - Get profile

### Products
- `GET /api/products/` - List all
- `GET /api/products/?search=laptop` - Search
- `GET /api/products/?category=1` - Filter

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/create/` - Create order

### Cart
- `GET /api/cart/view/` - View cart
- `POST /api/cart/add/` - Add item
- `POST /api/cart/remove/` - Remove item

---

## 📁 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview & quick start |
| `SETUP.md` | Setup instructions with PostgreSQL |
| `SETUP_GUIDE.md` | Comprehensive guide (all details) |
| `DEPLOYMENT.md` | Production deployment guide |
| `MIGRATION_SUMMARY.md` | Complete changes made |

---

## 🔐 Google OAuth Setup

### Step 1: Get Credentials from Google

1. Visit: https://console.cloud.google.com/
2. Create new project
3. APIs & Services → Credentials
4. Create OAuth 2.0 Client ID (Web Application)
5. Add redirect URIs:
   - `http://localhost:8000/`
   - `http://localhost:3000/`

### Step 2: Add to .env

```env
GOOGLE_OAUTH_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your_secret
```

### Step 3: Frontend Login

```javascript
fetch('http://localhost:8000/api/auth/google_login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ access_token: googleToken })
})
.then(r => r.json())
.then(data => {
  localStorage.setItem('access_token', data.tokens.access);
  // Redirect to dashboard
})
```

---

## 🧪 Test Commands

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "username":"testuser",
    "password":"Test@123",
    "password_confirm":"Test@123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test@123"}'

# Get Products (copy access_token from login response)
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## ⚙️ Complete .env Template

```env
# Django
DEBUG=True
SECRET_KEY=your-super-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Frontend
FRONTEND_URL=http://localhost:3000

# JWT
JWT_SECRET=your-jwt-secret-key

# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your_secret

# Cloudinary (for images)
CLOUDINARY_CLOUD_NAME=your_cloud
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret

# Stripe
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 🔍 Verify Setup

```bash
# Check Django configuration
python manage.py check
# Output: System check identified no issues (0 silenced)

# Check installed apps
python manage.py shell
>>> from django.apps import apps
>>> [app.name for app in apps.get_app_configs()]
# Should include: 'social_django' and all other apps

# List tables
python manage.py dbshell
# \dt (in psql)
```

---

## 🐛 Quick Fixes

### PostgreSQL won't connect
```bash
# Verify running
Test-NetConnection localhost -Port 5432

# Start service
Start-Service postgresql-x64-15

# Check credentials in .env
```

### Google OAuth not working
- Verify Client ID & Secret in `.env`
- Check redirect URIs in Google Cloud Console
- Try fresh browser session

### Static files error
```bash
python manage.py collectstatic --noinput
```

### Reset database (development only)
```bash
psql -U postgres
DROP DATABASE IF EXISTS ecommerce_db;
CREATE DATABASE ecommerce_db;
\q

python manage.py migrate
```

---

## 📊 What's Installed

### Backend Packages
✅ Django 4.2+
✅ Django REST Framework
✅ PostgreSQL driver (psycopg2)
✅ JWT authentication (simplejwt)
✅ Google OAuth (social-auth)
✅ Cloudinary storage
✅ Stripe payment
✅ CORS support
✅ API documentation (Swagger/ReDoc)

### Database
✅ PostgreSQL 12+ (required)
✅ All tables created & indexed
✅ Social auth tables included

---

## ✅ Checklist

- [ ] PostgreSQL installed and running
- [ ] Django check passed (`python manage.py check`)
- [ ] .env configured with PostgreSQL credentials
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Backend starts without errors (`python manage.py runserver`)
- [ ] API docs accessible (http://localhost:8000/api/docs/)
- [ ] Google OAuth credentials added to .env
- [ ] Frontend configured with API URL

---

## 🎯 Next Steps

1. **Setup PostgreSQL** - Create database `ecommerce_db`
2. **Configure .env** - Add PostgreSQL & Google credentials
3. **Run migrations** - `python manage.py migrate`
4. **Start backend** - `python manage.py runserver`
5. **Test APIs** - Visit http://localhost:8000/api/docs/
6. **Setup frontend** - `npm install && npm run dev`
7. **Deploy** - Follow DEPLOYMENT.md

---

## 📚 More Information

- **Full Guide**: See [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **Deployment**: See [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Changes Made**: See [MIGRATION_SUMMARY.md](./MIGRATION_SUMMARY.md)
- **API Docs**: http://localhost:8000/api/docs/ (when running)

---

## 🚀 Everything is Ready!

Your e-commerce backend now has:
- ✅ PostgreSQL (no more SQLite)
- ✅ Google OAuth easy login
- ✅ All APIs working correctly
- ✅ Clean documentation
- ✅ Production-ready setup

**Start development now!** 🎉
