from django.urls import path 
from . import views 
urlpatterns = [
    path('query/', views.QueryAPIView.as_view(), name='query'),
    path('ping/', views.PingApiView.as_view(), name='query'),

]


