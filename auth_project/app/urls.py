from django.urls import path
from .views import UserRegistrationView,get,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordRestEmailView,UserPasswordResetView
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view()),
    path('change_password/',UserChangePasswordView.as_view()),
    path('send-rest-password-email/',SendPasswordRestEmailView.as_view()),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view()),
    path('get_all/',get)
]
