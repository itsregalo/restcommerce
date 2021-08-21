from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

app_name = 'api-accounts'

urlpatterns = [
    path('register/', RegistrationView, name='register')
]
urlpatterns = format_suffix_patterns(urlpatterns)