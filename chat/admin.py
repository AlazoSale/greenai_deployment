from django.contrib import admin
# Register your models here.
from chat import models as chatModels

admin.site.register(chatModels.Message)
admin.site.register(chatModels.Conversation)