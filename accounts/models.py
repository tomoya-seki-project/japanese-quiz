from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='profile'
    )

    class Meta:
        db_table = 'user_profile'