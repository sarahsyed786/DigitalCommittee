# enrollment/models.py
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


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

class ResultHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.CharField(max_length=255)  # No null allowed now
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.result} - {self.created_at}"
# class UserPayment(models.Model):
#     app_user =models.ForeignKey(User, on_delete=models.CASCADE)
#     payment_bool = models.BooleanField(default=False)
#     strip_check_out_id = models.CharField(max_length=500)

# @receiver(post_save, sender=User)
# def create_use_payment(sender, instance, created, **kwargs):
#      if created:
#          UserPayment.objects.create(app_user=instance)
