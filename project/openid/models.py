from django.db import models
from django.contrib.auth.models import AbstractUser
from django_cryptography.fields import encrypt

class User(AbstractUser):
    """
        Model for user-data

    """
    student_id = encrypt((models.CharField(default="000000000")))
    first_name = encrypt((models.CharField(max_length = 100)))
    last_name = encrypt((models.CharField(max_length = 100)))
    email = (models.CharField(max_length = 100))
    username = encrypt((models.CharField(unique=True, max_length = 100)))
