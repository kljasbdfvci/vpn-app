from django.db import models

# Create your models here.
class Update(models.Model):
    name = models.CharField(max_length=256)  