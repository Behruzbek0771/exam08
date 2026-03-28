
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        USER = 'USER', 'User'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

    def __str__(self):
        return self.username
    
    @property
    def is_admin(self) -> bool:
        return self.Role == self.Role.ADMIN
