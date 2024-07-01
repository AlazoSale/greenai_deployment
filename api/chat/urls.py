from django.urls import path 
from . import views 
urlpatterns = [
    path('query/', views.QueryAPIView.as_view(), name='query'),
    path('conversations/', views.ConversationListAPIView.as_view(), name='query'),
    path('conversations/<uuid:uuid>/', views.ConversationMessagesListAPIView.as_view(), name='query'),
    path('translate/', views.T2TTranslationAPIView.as_view(), name='translate'),

]


