from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserListAPIView, UserDetailAPIView, UserRegistrationAPIView, LoginAPIView, LogoutAPIView, PasswordResetView, PasswordResetConfirmView


app_name = 'api_user'


urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user_list'),
    path('users/<uuid:id>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('register/', UserRegistrationAPIView.as_view(), name='user_register'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
