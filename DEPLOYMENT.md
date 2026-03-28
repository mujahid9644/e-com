# Production Deployment Guide

## 🚀 Pre-Deployment Checklist

- [ ] Database backup configured
- [ ] DEBUG=False in environment
- [ ] SECRET_KEY changed and secured
- [ ] ALLOWED_HOSTS configured properly
- [ ] HTTPS/SSL certificate obtained
- [ ] Environment variables secured
- [ ] Static/Media files configured
- [ ] Email service configured
- [ ] Payment gateway keys added
- [ ] Google OAuth credentials added
- [ ] Logging configured
- [ ] Database migrations completed

---

## 🐳 Docker Deployment

### Dockerfile (Backend)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y postgresql-client

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ecommerce_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    command: gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000 --workers 4
    environment:
      - DEBUG=False
      - DB_ENGINE=django.db.backends.postgresql
      - DB_NAME=ecommerce_db
      - DB_USER=postgres
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=postgres
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api

volumes:
  postgres_data:
```

---

## 🔧 Manual Linux Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv postgresql nginx supervisor git

# Create app user
sudo useradd -m appuser
sudo su - appuser
```

### 2. Clone & Setup Backend

```bash
git clone <repo-url> e-commerce
cd e-commerce/backend

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Edit .env with production settings
nano .env

python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 3. Configure Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/ecommerce-backend.service
```

**Content:**

```ini
[Unit]
Description=E-Commerce Backend Gunicorn
After=network.target

[Service]
User=appuser
Group=www-data
WorkingDirectory=/home/appuser/e-commerce/backend
ExecStart=/home/appuser/e-commerce/backend/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:8001 \
    ecommerce.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ecommerce-backend
sudo systemctl start ecommerce-backend
```

### 4. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/ecommerce
```

**Content:**

```nginx
upstream ecommerce_backend {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates (from Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;

    # Backend API
    location /api/ {
        proxy_pass http://ecommerce_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /home/appuser/e-commerce/backend/staticfiles/;
        expires 30d;
    }

    # Media files
    location /media/ {
        alias /home/appuser/e-commerce/backend/media/;
        expires 7d;
    }
}
```

```bash
# Enable configuration
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/

# Test Nginx
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 5. SSL Certificate (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## 📊 Production Settings

### Django Settings (.env)

```env
DEBUG=False
SECRET_KEY=your-super-secret-production-key

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=db_user
DB_PASSWORD=strong_password
DB_HOST=db.example.com

# Security
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## 📈 Monitoring & Maintenance

### Database Backups

```bash
# Backup
pg_dump ecommerce_db > backup_$(date +%Y%m%d).sql

# Restore
psql ecommerce_db < backup_20240101.sql
```

---

## ✅ Post-Deployment Verification

- [ ] Frontend loads without errors
- [ ] Login/Registration works
- [ ] Google OAuth login works
- [ ] API endpoints respond correctly
- [ ] Static/Media files serve properly
- [ ] HTTPS redirects work

## 🔐 Security Configuration

### 1. Update Django Settings (production)

```python
# backend/core/settings/prod.py

DEBUG = False
ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'api.yourdomain.com',
]

# Generate new SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set!")

# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}

# HTTPS only
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

---

## 🗄️ Database Setup (PostgreSQL)

### On Production Server:

```bash
# 1. Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# 2. Create database and user
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE ecommerce_db;
CREATE USER ecommerce_user WITH PASSWORD 'secure_password_here';
ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecommerce_user SET default_transaction_deferrable TO on;
ALTER ROLE ecommerce_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q  # Exit
```

### Update .env on Production:

```
DATABASE_URL=postgresql://ecommerce_user:secure_password_here@localhost:5432/ecommerce_db
```

---

## 🚀 Backend Deployment (Gunicorn + Nginx)

### Step 1: Install Gunicorn

```bash
cd backend
pip install gunicorn
```

### Step 2: Create Gunicorn Service

```bash
# Create system service
sudo nano /etc/systemd/system/ecommerce-gunicorn.service
```

Paste:
```ini
[Unit]
Description=Gunicorn for E-Commerce API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/ubuntu/e-com/backend
ExecStart=/home/ubuntu/e-com/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/gunicorn.sock \
    core.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ecommerce-gunicorn
sudo systemctl start ecommerce-gunicorn
```

### Step 3: Set Up Nginx

```bash
sudo nano /etc/nginx/sites-available/ecommerce
```

Paste (update domain!):
```nginx
upstream gunicorn {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /home/ubuntu/e-com/backend/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/e-com/backend/media/;
    }

    location / {
        proxy_pass http://gunicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable and test:
```bash
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔐 SSL/HTTPS Setup (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate (auto-configure Nginx)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## 📦 Frontend Deployment (Next.js)

### Option 1: Vercel (EASIEST - Recommended)

1. Push code to GitHub
2. Go to https://vercel.com
3. Click "New Project"
4. Import your GitHub repo
5. Set `NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api`
6. Deploy!

The frontend auto-scales and has free HTTPS.

### Option 2: Self-Hosted (Nginx)

```bash
cd frontend
npm run build

# Copy to server
scp -r .next/* user@server:/var/www/ecommerce/next/

# Run with PM2
npm install -g pm2
pm2 start "npm run start" --name "ecommerce-frontend"
pm2 startup
pm2 save
```

---

## 📊 Static Files Setup

```bash
cd backend

# Collect all static files
python manage.py collectstatic --noinput

# Files go to: backend/staticfiles/
# Nginx serves from there
```

---

## 📋 Environment Variables (Production)

Create `.env` on production server:

```
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-production-secret-key-here

DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_db

ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email (Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Payment Gateways
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
BKASH_APP_KEY=...
NAGAD_MERCHANT_ID=...

# AWS S3 (for images)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET_NAME=ecommerce-images
```

---

## 🛡️ Database Backups

### Automated Daily Backup:

```bash
# Create backup script
sudo nano /home/ubuntu/backup_db.sh
```

Paste:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ubuntu/backups"
mkdir -p $BACKUP_DIR

pg_dump ecommerce_db > $BACKUP_DIR/db_backup_$DATE.sql
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +30 -delete

# Upload to S3 (optional)
# aws s3 cp $BACKUP_DIR/db_backup_$DATE.sql.gz s3://your-bucket/backups/
```

Schedule with cron:
```bash
# Run daily at 2 AM
sudo crontab -e
0 2 * * * /home/ubuntu/backup_db.sh
```

---

## 📊 Monitoring & Logging

### 1. Django Error Tracking (Sentry)

```python
# backend/core/settings/prod.py
import sentry_sdk

sentry_sdk.init(
    dsn="https://your-sentry-key@sentry.io/your-project",
    traces_sample_rate=0.1,
    environment="production"
)
```

### 2. Server Monitoring

```bash
# Install monitoring
sudo apt install glances

# View system status
glances

# Or install Prometheus + Grafana for advanced monitoring
```

### 3. Log Aggregation

Application stores logs in `/var/log/`:
```bash
# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# View Django logs
tail -f /home/ubuntu/e-com/backend/logs/django.log
```

---

## 🧪 Pre-Production Testing

```bash
# Test with production settings
python manage.py runserver --settings=core.settings.prod

# Run migrations
python manage.py migrate --settings=core.settings.prod

# Collect static
python manage.py collectstatic --noinput --settings=core.settings.prod
```

---

## ✅ Deployment Checklist

```
Pre-Deployment:
- [ ] All code committed to Git
- [ ] Database backed up
- [ ] Environment variables set
- [ ] SSL certificate ready
- [ ] SECRET_KEY is unique
- [ ] DEBUG = False

Deployment:
- [ ] Stop old services
- [ ] Pull latest code
- [ ] Install new dependencies
- [ ] Run migrations
- [ ] Collect static files
- [ ] Start services
- [ ] Test all endpoints
- [ ] Monitor for errors

Post-Deployment:
- [ ] Verify website is live
- [ ] Test payment gateway
- [ ] Monitor error logs
- [ ] Check database performance
- [ ] Setup backup verification
- [ ] Test email notifications
- [ ] Monitor API performance
```

---

## 🚨 Urgent Issues Post-Deployment

### Website shows "502 Bad Gateway"
```bash
# Check Gunicorn
sudo service ecommerce-gunicorn status

# Restart
sudo service ecommerce-gunicorn restart

# Check for errors
sudo journalctl -u ecommerce-gunicorn -n 20
```

### Images not loading
```bash
# Check static files
python manage.py collectstatic --noinput

# Check permissions
sudo chown -R www-data:www-data /home/ubuntu/e-com/backend/media/
chmod -R 755 /home/ubuntu/e-com/backend/media/
```

### Database connection error
```bash
# Test connection
psql -U ecommerce_user -d ecommerce_db -c "SELECT 1;"

# Check .env DATABASE_URL
cat /home/ubuntu/e-com/backend/.env | grep DATABASE_URL
```

---

## 📞 Support & Monitoring

Regular checks:
- [ ] Daily: Check error logs
- [ ] Weekly: Verify backups
- [ ] Monthly: Review performance metrics
- [ ] Monthly: Update security patches

---

## 📖 Quick Reference

| Task | Command |
|------|---------|
| Start Django | `sudo service ecommerce-gunicorn start` |
| Restart Django | `sudo service ecommerce-gunicorn restart` |
| View logs | `sudo journalctl -u ecommerce-gunicorn -f` |
| Restart Nginx | `sudo service nginx restart` |
| Database backup | `pg_dump ecommerce_db > backup.sql` |
| SSH into server | `ssh ubuntu@your-server-ip` |

---

**Last Updated**: March 2026
**Status**: Production Ready
