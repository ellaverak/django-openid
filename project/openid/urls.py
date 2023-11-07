from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_id, name='login_id'),
    path('auth/', views.auth, name='auth'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout_id')
]
