from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    otp=models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True,
        blank=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email


class Product(models.Model):
    mehsul_adi = models.CharField(max_length=100)
    sekil=models.ImageField(upload_to='images/')
    qiymet = models.FloatField()
    istehsalci=models.CharField(max_length=35)
    seriya=models.CharField(max_length=55)
    emeliyyat_sistemi=models.CharField(max_length=35)
    sim_kartlarin_sayi=models.IntegerField()
    operativ_yaddas=models.CharField(max_length=25)
    daxili_yaddas=models.CharField(max_length=25)
    ekran=models.CharField(max_length=25)
    reng=models.CharField(max_length=15)

    def __str__(self):
        return self.mehsul_adi