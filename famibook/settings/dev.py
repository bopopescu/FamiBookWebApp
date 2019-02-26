from .common import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qpf6&77oy#48$y$-ko+v_6-!&ip&#a-k+1a@g9wejq0u72l!ct'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

print('you are in dev mode!!!!!!!!')
print(os.path.join(BASE_DIR, 'db.sqlite3'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
