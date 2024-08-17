from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.CharField()

    first_name = models.CharField()
    last_name = models.CharField()
    patronymic = models.CharField()

    phone_number = models.CharField()
    email = models.CharField()

    super_lessor = models.BooleanField(default=False)
    perfect_cleanliness = models.BooleanField(default=False)
    traveler = models.BooleanField(default=False)
    inspector = models.BooleanField(default=False)