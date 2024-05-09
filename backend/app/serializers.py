# file serializers.py
from rest_framework import serializers
from .models import *

class FridgeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Fridge
    fields = ('id', 'storedItems')