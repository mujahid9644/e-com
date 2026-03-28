# E-Commerce Platform - Modern, Full-Featured

A production-ready e-commerce platform built with **Django REST Framework**, **PostgreSQL**, **Next.js**, and **Google OAuth**.

## ✨ Features

✅ **User Authentication**: JWT + Google OAuth Easy Login
✅ **Product Catalog**: Advanced filtering, search, and categorization
✅ **Shopping Cart**: Full cart management with wishlist
✅ **Orders**: Order creation, tracking, and cancellation
✅ **Reviews**: Product reviews with ratings and helpful votes
✅ **Payments**: Stripe, bKash, Nagad integration
✅ **Admin Dashboard**: Comprehensive management interface
✅ **Responsive UI**: TailwindCSS + Framer Motion animations
✅ **Cloud Storage**: Cloudinary integration for images

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Node.js 16+

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows or source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
# Edit .env with PostgreSQL credentials and API keys

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend: http://localhost:8000
API Docs: http://localhost:8000/api/docs/
Admin: http://localhost:8000/admin/

### Frontend Setup

```bash
cd frontend
npm install
copy .env.example .env.local
npm run dev
```

Frontend: http://localhost:3000

---

## 📁 Project Structure

```
e-com/
├── backend/
│   ├── apps/
│   │   ├── users/      # Authentication & profiles
│   │   ├── products/   # Product management
│   │   ├── cart/       # Cart & wishlist
│   │   ├── orders/     # Order system
│   │   ├── payments/   # Payment processing
│   │   └── reviews/    # Reviews & ratings
│   ├── ecommerce/      # Django settings
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── pages/          # Next.js routes
│   ├── components/     # React components
│   ├── store/          # Zustand state
│   ├── utils/          # Helpers
│   └── package.json
├── README.md           # This file
├── SETUP_GUIDE.md      # Detailed setup
└── DEPLOYMENT.md       # Production deployment
```

---

## 🔐 Environment Setup

### Backend .env

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Frontend
FRONTEND_URL=http://localhost:3000

# JWT
JWT_SECRET=your-jwt-secret

# Google OAuth (from Google Cloud Console)
GOOGLE_OAUTH_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your_secret

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret

# Stripe
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
```

---

## 🔑 API Endpoints

### Authentication
```
POST   /api/auth/register/
POST   /api/auth/login/
POST   /api/auth/google_login/          # Google OAuth
GET    /api/auth/profile/me/
PUT    /api/auth/profile/update_profile/
```

### Products
```
GET    /api/products/                   # List with filters
GET    /api/products/{id}/
GET    /api/products/{id}/reviews/
GET    /api/products/categories/
```

### Cart & Orders
```
GET    /api/cart/view/
POST   /api/cart/add/
POST   /api/cart/remove/
GET    /api/orders/
POST   /api/orders/create/
```

### Reviews
```
GET    /api/reviews/
POST   /api/reviews/
PUT    /api/reviews/{id}/
DELETE /api/reviews/{id}/
```

---

## 🔐 Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 Client ID (Web Application)
3. Add redirect URIs: `http://localhost:8000/`, `http://localhost:3000/`
4. Add credentials to `.env`:
   ```env
   GOOGLE_OAUTH_CLIENT_ID=xxx.apps.googleusercontent.com
   GOOGLE_OAUTH_CLIENT_SECRET=your_secret
   ```

### Frontend Usage
```javascript
const handleGoogleLogin = async (token) => {
  const response = await fetch('http://localhost:8000/api/auth/google_login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ access_token: token })
  });
  
  const data = await response.json();
  localStorage.setItem('access_token', data.tokens.access);
};
```

---

## 📊 Database

### Setup PostgreSQL

```bash
# Create database
createdb ecommerce_db

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

---

## 🧪 Testing APIs

### Swagger UI
Visit: http://localhost:8000/api/docs/

### Using Curl
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"testuser","password":"Test@123","password_confirm":"Test@123"}'

# Get Products
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🚢 Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete deployment guide with:
- Docker setup
- Linux server configuration
- Nginx + Gunicorn
- SSL/HTTPS
- Database backups
- Monitoring

---

## 📖 Detailed Documentation

- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Comprehensive setup with all details
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Production deployment guide
- **[backend/README.md](./backend/README.md)** - Backend-specific documentation
- **[frontend/README.md](./frontend/README.md)** - Frontend-specific documentation

---

## 🐛 Common Issues

### PostgreSQL Connection Failed
```bash
# Check PostgreSQL is running and update .env with correct credentials
psql -U postgres -c "SELECT 1;"
```

### Migrations Error
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

### CORS Issues
Update `CORS_ALLOWED_ORIGINS` in `.env` with your frontend URL.

---

## 🔗 Useful Resources

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Next.js Docs](https://nextjs.org/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Stripe Integration](https://stripe.com/docs)
- [Google OAuth](https://developers.google.com/identity/protocols/oauth2)

---

## 📄 License

MIT License - Feel free to use for commercial projects

---

## 🆘 Need Help?

Refer to the detailed documentation files or check specific app READMEs in the backend/frontend directories.

**Happy coding!** 🎉

## 🔑 Key Features

### Authentication ✅
- User registration and login
- JWT token-based authentication
- Secure password hashing
- User profiles and preferences
- Address management

### Products ✅
- Product catalog with images
- Category and brand management
- Product filtering and search
- Discounts and pricing
- Stock management
- Featured products

### Shopping ✅
- Shopping cart management
- Wishlist functionality
- Product quantity adjustments
- Cart persistence

### Orders ✅
- Order creation and tracking
- Multiple payment methods
- Order status management
- Shipment tracking
- Return/refund requests

### Reviews ✅
- Product ratings (1-5 stars)
- Customer reviews
- Review images
- Helpful/unhelpful voting
- Verified purchase badge

### Payments ✅
- Stripe integration
- bKash payment gateway
- Nagad payment gateway
- Coupon/discount system
- Order total calculations with tax

### Admin Dashboard ✅
- Product management
- Order management
- User management
- Sales analytics
- Coupon management

## 📚 API Endpoints Summary

### Authentication
```
POST   /api/auth/register/           # Register user
POST   /api/auth/login/              # Login user
GET    /api/auth/profile/me/         # Get current user
PUT    /api/auth/profile/update_profile/  # Update profile
POST   /api/auth/profile/change_password/ # Change password
```

### Products
```
GET    /api/products/                # List products (with filters)
GET    /api/products/{slug}/         # Product details
GET    /api/products/categories/     # List categories
GET    /api/products/brands/         # List brands
GET    /api/products/featured/       # Featured products
```

### Cart & Wishlist
```
GET    /api/cart/view/               # View cart
POST   /api/cart/add/                # Add to cart
POST   /api/cart/remove/             # Remove from cart
POST   /api/cart/clear/              # Clear cart
GET    /api/cart/wishlist/view/      # View wishlist
POST   /api/cart/wishlist/add/       # Add to wishlist
```

### Orders
```
GET    /api/orders/                  # List user orders
POST   /api/orders/create/           # Create order
GET    /api/orders/{id}/             # Order details
POST   /api/orders/{id}/cancel/      # Cancel order
GET    /api/orders/{id}/tracking/    # Tracking info
```

### Reviews
```
GET    /api/reviews/                 # List reviews
POST   /api/reviews/                 # Create review
POST   /api/reviews/{id}/mark_helpful/ # Mark helpful
```

### Payments
```
POST   /api/payments/validate_coupon/  # Validate coupon
POST   /api/payments/apply_coupon/     # Apply coupon
GET    /api/payments/coupons/          # List coupons
```

**Full API documentation**: See `backend/README.md`

## 🎨 Frontend Components

### Key Components
- `Layout` - Main layout wrapper
- `Header` - Navigation header with search
- `ProductCard` - Product display with animations
- `SearchBar` - Product search
- `Footer` - Application footer
- `SkeletonGrid` - Loading placeholders

### Pages
- `/` - Home page with featured products
- `/products` - Products listing with filters
- `/products/[slug]` - Product details
- `/login` - Login page
- `/signup` - Registration page
- `/cart` - Shopping cart
- `/checkout` - Checkout page
- `/dashboard` - User dashboard
- `/orders` - Order history
- `/wishlist` - Wishlist

**Full frontend documentation**: See `frontend/README.md`

## 🗄️ Database Models

### Users
- `CustomUser` - Extended user with phone, profile picture
- `Address` - Shipping/billing addresses
- `UserPreferences` - User settings

### Products
- `Category` - Product categories
- `Brand` - Product brands
- `Product` - Main product model
- `ProductImage` - Gallery images
- `ProductAttribute` - Size, color, etc.

### Orders
- `Order` - Order record
- `OrderItem` - Items in order
- `OrderShipment` - Shipment tracking
- `OrderReturn` - Returns/refunds

### Cart
- `Cart` - User shopping cart
- `CartItem` - Items in cart
- `Wishlist` - User wishlist

### Reviews & Payments
- `ProductReview` - Customer reviews
- `ReviewImage` - Review photos
- `Payment` - Payment records
- `Coupon` - Discount codes

## 🔐 Security Features

- ✅ JWT token authentication
- ✅ CORS configuration
- ✅ CSRF protection
- ✅ SQL injection prevention (Django ORM)
- ✅ Secure password hashing
- ✅ Rate limiting support
- ✅ Environment variable protection

## 📦 Deployment

### Backend Deployment
1. Use PostgreSQL in production
2. Set `DEBUG = False` in settings
3. Generate strong `SECRET_KEY`
4. Configure ALLOWED_HOSTS
5. Use Gunicorn or similar WSGI server
6. Set up Nginx reverse proxy
7. Enable HTTPS/SSL

### Frontend Deployment
1. Build: `npm run build`
2. Deploy to Vercel, Netlify, or own server
3. Configure environment variables
4. Enable caching headers

## 🛠️ Development Tips

### Adding a New Page
1. Create file in `frontend/pages/newpage.jsx`
2. Import Layout and other components
3. Add to navigation if needed

### Adding New API Endpoint
1. Create serializer in `backend/apps/yourapp/serializers.py`
2. Create view in `backend/apps/yourapp/views.py`
3. Register in `backend/apps/yourapp/urls.py`
4. Import in main `backend/ecommerce/urls.py`

### Styling with Tailwind
- Use `glass` class for glassmorphism effect
- Use `gradient-text` for gradient text
- Use `gradient-button` for styled buttons
- Extend in `tailwind.config.js`

### State Management
- Use `useAuthStore()` for authentication
- Use `useCartStore()` for shopping cart
- Zustand stores auto-save to localStorage

## 📊 Database Diagrams

### User Flow
```
User → Register/Login → Get JWT Token → Access Protected Routes
```

### Product Flow
```
Category/Brand → Product → ProductImage → Review → Order
```

### Order Flow
```
Cart → Order → Payment → OrderShipment → Delivered
```

## 🐛 Common Issues & Solutions

### Backend Issues

**Port 8000 already in use**
```bash
python manage.py runserver 8001
```

**Database connection error**
```bash
# Check PostgreSQL is running and credentials are correct in .env
# Verify DATABASES setting in settings.py
```

**CORS errors**
```python
# Add your frontend URL to CORS_ALLOWED_ORIGINS in settings.py
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
```

### Frontend Issues

**API calls failing**
```bash
# Check backend URL in .env.local
# Verify backend is running
# Check browser console for errors
```

**Components not rendering**
```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install && npm run dev
```

## 🎯 Next Steps

1. **Customize branding** - Update logo, colors, company name
2. **Add payment integration** - Configure Stripe, bKash, Nagad
3. **Setup email** - Configure SMTP for order notifications
4. **Add analytics** - Integrate Google Analytics or similar
5. **Optimize images** - Use CDN for product images
6. **Setup monitoring** - Add error tracking (Sentry)
7. **Performance testing** - Load testing and optimization

## 📞 Support & Resources

### Documentation
- **Backend**: `/backend/README.md` - Django setup & API endpoints
- **Frontend**: `/frontend/README.md` - Next.js setup & components

### Official Docs
- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Next.js: https://nextjs.org/docs
- React: https://react.dev
- Tailwind: https://tailwindcss.com/docs

### External APIs
- Stripe: https://stripe.com/docs
- PostGRES: https://www.postgresql.org/docs/

## 📄 License

This e-commerce platform is provided as a learning resource and template.

---

## 🎉 Getting Help

If you encounter any issues:
1. Check the relevant README (backend or frontend)
2. Review error messages in console/logs
3. Verify environment variables are set correctly
4. Ensure all dependencies are installed
5. Check that ports are not already in use

---

**Ready to launch your e-commerce platform! 🚀**

*Last Updated: 2024*
