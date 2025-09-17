from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, matric_number=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        # Enforce these fields only for regular users (no is_superuser flag here)
        if not first_name or not last_name or not matric_number:
            raise ValueError("First name, last name, and matric number are required")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            matric_number=matric_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Defaults for fields not required for superuser
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')
        extra_fields.setdefault('matric_number', '0000000')

        user = self.create_user(
            email=email,
            first_name=extra_fields['first_name'],
            last_name=extra_fields['last_name'],
            matric_number=extra_fields['matric_number'],
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    matric_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'matric_number']

    objects = UserManager()

    def __str__(self):
        return self.email
