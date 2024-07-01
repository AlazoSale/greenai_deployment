from django.shortcuts import render
from django.conf import settings

from rest_framework.exceptions import NotFound
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from . import serializers as chatSerializers
from . import rag_actions as ragActions
from . import translate_actions as translateActions
from chat import models as chatModels

class QueryAPIView(generics.GenericAPIView):

    def post(self, request):
        serializer = chatSerializers.QuerySerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            response_data = ragActions.process_query(query)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ConversationListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = chatSerializers.ConversationSerializer

    def get_queryset(self):
        return chatModels.Conversation.objects.filter(user = self.request.user).order_by('-created_at')
    
class ConversationMessagesListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = chatSerializers.ConversationMessagesSerializer
    def get_queryset(self):
        return chatModels.Message.objects.filter(conversation__uuid = self.kwargs.get('uuid')).order_by('created_at')

class T2TTranslationAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        params = self.request.query_params
        required_params = ['text_to_translate', 'target_lang', 'source_lang']

        if not all(param in params for param in required_params):
            raise NotFound(detail=f'Missing parameters: {", ".join(required_params)}')

        translated_text = translateActions.translate_text(*[params.get(param) for param in required_params])
        return Response({'translated_text': translated_text})
    



