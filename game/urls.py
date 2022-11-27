from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.handleRegister, name="handleRegister"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('move', views.getmove, name="getmove"),
    path('linker', views.linker, name="linker"),
    path('state', views.boardstate, name="boardstate"),
]
