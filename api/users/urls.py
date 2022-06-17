from django.urls import path
from users.views import UserSignupView, ResourceView, VerifyEmail, UserLoginView

urlpatterns = [
    path('auth/signup/', UserSignupView.as_view()),
    path('auth/registers/', ResourceView.as_view()),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('auth/login/', UserLoginView.as_view(), name="login"), 
]
