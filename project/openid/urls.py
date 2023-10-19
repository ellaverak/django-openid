from django.urls import path

from . import views

urlpatterns = [
    path('', views.login),
    path('auth/', views.auth, name='auth'),
    path('home/', views.home, name='home')
]
