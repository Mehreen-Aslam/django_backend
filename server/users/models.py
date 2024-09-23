# from django.db import models

# Create your models here.
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, country=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not username:
#             raise ValueError('Users must have a username')

#         user = self.model(
#             username=username,
#             email=self.normalize_email(email),
#             country=country,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, country=None):
#         user = self.create_user(
#             username=username,
#             email=email,
#             password=password,
#             country=country
#         )
#         user.is_admin = True
#         user.is_superuser = True
#         user.is_staff = True
#         user.save(using=self._db)
#         return user

# class User(AbstractBaseUser):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=100, unique=True)
#     email = models.EmailField(max_length=255, unique=True)
#     country = models.CharField(max_length=100, blank=True, null=True)
#     is_verified = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True

#     @property
#     def is_staff(self):
#         return self.is_admin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, country=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            country=country,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, country=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            username=username,
            email=email,
            password=password,
            country=country,
            **extra_fields
        )

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    # email = models.EmailField(max_length=255, unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    # is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = UserManager()

    # objects = UserManager()
     

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Username is required for creating superuser

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

#slider
class Slider(models.Model):
    image = models.URLField(max_length=500, blank=False, null=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image

        from django.db import models
        # ContactUs

class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    email = models.EmailField()
    phoneno = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# models.py

from django.db import models

class Blog(models.Model):
    image = models.URLField(max_length=255, blank=True, null=True)
    heading = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    writtenby = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading

from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    status = models.CharField(max_length=50, blank=True, null=True)  # Status is optional
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Team(models.Model):
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)  # ImageField for uploading images
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

# models.py
from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question


