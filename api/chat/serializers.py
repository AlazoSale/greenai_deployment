from rest_framework import serializers

# Custom Imports
from chat import models as chatModels


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=1000)

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = chatModels.Conversation  
        fields = ['uuid', 'summarized_conv']

class ConversationMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = chatModels.Message  
        fields = ['query', 'response']