from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random


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
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100, blank=True, null=True, default='Unknown')  # Default value for country
    otp = models.CharField(max_length=4, blank=True, null=True, default='0000')  # Default value for OTP
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Slider(models.Model):
    image = models.URLField(max_length=500, blank=False, null=False, default='https://example.com/default-image.jpg')  # Default image URL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image


class ContactUs(models.Model):
    name = models.CharField(max_length=255, default='Anonymous')  # Default value for name
    country = models.CharField(max_length=255, default='Unknown')  # Default value for country
    email = models.EmailField(default='no-reply@example.com')  # Default value for email
    phoneno = models.CharField(max_length=20, default='0000000000')  # Default value for phone number
    message = models.TextField(default='No message provided')  # Default message value
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    image = models.URLField(max_length=255, blank=True, null=True, default='https://example.com/default-blog-image.jpg')  # Default image URL
    heading = models.CharField(max_length=255, default='Default Heading')  # Default heading
    category = models.CharField(max_length=100, default='General')  # Default category
    written_by = models.CharField(max_length=100, default='Admin')  # Default value for written_by
    content = models.TextField(default='No content provided')  # Default content
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading


class Job(models.Model):
    title = models.CharField(max_length=255, default='Job Title')  # Default title
    location = models.CharField(max_length=255, default='Location')  # Default location
    category = models.CharField(max_length=255, default='General')  # Default category
    status = models.CharField(max_length=50, blank=True, null=True, default='Open')  # Default status
    description = models.TextField(default='Job description')  # Default description
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Team(models.Model):
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)  # ImageField for uploading images
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class FAQ(models.Model):
    question = models.CharField(max_length=255, default='Default question')  # Default question
    answer = models.TextField(default='Default answer')  # Default answer
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question



class ForgetPassword(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=4)  # Set max_length to 4
    created_at = models.DateTimeField(auto_now_add=True)
    
    def generate_otp(self):
        return str(random.randint(1000, 9999))  # Generates a 4-digit OTP

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_otp()  # Assigns the generated OTP if it's not already set
        super().save(*args, **kwargs)

