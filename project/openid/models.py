from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
        Model for user-data

    """
    student_id = models.IntegerField(default=000000000)
    password = models.TextField(default=0000)
    is_staff = models.BooleanField(default=0)

