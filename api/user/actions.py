from datetime import datetime, timedelta
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.utils.crypto import get_random_string
import re
from django.core.mail import send_mail
from django.conf import settings

from user import models as userModels
from misc import models as miscModels


def validate_user_name_format(value):
    return value


def validate_email_input( value):
    is_email_format = re.match(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', value)
    if not is_email_format :
        raise serializers.ValidationError('invalid email.')
    return value


def validate_email_input_exists( value):
        value = validate_email_input(value)
        if not userModels.User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist.')
        return value


def validate_password_match(password, confirm_password):
        if password != confirm_password:
            raise serializers.ValidationError('The passwords do not match.')
        return password


def generate_otp_email(email):

    otp_code = get_random_string(length=4, allowed_chars='0123456789')
    try:
        temp_otp = userModels.TempOTP.objects.get(email=email)
        temp_otp.otp = otp_code
        temp_otp.validated = False
        temp_otp.save()
    except:
        temp_otp = userModels.TempOTP.objects.create(email=email, otp=otp_code)
    return temp_otp


def validate_otp(otp, value):
    try:
        temp_otp = userModels.TempOTP.objects.get(otp=otp, email=value, validated=False)
        temp_otp.validated = True
        temp_otp.save()
    except:
        raise serializers.ValidationError('Invalid OTP or OTP Expired.')
    return otp


def verify_otp(otp, value):
    if not userModels.User.objects.filter(email= value).first():
        raise serializers.ValidationError('Invalid email')
    else: 
        try:    
            userModels.TempOTP.objects.get(otp=otp, email=value, validated=False)
        except:
            raise serializers.ValidationError('Invalid OTP or OTP Expired.')
        return otp

