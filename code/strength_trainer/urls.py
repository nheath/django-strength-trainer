from django.urls import path, include, re_path
from django.contrib.auth import views as authviews
from .forms import LoginForm
from . import views

urlpatterns = [
    path('',views.index),
    # re_path(r'^long_cat/(?P<username>.+)/$', views.long_cat),
    re_path(r'^update/(?P<week>week_[1,2,3,4])/(?P<workout>bench|squat|overhead|deadlift)/$', views.update),
    path('register/', views.register),
    path('workout_week_api/', views.workout_week_api),
    path('home/', views.home),
    path('new_workout/', views.new_workout),
    path('login/', authviews.login, {
        'template_name':'registration/login.html',
        'authentication_form':LoginForm
    }, name="login"),
    path('logout/', authviews.logout,{
        'next_page':'/login/'
}),
]