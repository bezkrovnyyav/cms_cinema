from django.urls import path
from .views import *

urlpatterns = [
    path('', UserUpdateView.as_view(), name='user'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),
]
