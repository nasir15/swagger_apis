from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.utils.timezone import now
import os

# Create your models here.

class User(AbstractUser):
    father_name = models.CharField(max_length=250, blank=True, null=True)
    company_name = models.CharField(max_length=512, blank=True, null=True)
    unit = models.CharField(max_length=250)
    brigade = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length = 254, blank=True , null=True)
    gender = models.CharField(max_length=1, default="N")
    user_type = models.CharField(max_length=3, default="RGU")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='user_created_by', null = True, blank = True)

    class Meta:
        managed = True
        db_table = 'users'

