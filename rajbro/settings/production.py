import os
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'da172truikfs15',
        'USER': 'pecwehrdoxtoko',
        'PASSWORD': 'kKAYhtHmvPFbcz8MP6-S6jjRai',
        'HOST': 'ec2-54-243-52-209.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)