from django.contrib import admin
from accounts.models import (CustomUser, PhoneNumber, Profile
                         )
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'is_superuser',
                'is_staff',
                'is_merchant',
                'is_customer',
            ),
        }),
    )
    
    
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(PhoneNumber)
admin.site.register(Profile)