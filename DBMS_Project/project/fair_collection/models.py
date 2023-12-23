# enrollment/models.py
from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Enrollment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    package = models.ForeignKey('Package', on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=255)
    message = models.TextField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    package = models.CharField(max_length=20)