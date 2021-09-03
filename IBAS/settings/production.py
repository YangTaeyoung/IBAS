from IBAS.settings.base import *
from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk

sentry_sdk.init(
    dsn="https://e0b7f7f1f8f04b39a633a223a86a8dca@o977207.ingest.sentry.io/5933669",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    #traces_sampler=traces_sampler,
    send_default_pii=True,
    environment= "production",
)    


ADMINS = [
    ('Dong Hyeon Yu', 'ydh9516.dev@gmail.com'),
]

WSGI_APPLICATION = 'IBAS.wsgi.production.application'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_vthq1y2s@$+o&+759)d)0r59e&%!gdcp7(^tsu1=+b-cog_@1'
# send email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ibasmail20@gmail.com'
EMAIL_HOST_PASSWORD = 'ibasforever'
