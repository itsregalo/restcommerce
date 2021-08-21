from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api-accounts'

urlpatterns = [
    path('register/', RegistrationView, name='register'),
    path('login/', obtain_auth_token, name='login'),
]
urlpatterns = format_suffix_patterns(urlpatterns)