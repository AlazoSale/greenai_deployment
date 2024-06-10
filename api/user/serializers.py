from rest_framework import serializers

# Package Imports
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Custom Imports
from user import models as userModels
from . import actions as userActions


class BaseUserSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_user_name(self, value):
        if not value:
            raise serializers.ValidationError("User name cannot be empty.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email cannot be empty.")
        value = userActions.validate_email_input(value)
        if userModels.User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password cannot be empty.")
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        return userActions.validate_password_match(value, self.initial_data.get('confirm_password'))
    

class UserRegisterOtpSerializer(BaseUserSerializer):
    pass


class UserRegisterSerializer(BaseUserSerializer):
    otp = serializers.CharField(required=True)

    def validate_otp(self, value):
        email = self.initial_data.get('email')
        if email:
            userActions.validate_otp(value, email)
        return value


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

        
    def validate_password(self, value):
        email = self.initial_data.get('email')
        user = userModels.User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError('Account with this email does not exist.')

        if not user.check_password(value):
            raise serializers.ValidationError('Invalid password.')

        return value


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = userModels.User
        fields = ['user_name','email']



