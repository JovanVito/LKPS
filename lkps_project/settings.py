import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-s#=nq%-*uzhpc+ew7ihhf_uhzlnm-disf6d*ea&=&++48va2=g'
DEBUG = True
ALLOWED_HOSTS = ['*']

# --- APLIKASI ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', # Cukup tulis satu kali saja di sini
]

# --- MIDDLEWARE (Urutan Sangat Penting!) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Harus sebelum Auth & Messages
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lkps_project.urls'

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')], 
        'APP_DIRS': True, 
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lkps_project.wsgi.application'

# --- DATABASE (PostgreSQL) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_lkps',        
        'USER': 'postgres',      
        'PASSWORD': 'Jovan123', 
        'HOST': 'localhost',     
        'PORT': '5432',        
    }
}

# --- STATIC FILES ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'static'),
]