from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction

# Package Imports
from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Custom Imports
from user import models as userModels
from . import serializers as userSerializers
from . import actions

class UserRegisterOTPAPIView(generics.GenericAPIView):
    """
    Generate OTP to proceed with account registration process
    """

    serializer_class = userSerializers.UserRegisterOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        temp_otp = actions.generate_otp_email( serializer.validated_data['email'])
        print(temp_otp.otp)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    

class UserRegisterAPIView(generics.GenericAPIView):
    """
    Last View for registering user, verify otp and create the user
    """
    serializer_class = userSerializers.UserRegisterSerializer
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                validated_data = serializer.validated_data
                validated_data.pop('confirm_password', None)
                validated_data.pop('otp', None)

                user_create = userModels.User.objects.create_user(**validated_data)


                refresh = RefreshToken.for_user(user_create)
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(response_data, status=status.HTTP_200_OK)

        except (ObjectDoesNotExist, IntegrityError) as e:
            raise serializers.ValidationError({'error': str(e)})
        

class UserLoginAPIView(generics.GenericAPIView):
    """
    Get the user email and password and then provide tokens if validated
    """

    serializer_class = userSerializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = userModels.User.objects.get(email=serializer.validated_data['email'])
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    
class LogoutAPIView(generics.GenericAPIView):
    """
    Blacklist the tokens when logging out
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            refresh = request.data["refresh"]
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"detail": "Refresh token blacklisted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UserDetailsAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve user details
    """
    serializer_class = userSerializers.UserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user