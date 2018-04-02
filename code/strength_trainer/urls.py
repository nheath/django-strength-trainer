from django.urls import path, include, re_path
from django.contrib.auth import views as authviews
from .forms import LoginForm
from . import views

urlpatterns = [
    path('',views.index),
    path('register/', views.register),
    path('home/', views.home),
    path('login/', authviews.login, {
        'template_name':'registration/login.html',
        'authentication_form':LoginForm
    }, name="login"),
    path('logout/', authviews.logout,{
        'next_page':'/login/'
}),
]