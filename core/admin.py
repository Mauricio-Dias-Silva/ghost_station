# core/admin.py — Ghost Station Admin

from django.contrib import admin
from .models import Evidencia, SessaoInvestigacao


@admin.register(SessaoInvestigacao)
class SessaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'local', 'status', 'total_anomalias', 'score_maximo', 'data_inicio', 'data_fim']
    list_filter = ['status', 'data_inicio']
    search_fields = ['titulo', 'local', 'notas']
    readonly_fields = ['total_anomalias', 'score_maximo', 'energia_media']
    actions = ['encerrar_sessoes']

    @admin.action(description="Encerrar sessões selecionadas")
    def encerrar_sessoes(self, request, queryset):
        for sessao in queryset.filter(status='ativa'):
            sessao.encerrar()


@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'score_coincidencia', 'nivel_audio_db', 'variacao_magnetica',
                    'origem_disparo', 'ia_classificacao', 'ia_confianca', 'data_captura']
    list_filter = ['tipo', 'score_coincidencia', 'origem_disparo', 'data_captura']
    search_fields = ['analise_ia', 'ia_classificacao']
    readonly_fields = ['data_captura', 'analise_ia', 'ia_classificacao', 'ia_confianca']
