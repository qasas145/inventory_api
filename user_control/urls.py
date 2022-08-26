from django.contrib import admin
from django.urls import path, include
from .views import LoginView, RegisterView, UserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserView)
urlpatterns = [
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("", include(router.urls))
]
