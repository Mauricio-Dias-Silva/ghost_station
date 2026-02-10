# core/urls.py — Ghost Station Routes

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('scanner/', views.mobile_scanner, name='mobile_scanner'),

    # APIs
    path('api/gatilho_anomalia/', views.gatilho_anomalia, name='gatilho_anomalia'),
    path('api/iniciar_sessao/', views.iniciar_sessao, name='iniciar_sessao'),
    path('api/encerrar_sessao/', views.encerrar_sessao, name='encerrar_sessao'),
    path('api/evidencias/', views.api_evidencias, name='api_evidencias'),
    path('api/status/', views.api_status, name='api_status'),
]