from pymongo import MongoClient
from django.db import models

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)


    def save(self, *args, **kwargs):#method yo save user data into the database
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id