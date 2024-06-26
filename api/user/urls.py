from rest_framework_simplejwt.views import TokenRefreshView,TokenBlacklistView
from django.urls import path 
from . import views 
urlpatterns = [
    path('register/request-otp/', views.UserRegisterOTPAPIView.as_view(), name='register'),
    path('register/', views.UserRegisterAPIView.as_view(), name='register'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),

    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('details/', views.UserDetailsAPIView.as_view(), name='logout'),

    
    path('forgot-password/request-otp/', views.ForgotPasswordOTPAPIView.as_view(), name='forgot-pw'),
    path('forgot-password/verify-otp/', views.VerifyOTPAPIView.as_view(), name='forgot-otp'),
    path('forgot-password/reset/', views.ResetPasswordAPIView.as_view(), name='forgot-reset'),

]


