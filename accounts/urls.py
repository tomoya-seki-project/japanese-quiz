from django.urls import path
from django.views.generic.base import TemplateView

from . import views
from .views import (
    RegistUserView, UserLoginView, UserLogoutView, HomeView, UserView
)

app_name = 'accounts'

urlpatterns = [
    path('home/', HomeView.as_view(), name='user_home'),
    path('user_regist/', RegistUserView.as_view(), name='user_regist'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user_detail/', UserView.as_view(), name='user_detail'),
]
