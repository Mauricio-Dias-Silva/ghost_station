from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('api/gatilho_anomalia/', views.gatilho_anomalia, name='gatilho_anomalia'),
]