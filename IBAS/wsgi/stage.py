import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IBAS.settings.stage')

#from whitenoise import WhiteNoise


application = get_wsgi_application()
#application = WhiteNoise(application)