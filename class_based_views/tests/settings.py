DATABASE_ENGINE = 'sqlite3'
ROOT_URLCONF = 'class_based_views.tests.urls'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'class_based_views',
    'class_based_views.tests',
]
SITE_ID = 1