from django.db import models

# Create your models here.
from django.db import models
from user import models as userModels
import uuid

class Conversation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summarized_conv =  models.TextField()
    user = models.ForeignKey(userModels.User, on_delete=models.DO_NOTHING, related_name='conversation_user')

    def __str__(self):
        return f'Conv ({self.uuid}) of {self.user}'

class Message(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    query = models.CharField()
    response = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='message_conversation')

    def __str__(self):
        return f'Message ({self.uuid}) of {self.conversation}'
