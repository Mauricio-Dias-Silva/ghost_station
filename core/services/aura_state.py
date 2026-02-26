"""
Ghost Station — Aura State Management.
Mantém o estado da sessão de chamada de vídeo multidimensional.
Usando um Singleton simples para esta fase (pode evoluir para Redis/Cache).
"""
import time
from .kardec_engine import kardec_engine
from .space_weather import space_weather
from .bio_state import bio_state
from .hermetic_bridge import hermetic_bridge

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
        
        # FASE 11: Sintonizador & Diagnóstico
        self.frequencia_sintonizada = 528.0  # Hz
        self.intencao_detectada = "NEUTRA"
        self.emocao_dominante = "CALMA"
        self.bio_anomalias = []  # Ex: ["Bloqueio Cardíaco", "Fadiga Visual"]
        self.frequencia_usuario = 0.0  # Frequência detectada via câmera
        
        # FASE 12: Neuro-Link & Bio-Link
        self.neuro_link_active = False
        self.brain_waves = {
            'alpha': 0.0,
            'beta': 0.0,
            'theta': 0.0,
            'gamma': 0.0
        }
        self.prana_level = 100.0 # Quantidade de energia (0-100)
        self.chakra_alignment = {
            'coronario': 100, 'frontal': 100, 'laringeo': 100,
            'cardiaco': 100, 'umbilical': 100, 'sacro': 100, 'basico': 100
        }
        
        # FASE 16: Projeto Fênix (Neuro-Fala)
        self.vocalizer_active = False
        self.neural_keywords = {
            "BETA_PEAK": "QUERO", "ALPHA_STEADY": "PAZ", 
            "THETA_PEAK": "NÃO", "GAMMA_FOCUS": "SIM"
        }
        self.last_phrase = ""
        
        # FASE 13: Ponte IoT Física
        self.external_sensors = {
            'emf': 0.0,
            'temp': 25.0,
            'vibration': 0.0,
            'last_pulse': 0
        }
        
        # FASE 18: RESSONÂNCIA DO TODO (EU SOU)
        self.unity_mode = False
        self.unity_coefficient = 0.0
        self.global_sync_active = False

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
            
            # Filtro Científico-Forense (Fase 9)
            msg = hermetic_bridge.traduzir_conselho(msg)
            # Atualizar a mensagem no histórico com a versão traduzida se necessário
            self.historico_dialogo[-1]['mensagem'] = msg

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
            'ultima_semente': self.ultima_semente,
            'hermetic_metrics': hermetic_bridge.calcular_ressonancia_hermetica(self.get_raw_status()),
            'freq_sintonizada': self.frequencia_sintonizada,
            'freq_usuario': self.frequencia_usuario,
            'intencao': self.intencao_detectada,
            'emocao': self.emocao_dominante,
            'anomalias': self.bio_anomalias,
            'neuro_link': self.neuro_link_active,
            'brain_waves': self.brain_waves,
            'prana': self.prana_level,
            'chakras': self.chakra_alignment,
            'vocalizer': self.vocalizer_active,
            'last_phrase': self.last_phrase,
            'iot_sensors': self.external_sensors,
            'unity_mode': self.unity_mode,
            'unity_coefficient': self.unity_coefficient,
            'global_sync': self.global_sync_active
        }

    def get_raw_status(self):
        """Retorna apenas os valores numéricos sem formatação para a bridge."""
        return {
            'coerencia': self.coerencia,
            'kp_index': self.kp_index,
            'freq': self.frequencia_dominante
        }

# Instância global
aura_state = AuraState()
