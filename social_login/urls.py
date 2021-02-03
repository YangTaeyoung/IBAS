
from django.urls import path, include
from . import views
urlpatterns = [
    path('account/', include('allauth.urls'))
]

