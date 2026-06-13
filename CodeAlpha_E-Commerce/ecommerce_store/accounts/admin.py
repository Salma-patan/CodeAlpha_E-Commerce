from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'first_name', 'last_name', 'is_active']
    list_filter = ['user_type', 'is_active', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('User Type & Contact', {'fields': ('user_type', 'phone', 'address')}),
    )
