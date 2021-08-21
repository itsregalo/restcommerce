from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import RegistrationSerializer

@api_view(['POST'])