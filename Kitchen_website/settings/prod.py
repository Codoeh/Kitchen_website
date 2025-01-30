from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

DATABASES = {
 'default': {
   'ENGINE': 'django.db.backends.postgresql',
   'NAME': os.getenv('POSTGRES_DB'),
   'USER': os.getenv('POSTGRES_USER'),
   'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
   'HOST': os.getenv('POSTGRES_HOST'),
   'PORT': os.getenv('POSTGRES_DB_PORT', 5432),
   'OPTIONS': {
     'sslmode': 'require',
   },
 }
}

print("Loaded settings from prod.py")

DEBUG = False
