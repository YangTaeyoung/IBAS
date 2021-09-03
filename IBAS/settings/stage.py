from IBAS.settings.base import *
from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk

sentry_sdk.init(
    dsn="https://e0b7f7f1f8f04b39a633a223a86a8dca@o977207.ingest.sentry.io/5933669",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    #traces_sampler=traces_sampler,
    send_default_pii=True,
    environment="stage",
)


ADMINS = [
    ('Dong Hyeon Yu', 'ydh9516.dev@gmail.com'),
]

WSGI_APPLICATION = 'IBAS.wsgi.stage.application'
