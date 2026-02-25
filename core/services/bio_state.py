"""
Ghost Station — BioState Management.
Responsável por gerenciar os sinais vitais do observador e calcular a coerência cardíaca.
Pode ser alimentado por sensores externos ou simulação guiada.
"""
import time
import math

class BioState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BioState, cls).__new__(cls)
            cls._instance.reset()
        return cls._instance

    def reset(self):
        self.bpm = 70.0  # Batimentos por minuto
        self.estresse = 20.0  # 0 a 100
        self.coerencia_cardiaca = 0.0 # 0 a 100 (Sincronia com o pacer)
        self.energia_metabolica = 100.0 # Bateria humana
        self.last_update = time.time()
        self.session_start = time.time()

    def update_vital_signs(self, bpm=None, estresse=None):
        if bpm is not None:
            self.bpm = bpm
        if estresse is not None:
            self.estresse = estresse
        self.last_update = time.time()

    def calcular_coerencia(self, tempo_ciclo=10):
        """
        Simula a coerência baseada na respiração rítmica (pode ser validada por sensores).
        Um ciclo de 10s (6 respirações por minuto) é o ideal.
        """
        elapsed = time.time() - self.session_start
        # Onda senoidal representando a respiração ideal
        onda_ideal = (math.sin(2 * math.pi * elapsed / tempo_ciclo) + 1) / 2
        
        # Coerência aumenta se o estresse for baixo e o BPM estiver estável
        fator_estresse = (100 - self.estresse) / 100
        self.coerencia_cardiaca = round(onda_ideal * 100 * fator_estresse, 2)
        
        # Consumo metabólico: sessões longas cansam o observador
        # Perda de 1% de energia a cada 5 minutos de foco intenso
        perda = (time.time() - self.last_update) / 300
        self.energia_metabolica = max(0, self.energia_metabolica - perda)
        
        return self.coerencia_cardiaca

    def get_status(self):
        self.calcular_coerencia()
        return {
            'bpm': round(self.bpm, 1),
            'estresse': round(self.estresse, 1),
            'coerencia': self.coerencia_cardiaca,
            'energia': round(self.energia_metabolica, 1),
            'fadiga_alerta': self.energia_metabolica < 20
        }

bio_state = BioState()
