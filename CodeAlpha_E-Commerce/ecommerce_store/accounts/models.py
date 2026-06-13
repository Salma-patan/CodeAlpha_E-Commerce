from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('owner', 'Product Owner'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def is_owner(self):
        return self.user_type == 'owner'

    def is_customer(self):
        return self.user_type == 'customer'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
