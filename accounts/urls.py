from django.urls import path
from django.views.generic.base import TemplateView

from . import views
from .views import (
    RegistUserView,
    UserLoginView,
    UserLogoutView,
    HomeView,
    UserView,
    ActivateUserView,
    ActivationEmailSentView,
    ResendActivationEmailView,
)

app_name = 'accounts'

urlpatterns = [
    path('', HomeView.as_view(), name='user_home'),
    path('user_regist/', RegistUserView.as_view(), name='user_regist'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user_detail/', UserView.as_view(), name='user_detail'),
    path("activate/<uidb64>/<token>/", ActivateUserView.as_view(), name="user_activate"),
    path("activation-email-sent/", ActivationEmailSentView.as_view(), name="activation_email_sent"),
    path("resend-activation-email/", ResendActivationEmailView.as_view(), name="resend_activation_email"),
]
