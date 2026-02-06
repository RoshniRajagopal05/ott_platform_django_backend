

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length =255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_password_change = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'




class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='images/')
    
    trailer = models.FileField(
        upload_to='trailers/',
        null=True,
        blank=True
    )

    video = models.FileField(upload_to='videos/')
    
    # New fields for enhanced details
    genre = models.CharField(max_length=100, default='Unknown', blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, blank=True)
    duration = models.IntegerField(default=0, blank=True)  # Duration in minutes
    release_year = models.IntegerField(default=2024, blank=True)
    director = models.CharField(max_length=100, default='Unknown', blank=True)
    cast = models.TextField(default='', blank=True)  # Comma-separated cast names


    
class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
