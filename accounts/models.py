from django.db import models

from django.db.models.functions import Lower
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from core.models import TimeStampedModel


class UserManager(DjangoUserManager):
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        return super().normalize_email(email).strip().lower()

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Please enter email')
        if not username:
            raise ValueError('Please enter username')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="user_email_ci_unique",
            ),
        ]

class UserProfile(TimeStampedModel):
    last_vocab_sync_at = models.DateTimeField(blank=True, null=True)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='profile'
    )

    def __str__(self):
        return ''

    class Meta:
        db_table = 'user_profile'
