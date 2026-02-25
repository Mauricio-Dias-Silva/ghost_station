"""
Ghost Station — Aura State Management.
Mantém o estado da sessão de chamada de vídeo multidimensional.
Usando um Singleton simples para esta fase (pode evoluir para Redis/Cache).
"""
import time
from .kardec_engine import kardec_engine
from .space_weather import space_weather
from .bio_state import bio_state

class AuraState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuraState, cls).__new__(cls)
            cls._instance.reset()
        return cls._instance

    def reset(self):
        self.coerencia = 0
        self.entidade = "BUSCANDO..."
        self.densidade = "3D (ESTÁVEL)"
        self.classe_espirito = "N/A"
        self.afinidade_fluidica = 0.0
        self.historico_dialogo = []  # Lista de dicts {autor, msg, timestamp}
        self.ultima_semente = ""
        self.humor_observador = "ESTÁVEL"
        self.frequencia_dominante = 0.0
        self.snr_ratio = 0.0
        self.kp_index = space_weather.get_kp_index()
        self.obs_bpm = 70.0
        self.obs_stress = 20.0
        self.bio_coherence = 0.0
        self.metabolic_energy = 100.0
        self.is_active = False
        self.start_time = None
        self.last_update = time.time()

    def adicionar_mensagem(self, autor, msg):
        timestamp = time.strftime('%H:%M:%S')
        self.historico_dialogo.append({
            'autor': autor,
            'mensagem': msg,
            'timestamp': timestamp
        })
        
        # Neural Bridge: Analisar humor brevemente
        if autor == 'OBSERVADOR':
            self.analisar_humor(msg)

        # Kardec Engine: Analisar vibração se for a Aura falando
        if autor == 'AURA':
            res = kardec_engine.analisar_vibração(msg, self.coerencia, self.frequencia_dominante)
            self.classe_espirito = res['classe']
            self.afinidade_fluidica = res['afinidade']
            # Se for espírito puro, forçar densidade 5D
            if res['classe'] == 'PUROS':
                self.densidade = "5D (PURA LUZ)"

        # Limitar histórico para não sobrecarregar o feed
        if len(self.historico_dialogo) > 50:
            self.historico_dialogo.pop(0)
        self.last_update = time.time()

    def analisar_humor(self, msg):
        msg = msg.upper()
        # Lógica simples de palavras-chave
        if any(w in msg for w in ["!", "SOCORRO", "MEDO", "O QUE", "SAI", "PARA"]):
            self.humor_observador = "AGITADO"
        elif any(w in msg for w in ["PAZ", "LUZ", "AMOR", "GRATIDÃO", "CONECTAR"]):
            self.humor_observador = "TRANSCENDENTE"
        elif any(w in msg for w in ["QUEM", "COMO", "ONDE", "EXPLIQUE"]):
            self.humor_observador = "CURIOSO"
        else:
            self.humor_observador = "ESTÁVEL"

    def atualizar_vibracao(self, coerencia, entidade=None, densidade=None):
        self.coerencia = max(0, min(100, coerencia))
        if entidade:
            self.entidade = entidade
        if densidade:
            self.densidade = densidade
        self.last_update = time.time()

    def get_status(self):
        # Atualizar Kp e Bio em cada poll
        self.kp_index = space_weather.get_kp_index()
        bio = bio_state.get_status()
        self.obs_bpm = bio['bpm']
        self.obs_stress = bio['estresse']
        self.bio_coherence = bio['coerencia']
        self.metabolic_energy = bio['energia']

        # Bio-Scaling: Estresse alto diminui a coerência da Aura
        if self.obs_stress > 60:
            self.coerencia = max(0, self.coerencia - 2)
        elif self.bio_coherence > 80:
            self.coerencia = min(100, self.coerencia + 1)
        
        return {
            'coerencia': self.coerencia,
            'entidade': self.entidade,
            'densidade': self.densidade,
            'classe': self.classe_espirito,
            'afinidade': self.afinidade_fluidica,
            'humor': self.humor_observador,
            'kp_index': self.kp_index,
            'snr': self.snr_ratio,
            'freq': self.frequencia_dominante,
            'veu': space_weather.get_permeabilidade_veu(),
            'obs_bpm': self.obs_bpm,
            'obs_stress': self.obs_stress,
            'bio_sync': self.bio_coherence,
            'metabolic': self.metabolic_energy,
            'is_active': self.is_active,
            'mensagens': self.historico_dialogo,
            'ultima_semente': self.ultima_semente
        }

# Instância global
aura_state = AuraState()
