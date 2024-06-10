from rest_framework import serializers

# Package Imports
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Custom Imports

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=1000)