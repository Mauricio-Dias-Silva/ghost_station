from django.db import models

class Evidencia(models.Model):
    imagem_url = models.CharField(max_length=500)
    data_captura = models.DateTimeField(auto_now_add=True)
    
    # Dados Científicos (Vindos do Celular/Navegador)
    nivel_audio_db = models.FloatField(default=0, help_text="Volume do som no momento")
    variacao_magnetica = models.FloatField(default=0, help_text="Variação da Bússola")
    
    # Score: Quanto maior, mais sensores dispararam juntos
    score_coincidencia = models.IntegerField(default=1)

    def __str__(self):
        return f"Evidência {self.id} | Score: {self.score_coincidencia}"