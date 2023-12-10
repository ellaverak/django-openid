from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", views.login, name="login"),
    path('auth/', views.auth, name='auth'),
    path('home/', views.home, name='home')
]
