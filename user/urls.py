from django.urls import path
from user.views  import (
    DuplicatecheckView,
    SignupView,
    SocialSignupView,
    LoginView,
    SocialLoginView,
    MessageSendView,
    MessageCheckView,
)

urlpatterns = [
    path('/check', DuplicatecheckView.as_view()),
    path('/signup', SignupView.as_view()),
    path('/signup/social', SocialSignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/login/social', SocialLoginView.as_view()),
    path('/message', MessageSendView.as_view()),
    path('/messagecheck', MessageCheckView.as_view()),
]
