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
    

class ForgotPasswordOTPAPIView(generics.GenericAPIView):
    """
    Generate the OTP with email to reset password
    """
    serializer_class = userSerializers.EmailSerializer

    def post(self,request,*args,**kwargs):

        if 'email' in request.data:
            generate_otp_function = actions.generate_otp_email
        else:
            return Response({'error':'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        temp_otp = generate_otp_function(serializer.validated_data['email'])
        print(temp_otp.otp)
        return Response(status=status.HTTP_200_OK)
    
class VerifyOTPAPIView(generics.GenericAPIView):
    """
    Verify the OTP, email to proceed to next screen
    """
    serializer_class = userSerializers.OTPSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)
        

class ResetPasswordAPIView(generics.UpdateAPIView):
    """
    Verify OTP and reset the password
    """

    serializer_class = userSerializers.ResetPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data.get('otp')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        userSerializers.ForgotPasswordValidators.validate_otp(otp, email)

        user = self.get_user_by_credentials(email)
        if user:
            user.set_password(password)
            user.save()
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def get_user_by_credentials(self, email):
        if email:
            try:
                return userModels.User.objects.get(email=email)
            except userModels.User.DoesNotExist:
                pass
        return None

