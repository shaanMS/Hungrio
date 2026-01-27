import debug_toolbar  
from csp.constants import NONCE
from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print('\n\n\n\n\n\n')
print(BASE_DIR,'\n\n\n\n\n\n\n----')
load_dotenv(BASE_DIR / ".env") # iske bagair django nhi load nhi karega ok!
print('-------------------  ',BASE_DIR)

#BREVO_SMTP_USER=9e05d3001@smtp-brevo.com
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
SMTP_HOST_KEY_BREVO = os.getenv("SMTP_HOST_KEY_BREVO")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")


#print("Stripe Secret:", STRIPE_SECRET_KEY,'\n',STRIPE_PUBLISHABLE_KEY) 


if not STRIPE_SECRET_KEY:
    raise Exception("STRIPE_SECRET_KEY not set in environment")
    print("Stripe Secret:", STRIPE_SECRET_KEY)  # for debugging purposes


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!




FRONTEND_URL = "http://localhost:9998"
'''
preffered way may be

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:2222")


'''



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ "localhost",
    "127.0.0.1",
    "192.168.29.185",]


# Application definition

INSTALLED_APPS = [
    "jazzmin", 
    # Django core apps (keep these first)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp' ,# django csp , content security policy 
    'corsheaders',
    'rest_framework',      
   
    # -------------------------------
    # Your custom apps (in logical order)
    # -------------------------------
    'restaurant',                     # main/project app (usually has settings, urls, etc.)
    'checkout_and_billing',
    'accounts',                       # users, profiles, authentication
    'customer',                       # customer specific models
    
    'category',                       # categories & subcategories
    'product',                        # products menu
    'stock_and_capacity',             # daily stock, capacity, prices
    
    'cart',                           # shopping cart
    'order',                          # orders
    'order_payment',                 # payments (note: better name would be order_payment)
    'invoice',                        # invoices
    'receipt',                        # receipts (note: spelling → receipt)
    'refund',                         # refund handling
    
    'complaint',                      # customer complaints/feedback
    
    'wishlist',
                # Django REST Framework (sabse important)
    #'corsheaders',                       # CORS headers (frontend se call karne ke liye must)
    'django_ratelimit',                  # Application-level rate limiting
    'django_filters',



    # Channels (real-time features ke liye - order tracking, notifications)
    'channels',

    # Optional but highly recommended for modern JWT auth
    'rest_framework_simplejwt',
    # 'rest_framework_simplejwt.token_blacklist',  # Agar token blacklist karna ho toh add karo

]







MIDDLEWARE = [
   # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

# CONTENT_SECURITY_POLICY = {
#     "DIRECTIVES": {
#         "default-src": ["'self'" , ],

#         "script-src": [
#             "'self'",
#            # "'unsafe-inline'",   # ❗ dev only
#              NONCE,
#           # "'unsafe-eval'",  
#           # "'http://192.168.29.185:2222/static/'",
#             "https://js.stripe.com",
           

#         ],

#         "style-src": [
#             "'self'",
#            # "'unsafe-inline'",   # ❗ dev only
#              NONCE,
#           #  "http://192.168.29.185:2222/static/",
#           #  '',
#              "https://js.stripe.com",
#         ],

#         "img-src": [
#             "'self'",
#             "data:",
#             "blob:",
#             "https://js.stripe.com",
#         ],

#         "font-src": [
#             "'self'",
#             "data:",
#             "https://js.stripe.com",
#         ],
#         "frame-src": [
#     "https://js.stripe.com",
#         ],

#         "connect-src": [
#             "'self'",
#             "http://127.0.0.1:2222",
#             "http://localhost:2222",
#           #  "http://192.168.29.185:2222",
#           #  "http://192.168.29.185:*",
#           #  "http://192.168.29.185:2222/static/",
#              "https://js.stripe.com",
#             '',
#         ],

#         "frame-ancestors": ["'none'"],
#         "base-uri": ["'self'"],
#         "object-src": ["'none'"],
#     }
# }




CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],

        "script-src":[
            "'self'",
             "'unsafe-inline'",
             #  "http://localhost:9998",
            #   "http://127.0.0.1:9998",
            #   "http://127.0.0.1:2222/",
          #  NONCE,
             "https://js.stripe.com",
            "'unsafe-eval'",
        ],

        # "style-src": [
        #     "'self'",
        #   #  NONCE,
        #      "http://localhost:9998",
        #      "http://127.0.0.1:9998",
        #       "https://js.stripe.com",
        #      "https://fonts.googleapis.com",
        #     "https://cdnjs.cloudflare.com",
        # ],
"style-src": ["'self'", "'unsafe-inline'", "http://localhost:9998", "http://127.0.0.1:9998", "https://fonts.googleapis.com", "https://cdnjs.cloudflare.com"],

        "font-src": [
            "'self'",
            "'unsafe-inline'"
            "http://localhost:9998",
             "http://127.0.0.1:9998",
            "https://fonts.gstatic.com",
            "https://cdnjs.cloudflare.com",
            "data:",
        ],

        "img-src": [
            "'self'",
            "data:",
            "blob:",
        ],

        "frame-src": [
            "https://js.stripe.com",
        ],

        "connect-src": [
            "'self'",
            "'unsafe-inline'"
            "http://localhost:9998",
            "http://127.0.0.1:9998",
            "http://localhost", 
            "http://127.0.0.1:2222",
            "https://js.stripe.com",
        ],

        "object-src": ["'none'"],
        "base-uri": ["'self'"],
        "frame-ancestors": ["'none'"],
    }
}








ROOT_URLCONF = "restaurant.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [

            BASE_DIR / "product" / "restaurant_frontend", 
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

#WSGI_APPLICATION = "restaurant.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
       # "NAME": BASE_DIR / "db.sqlite3",
           "NAME" : "restaurant_database",#  --- case lower rakho waise insesitive shayd hota hai 
           "USER" : "postgres",
           "PASSWORD" : "12345",
           "HOST" : "localhost",
           "PORT" : "5432"
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/



STATIC_URL = "/static/" # leading slash for nginx

STATICFILES_DIRS = [
    BASE_DIR / "product" / "restaurant_frontend",  # Agar static files serve karni hain
]

STATIC_ROOT = BASE_DIR / "staticfiles"
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'




# 1. REST Framework Settings (security ke liye important)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # modern JWT
        # 'rest_framework.authentication.TokenAuthentication',       # old style (optional)
        #'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Default: sab endpoints protected
        # Agar kuch public chahiye toh view level pe override karo
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3000/minute',      # Anonymous users (bahut important)
        'user': '100/minute',     # Logged-in users
        'login': '100/minute',     # Login endpoint ke liye (brute-force rokne ke liye)
    },
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}
INSTALLED_APPS += [
    "django_celery_beat",
]

# 2. CORS Settings (frontend ke liye must)
CORS_ALLOW_ALL_ORIGINS = False  # Production mein False rakho
CORS_ALLOWED_ORIGINS = [
    "http://localhost:2222",
     "http://127.0.0.1:2222",
    "http://localhost:9998",
    "http://127.0.0.1:9998",
]
CORS_ALLOW_CREDENTIALS = False

# 3. Channels (WebSockets)
ASGI_APPLICATION = 'restaurant.asgi.application'  # project ke asgi.py file ka path
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # Redis server chahiye
        },
    },
}

# 4. Rate limit settings (django-ratelimit ke liye)
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'  # ya redis use karo


# django-ratelimit के warning को suppress (temporary)
SILENCED_SYSTEM_CHECKS = ['django_ratelimit.E003', 'django_ratelimit.W001']


CSRF_COOKIE_SECURE = False  # True in production
CSRF_COOKIE_HTTPONLY = False  # JavaScript se access करने के लिए
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:2222",
    "http://127.0.0.1:2222",
]
SESSION_COOKIE_SECURE = False  # True in production
SESSION_COOKIE_SAMESITE = 'Lax'  # 'None' agar cross-site cookies chahiye

JAZZMIN_SETTINGS = {
    "site_title": "Restaurant Admin",
    "site_header": "Live Restaurant Panel",
    "site_brand": "FoodOps",
    "welcome_sign": "Welcome to Restaurant Control Center",

    "show_sidebar": True,
    "navigation_expanded": True,

    "icons": {
        "auth.user": "fas fa-user",
        "restaurant.Order": "fas fa-receipt",
        "restaurant.Menu": "fas fa-utensils",
        "restaurant.Table": "fas fa-chair",
    },

    "order_with_respect_to": ["restaurant"],
}

SIMPLE_JWT = {
    # 🔐 Access token (API calls ke liye)
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),   # 🔥 1 hour

    # 🔁 Refresh token (silent re-login)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),   # 🔥 7 days

    # Security best practices
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,

    "AUTH_HEADER_TYPES": ("Bearer",),

    # Optional
    "UPDATE_LAST_LOGIN": True,
}





EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = '9e05d3001@smtp-brevo.com'
EMAIL_HOST_PASSWORD = os.getenv("SMTP_HOST_KEY_BREVO")

DEFAULT_FROM_EMAIL = 'Hungrio <authorit10@gmail.com>'

#  django debugging k liye 

INTERNAL_IPS = [
    "127.0.0.1",
]

# if DEBUG:
#     INSTALLED_APPS += ["debug_toolbar"]
#     MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")




# CELERY
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kolkata"



