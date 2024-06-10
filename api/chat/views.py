from django.shortcuts import render
from django.conf import settings


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from . import serializers as chatSerializers
from . import actions as chatActions


class QueryAPIView(generics.GenericAPIView):

    def post(self, request):
        serializer = chatSerializers.QuerySerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            response_data = chatActions.process_query(query)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class PingApiView(generics.GenericAPIView):

    def get(self, request):
        return Response({"response": "Ok"}, status=status.HTTP_200_Ok)  