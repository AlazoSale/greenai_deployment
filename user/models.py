
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
        Overriding the default user manager used in terminal to create user
    """

    def create_user(self, email, password , user_name=None):
        user = self.model(
            user_name=user_name,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, user_name=None ):
        user = self.create_user(
            user_name=user_name,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    """
        Custom user model
    """
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            primary_key=True)
    user_name = models.CharField(verbose_name='user name',
                                 max_length=50,
                                 blank=True,
                              null=True,)
    email = models.EmailField(blank=True,
                              null=True,
                              max_length=254,
                              unique=True,
                              verbose_name='email address')
    is_superuser = models.BooleanField(default=False,
                                       verbose_name='is superuser')        
    is_active = models.BooleanField(default=True)

    last_login = models.DateTimeField(blank=True,
                                      null=True,
                                      verbose_name='last login')
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')
    objects = UserManager()
    USERNAME_FIELD = 'email'


    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        user_name = self.user_name if self.user_name else ""
        email = self.email if self.email else ""
        return f"{user_name} ({email})"

    class Meta:
        ordering = ['user_name']



class TempOTP(models.Model):
    email = models.EmailField(max_length=254, blank=True, null=True)
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False)
    
    def __str__(self):
        email = self.email if self.email else ''
        return f' ({email})'

