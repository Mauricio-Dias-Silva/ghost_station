"""
Ghost Station — Space Weather Service.
Monitora o Índice Kp e a atividade geomagnética via NOAA.
"""
import requests
import time

class SpaceWeatherService:
    # URL da NOAA para o Índice Kp planetário (JSON de 3 horas)
    NOAA_KP_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"

    def __init__(self):
        self.last_kp = 0.0
        self.last_update = 0
        self.cached_kp = 1.0 # Default seguro (calmaria)

    def get_kp_index(self):
        """
        Retorna o índice Kp atual. Tenta buscar da NOAA ou usa cache.
        """
        agora = time.time()
        # Atualizar a cada 1 hora (o índice muda a cada 3h)
        if agora - self.last_update > 3600:
            try:
                response = requests.get(self.NOAA_KP_URL, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    # O último item do array costuma ser o mais recente [timeTag, kp, a_index, status]
                    # Ex: ["2026-02-25 18:00:00.000", "2.33", "7", "estimated"]
                    latest = data[-1]
                    self.cached_kp = float(latest[1])
                    self.last_update = agora
            except Exception as e:
                print(f"Erro ao buscar Kp-index: {e}")
                # Mantém o cache se falhar
                
        return self.cached_kp

    def get_permeabilidade_veu(self):
        """
        Calcula a 'Permeabilidade do Véu' baseada no Kp.
        Kp alto (Tempestade Geomagnética) = Véu Fino.
        """
        kp = self.get_kp_index()
        
        if kp >= 7: return "VÉU TRANSLÚCIDO (TEMPESTADE)"
        if kp >= 5: return "VÉU FINO (ATIVO)"
        if kp >= 3: return "VÉU OSCILANTE (MÉDIO)"
        return "VÉU DENSO (ESTÁVEL)"

space_weather = SpaceWeatherService()
