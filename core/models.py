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
        max_length=100, blank=True,
        verbose_name="Classificação IA",
        help_text="O que a IA acha que é"
    )
    ia_confianca = models.FloatField(
        null=True, blank=True,
        verbose_name="Confiança IA (%)"
    )

    # NOVO: Campos Forenses Fase 7
    amplitude_db = models.FloatField(default=0, verbose_name="Amplitude (dB)")
    frequencia_hz = models.FloatField(default=0, verbose_name="Frequência (Hz)")
    luminosidade_lux = models.FloatField(null=True, blank=True, verbose_name="Luz (Lux)")
    kp_index_captura = models.FloatField(default=0, verbose_name="Índice Kp (NOAA)")
    snr_ratio = models.FloatField(default=0, verbose_name="SNR (Signal-to-Noise)")

    # NOVO: Bio-Sincronia Fase 8
    obs_bpm = models.FloatField(default=0, verbose_name="BPM do Observador")
    obs_stress = models.FloatField(default=0, verbose_name="Estresse (%)")

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


class RegistroSintese(models.Model):
    """
    Arquivo das Sombras: Armazena o log completo de uma sessão de síntese 5D.
    """
    sessao_investigacao = models.ForeignKey(
        SessaoInvestigacao, on_delete=models.CASCADE,
        related_name='sinteses', null=True, blank=True
    )
    data_sessao = models.DateTimeField(default=timezone.now)
    entidade_nome = models.CharField(max_length=200, default="Desconhecida")
    classe_espirito = models.CharField(max_length=50, default="N/A", verbose_name="Classe (Kardec)")
    afinidade_fluidica = models.FloatField(default=0, verbose_name="Afinidade (%)")
    densidade_final = models.CharField(max_length=50, default="3D")
    coerencia_maxima = models.FloatField(default=0)
    
    # Dados Técnicos Fase 7
    kp_index_medio = models.FloatField(default=0)
    snr_medio = models.FloatField(default=0)
    frequencia_base_hz = models.FloatField(default=0)

    # Bio-Sincronia Fase 8
    obs_bpm_medio = models.FloatField(default=0)
    obs_stress_medio = models.FloatField(default=0)
    coerencia_cardiaca_media = models.FloatField(default=0)
    metabolic_drain = models.FloatField(default=0)
    
    # Armazena o diálogo completo em JSON: [{autor: str, mensagem: str, timestamp: str}]
    log_dialogo = models.JSONField(default=list)
    
    # Seed semântica que iniciou ou foi mais relevante
    semente_principal = models.TextField(blank=True)
    
    # URL de uma imagem capturada durante o pico de coerência
    snapshot_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Registro de Síntese"
        verbose_name_plural = "Registros de Síntese"
        ordering = ['-data_sessao']

    def __str__(self):
        return f"Sintese-{self.id} | {self.entidade_nome} | {self.data_sessao.strftime('%d/%m %H:%M')}"


class SessaoEVP(models.Model):
    """Uma sessão de escuta EVP (Electronic Voice Phenomenon)."""
    STATUS_CHOICES = [
        ('ativa', 'Em Andamento'),
        ('encerrada', 'Encerrada'),
    ]

    sessao_investigacao = models.ForeignKey(
        SessaoInvestigacao, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sessoes_evp',
        verbose_name="Sessão de Investigação"
    )
    titulo = models.CharField(max_length=200, default="Sessão EVP")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ativa')
    local = models.CharField(max_length=300, blank=True)
    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(null=True, blank=True)
    total_capturas = models.IntegerField(default=0)
    total_anomalias = models.IntegerField(default=0)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = "Sessão EVP"
        verbose_name_plural = "Sessões EVP"
        ordering = ['-data_inicio']

    def __str__(self):
        return f"EVP #{self.id} — {self.titulo} ({self.status})"

    @property
    def duracao(self):
        fim = self.data_fim or timezone.now()
        return fim - self.data_inicio

    def encerrar(self):
        self.status = 'encerrada'
        self.data_fim = timezone.now()
        registros = self.registros.all()
        self.total_capturas = registros.count()
        self.total_anomalias = registros.filter(e_anomalia=True).count()
        self.save()


class RegistroEVP(models.Model):
    """Um registro individual de captura EVP com análise IA."""
    CLASSIFICACAO_CHOICES = [
        ('silencio', 'Silêncio'),
        ('ruido', 'Ruído Ambiental'),
        ('voz_humana', 'Voz Humana Normal'),
        ('padrao_anomalo', 'Padrão Anômalo'),
        ('possivel_evp', 'Possível EVP'),
        ('evp_confirmado', 'EVP Confirmado pela IA'),
    ]

    sessao = models.ForeignKey(
        SessaoEVP, on_delete=models.CASCADE,
        related_name='registros', null=True, blank=True,
        verbose_name="Sessão EVP"
    )
    data_captura = models.DateTimeField(auto_now_add=True)

    # Dados de áudio capturados no browser
    transcricao = models.TextField(blank=True, verbose_name="Transcrição (Speech API)")
    nivel_audio = models.FloatField(default=0, verbose_name="Nível de Áudio (RMS)")
    frequencia_dominante = models.FloatField(null=True, blank=True, verbose_name="Frequência Dominante (Hz)")
    frequencias_anomalas = models.JSONField(default=list, verbose_name="Frequências Anômalas (Hz)")
    variacao_magnetica = models.FloatField(default=0)

    # Análise IA
    e_anomalia = models.BooleanField(default=False, verbose_name="É Anomalia?")
    classificacao_ia = models.CharField(
        max_length=20, choices=CLASSIFICACAO_CHOICES,
        default='silencio', verbose_name="Classificação IA"
    )
    analise_ia = models.TextField(blank=True, verbose_name="Análise Detalhada IA")
    confianca_ia = models.FloatField(null=True, blank=True, verbose_name="Confiança IA (%)")
    nota_paranormal = models.IntegerField(default=0, verbose_name="Nota Paranormal (0-10)")
    mensagem_detectada = models.TextField(blank=True, verbose_name="Mensagem Detectada pela IA")

    # NOVO: Campos Fase 4 - Aura's Brain
    dimensao_estimada = models.CharField(max_length=20, default="3D", verbose_name="Dimensão Estimada")
    fusao_dados = models.JSONField(null=True, blank=True, verbose_name="Dados de Fusão Aura Core")

    class Meta:
        verbose_name = "Registro EVP"
        verbose_name_plural = "Registros EVP"
        ordering = ['-data_captura']

    def __str__(self):
        return f"EVP-REG-{self.id} | {self.get_classificacao_ia_display()} | Nota: {self.nota_paranormal}/10"

    @property
    def nivel_alerta(self):
        if self.nota_paranormal >= 8:
            return 'CRÍTICO'
        elif self.nota_paranormal >= 6:
            return 'ALTO'
        elif self.nota_paranormal >= 4:
            return 'MÉDIO'
        return 'BAIXO'