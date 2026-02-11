# Hungrio 🍽️ – Modern Food Ordering Platform

Full-stack **restaurant food ordering system** with secure payments, real-time ready architecture, and production-grade security.

## 🌐 Live Demo (Working)

👉 **https://hungrio-production.up.railway.app/**

Try it live:
- Browse menu as guest
- Login / Signup with CAPTCHA protection
- Add to cart & wishlist
- Checkout with **Stripe test card**
- See order confirmation + email

**Test Card:** 4242 4242 4242 4242 | Any future date | Any CVC

## 🔥 Standout Features

- **Live on Railway** with PostgreSQL + Redis
- **Stripe Payments** – full checkout + webhook support
- **JWT Authentication** + CAPTCHA protection on login
- **Content Security Policy (CSP)** – strong XSS protection
- **Rate Limiting** on APIs (100/min user, 1000/day anon)
- **CORS & CSRF** configured for secure frontend-backend
- **Celery + Redis** – ready for background tasks & scheduled jobs
- **Django Channels** – real-time order updates possible
- **Transactional Emails** via Brevo (order confirmation)
- **Whitenoise** – efficient static file serving
- **Modular app structure** – clean & scalable (15+ apps)
- Beautiful **responsive frontend** with mobile-first design

## 📸 Screenshots

<p align="center">
  <img src="photos/guest home page.jpeg" width="32%" alt="Guest Home Page" />
  <img src="photos/users cart view.jpeg" width="32%" alt="User Cart" />
  <img src="photos/users wishlist.jpeg" width="32%" alt="Wishlist" />
</p>

<p align="center">
  <img src="photos/checkout to payment page order initiated.jpeg" width="32%" alt="Checkout" />
  <img src="photos/stripe demo card detail insertion.jpeg" width="32%" alt="Stripe Payment" />
  <img src="photos/payment done.jpeg" width="32%" alt="Payment Success" />
</p>

<p align="center">
  <img src="photos/order confirmation details with payment id and order id.jpeg" width="32%" alt="Order Confirmation" />
  <img src="photos/order confirmation email on gmail.jpeg" width="32%" alt="Order Email" />
  <img src="photos/captcha proetection.jpeg" width="32%" alt="CAPTCHA Protection" />
</p>

## 🛠 Tech Stack

- **Backend**: Django 5.x, Django REST Framework, Simple JWT
- **Database**: PostgreSQL (Railway)
- **Payments**: Stripe (with webhooks)
- **Real-time**: Django Channels + Redis
- **Tasks**: Celery + Celery Beat
- **Email**: Brevo (Sendinblue) SMTP/API
- **Security**: CSP, Rate Limiting, CAPTCHA, CORS
- **Frontend**: Django Templates + Custom CSS/JS
- **Deployment**: Railway.app (Procfile + runtime.txt)
- **Static Files**: Whitenoise (compressed)

## 🚀 Quick Local Setup

```bash
git clone https://github.com/shaanMS/Hungrio.git
cd Hungrio/restaurant

# Install dependencies
pip install -r requirements.txt

# Migrate
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run
python manage.py runserver