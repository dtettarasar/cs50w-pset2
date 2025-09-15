from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    
    cat_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}: {self.cat_name}"