from rest_framework import serializers
from accounts.models import CustomUser

from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username','password','password2']

        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = User.objects.create(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'password must match'})
        user.set_password(password)
        user.save()
        return user