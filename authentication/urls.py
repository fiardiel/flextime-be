from django.urls import path, re_path
from authentication.views import login, register, logout, test_token

urlpatterns = [
    re_path('login', login),
    re_path('register', register),
    re_path('logout', logout),
    re_path('test_token', test_token),
]