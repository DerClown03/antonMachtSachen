from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("registration", views.SignupView.as_view(), name="signup"),
]