from django.db import models


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
