from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page_view, name="home"),
    path("login/", views.login),
    path("auth/", views.auth, name="auth"),
]