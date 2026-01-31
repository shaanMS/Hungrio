from pathlib import Path
import os
from datetime import timedelta

# --------------------------------------------------
# BASE
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# CORE
# --------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise Exception("DJANGO_SECRET_KEY not set")

# DEBUG को Railway variable से पढ़ो, default False (production safe)
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    'hungrio-production.up.railway.app',
    '.up.railway.app',          # wildcard for Railway subdomains
    'localhost',
    '127.0.0.1',
    '*',                        # temporary test के लिए (बाद में हटा दो)
]



CSRF_TRUSTED_ORIGINS = [
    'https://hungrio-production.up.railway.app',
    'https://*.up.railway.app',
]


USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Production में True रखो (Railway HTTPS handle करता है)
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False") == "True"

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    # "jazzmin",  # commented out - remove permanently अगर issue दे रहा है

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",
    "csp",
    "django_filters",
    "channels",
   # "django_ratelimit",
    "django_celery_beat",
    "rest_framework_simplejwt",
     "captcha",
    "restaurant",
    "accounts",
    "customer",
    "category",
    "product",
    "stock_and_capacity",
    "cart",
    "order",
    "order_payment",
    "invoice",
    "receipt",
    "refund",
    "complaint",
    "wishlist",
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

# --------------------------------------------------
# URL / ASGI
# --------------------------------------------------
ROOT_URLCONF = "restaurant.urls"
ASGI_APPLICATION = "restaurant.asgi.application"

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "product" / "restaurant_frontend"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --------------------------------------------------
# DATABASE (Railway PostgreSQL)
# --------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("PGDATABASE"),
        "USER": os.getenv("PGUSER"),
        "PASSWORD": os.getenv("PGPASSWORD"),
        "HOST": os.getenv("PGHOST"),
        "PORT": os.getenv("PGPORT", "5432"),
        "OPTIONS": {"sslmode": "require"},
    }
}

# --------------------------------------------------
# STATIC & MEDIA
# --------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------
# AUTH
# --------------------------------------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# --------------------------------------------------
# REST FRAMEWORK
# --------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "1000/day",
        "user": "100/min",
    },
}

# --------------------------------------------------
# JWT
# --------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --------------------------------------------------
# CORS
# --------------------------------------------------
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://hungrio-production.up.railway.app",
    "http://localhost:3000",  # अगर frontend local में है
    # और भी origins ऐड कर सकते हो
]

# --------------------------------------------------
# EMAIL (Brevo SMTP)
# --------------------------------------------------
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"
)
# EMAIL_HOST = os.getenv("EMAIL_HOST")
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
# EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
# DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

# --------------------------------------------------
# STRIPE
# --------------------------------------------------
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# --------------------------------------------------
# REDIS / CELERY / CHANNELS
# --------------------------------------------------
REDIS_URL = os.getenv("REDIS_URL")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}


BREVO_API_KEY = os.getenv("hungrio_brevo")
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
BREVO_SENDER_NAME = os.getenv("BREVO_SENDER_NAME")



CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kolkata"

# --------------------------------------------------
# CSP (SAFE)
# --------------------------------------------------
# --------------------------------------------------
# CONTENT SECURITY POLICY (FULL – COPY & PASTE)
# --------------------------------------------------

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {

        # Default
        "default-src": [
            "'self'",
        ],

        # JavaScript
        "script-src": [
            "'self'",
            "https://js.stripe.com",
            "'unsafe-inline'",   # HTML onclick / inline scripts (later remove)
        ],

        # CSS
        "style-src": [
            "'self'",
            "'unsafe-inline'",
            "https://fonts.googleapis.com",
            "https://cdnjs.cloudflare.com",
        ],

        # Fonts
        "font-src": [
            "'self'",
            "https://fonts.gstatic.com",
            "https://cdnjs.cloudflare.com",
        ],

        # Images / Icons
        "img-src": [
            "'self'",
            "data:",
            "blob:",
        ],

        # Stripe iframe / checkout
        "frame-src": [
            "https://js.stripe.com",
        ],

        # API / AJAX / Fetch / WebSocket
        "connect-src": [
            "'self'",
            "https://hungrio-production.up.railway.app",
            "https://api.stripe.com",
            "wss://hungrio-production.up.railway.app",
        ],

        # Forms (POST, login, payment)
        "form-action": [
            "'self'",
            "https://api.stripe.com",
        ],

        # Media (future-proof)
        "media-src": [
            "'self'",
        ],

        # Objects (disable Flash etc.)
        "object-src": [
            "'none'",
        ],

        # Base URI
        "base-uri": [
            "'self'",
        ],

        # Clickjacking protection
        "frame-ancestors": [
            "'self'",
        ],
    }
}

# --------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CAPTCHA_IMAGE_SIZE = (100, 40)
CAPTCHA_LENGTH = 4
CAPTCHA_TIMEOUT = 5 * 60