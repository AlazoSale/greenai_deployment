from django.contrib import admin

from . import models as userModels
# Register your models here.
admin.site.register(userModels.User)
admin.site.register(userModels.TempOTP)