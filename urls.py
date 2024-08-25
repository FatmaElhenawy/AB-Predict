from turtle import home
from django.urls import path, include
from django.conf import settings
from myApp import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin

app_name = 'myApp'

urlpatterns = [
        path('', views.home, name='home'),
        path('sign/', views.sign, name='sign'),
        path('login/', views.Login, name='Login'),
        path('home_log', views.home_log, name='home_log'),
        path('history/', views.history, name='history'),
        path('prediction/', views.mainPrediction, name='prediction'),
        path('logout/', views.logoutUser, name='logoutUser'),
        path('predictionM/', views.predictBigData, name='predictBigData'),
        path('prediction/model_one.html', views.predict,name='model1'),
        path('prediction/model_two.html', views.predictBigData,name='model2'),
]
