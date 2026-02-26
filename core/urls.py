# core/urls.py — Ghost Station Routes

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('scanner/', views.mobile_scanner, name='mobile_scanner'),

    # EVP Console
    path('evp/', views.evp_console, name='evp_console'),

    # APIs — Investigação
    path('api/gatilho_anomalia/', views.gatilho_anomalia, name='gatilho_anomalia'),
    path('api/iniciar_sessao/', views.iniciar_sessao, name='iniciar_sessao'),
    path('api/encerrar_sessao/', views.encerrar_sessao, name='encerrar_sessao'),
    path('api/evidencias/', views.api_evidencias, name='api_evidencias'),
    path('api/status/', views.api_status, name='api_status'),

    # APIs — EVP
    path('api/evp/analisar/', views.api_evp_analisar, name='api_evp_analisar'),
    path('api/evp/registros/', views.api_evp_registros, name='api_evp_registros'),
    path('api/evp/status/', views.api_evp_status, name='api_evp_status'),
    path('api/evp/iniciar/', views.api_iniciar_sessao_evp, name='api_iniciar_sessao_evp'),
    path('api/evp/encerrar/', views.api_encerrar_sessao_evp, name='api_encerrar_sessao_evp'),

    # ITC Visual Console (Fase 3)
    path('itc/', views.itc_console, name='itc_console'),
    path('itc_video_feed/', views.itc_video_feed, name='itc_video_feed'),
    path('api/itc/analisar/', views.api_itc_analisar, name='api_itc_analisar'),
    
    # Aura Synthesis (Fase 5)
    path('video_call/', views.video_call, name='video_call'),
    path('aura_video_feed/', views.aura_video_feed, name='aura_video_feed'),
    path('api/aura/send_seed/', views.api_aura_send_seed, name='api_aura_send_seed'),
    path('api/aura/status/', views.api_aura_status, name='api_aura_status'),
    path('api/aura/toggle/', views.api_aura_toggle, name='api_aura_toggle'),
    path('api/aura/ping/', views.api_quantum_ping, name='api_aura_ping'),
    path('api/bio/update/', views.api_bio_update, name='api_bio_update'),
    path('blueprints/', views.blueprint_view, name='blueprints'),
]