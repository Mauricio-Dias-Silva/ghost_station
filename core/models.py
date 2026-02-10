# core/models.py — Ghost Station Data Layer

from django.db import models
from django.utils import timezone


class SessaoInvestigacao(models.Model):
    """Uma sessão de investigação paranormal (agrupa evidências)."""
    STATUS_CHOICES = [
        ('ativa', 'Em Andamento'),
        ('encerrada', 'Encerrada'),
        ('analisando', 'Em Análise IA'),
    ]

    titulo = models.CharField(max_length=200, default="Investigação sem título")
    local = models.CharField(max_length=300, blank=True, verbose_name="Local da Investigação")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ativa')
    notas = models.TextField(blank=True, verbose_name="Notas do Investigador")

    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(null=True, blank=True)

    # Estatísticas calculadas
    total_anomalias = models.IntegerField(default=0)
    score_maximo = models.IntegerField(default=0)
    energia_media = models.FloatField(default=0)

    class Meta:
        verbose_name = "Sessão de Investigação"
        verbose_name_plural = "Sessões de Investigação"
        ordering = ['-data_inicio']

    def __str__(self):
        return f"#{self.id} — {self.titulo} ({self.get_status_display()})"

    @property
    def duracao(self):
        fim = self.data_fim or timezone.now()
        return fim - self.data_inicio

    def encerrar(self):
        self.status = 'encerrada'
        self.data_fim = timezone.now()
        # Recalcular stats
        evidencias = self.evidencias.all()
        self.total_anomalias = evidencias.count()
        if evidencias.exists():
            self.score_maximo = evidencias.order_by('-score_coincidencia').first().score_coincidencia
            self.energia_media = evidencias.aggregate(
                avg=models.Avg('nivel_audio_db')
            )['avg'] or 0
        self.save()


class Evidencia(models.Model):
    """Uma anomalia detectada e capturada durante investigação."""
    TIPO_CHOICES = [
        ('visual', 'Anomalia Visual (Face/Forma)'),
        ('sonora', 'Anomalia Sonora (Audio Spike)'),
        ('magnetica', 'Anomalia Magnética (Bússola)'),
        ('multipla', 'Anomalia Múltipla (Multi-Sensor)'),
        ('manual', 'Captura Manual'),
    ]

    sessao = models.ForeignKey(
        SessaoInvestigacao, on_delete=models.CASCADE,
        related_name='evidencias', null=True, blank=True,
        verbose_name="Sessão"
    )

    imagem_url = models.CharField(max_length=500)
    data_captura = models.DateTimeField(auto_now_add=True)

    # Tipo de anomalia
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='visual')

    # Dados Científicos (Vindos do Celular/Navegador)
    nivel_audio_db = models.FloatField(default=0, help_text="Volume do som no momento")
    variacao_magnetica = models.FloatField(default=0, help_text="Variação da Bússola")
    temperatura = models.FloatField(null=True, blank=True, help_text="Temperatura ambiente (°C)")

    # Localização
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Score: Quanto maior, mais sensores dispararam juntos
    score_coincidencia = models.IntegerField(default=1)

    # IA Analysis
    analise_ia = models.TextField(blank=True, verbose_name="Análise da IA")
    ia_classificacao = models.CharField(
        max_length=30, blank=True,
        verbose_name="Classificação IA",
        help_text="O que a IA acha que é"
    )
    ia_confianca = models.FloatField(
        null=True, blank=True,
        verbose_name="Confiança IA (%)"
    )

    # Origem do disparo
    origem_disparo = models.CharField(max_length=50, default='desconhecido')

    class Meta:
        verbose_name = "Evidência"
        verbose_name_plural = "Evidências"
        ordering = ['-data_captura']

    def __str__(self):
        return f"EVD-{self.id} | {self.get_tipo_display()} | Score: {self.score_coincidencia}"

    @property
    def nivel_perigo(self):
        """Classificação de perigo baseada no score."""
        if self.score_coincidencia >= 4:
            return 'CRÍTICO'
        elif self.score_coincidencia >= 3:
            return 'ALTO'
        elif self.score_coincidencia >= 2:
            return 'MÉDIO'
        return 'BAIXO'