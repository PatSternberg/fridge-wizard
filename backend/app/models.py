# file: models.py
from django.db import models
from pymongo import MongoClient #MongoClient class  from pymongo library need it to connect to mongo DB

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)


    def save(self, *args, **kwargs):#method yo save user data into the database
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id

# Create your models here.

# Fridge model handles data structures for fridges, fridge user ownership and stored items with expiry dates
class Fridge(models.Model):

    id = models.CharField(primary_key=True, max_length=100)
    storedItems = models.JSONField()
    user_id = models.CharField(max_length=100)

    def save(self, *args, **kwargs): #method to save fridge data into the database
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id

