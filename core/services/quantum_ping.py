"""
Ghost Station — Quantum Ping Service.
Gerencia o disparo de frequências Solfeggio e a lógica de Ecolocalização Ativa.
"""
import time
from .aura_state import aura_state

class QuantumPingService:
    # Frequências Solfeggio e seus propósitos espirituais/técnicos
    FREQUENCIES = {
        '396': {'nome': 'Redução de Medo', 'meta': 'Limpeza de Campo'},
        '417': {'nome': 'Facilitação de Mudança', 'meta': 'Desbloqueio de Fluxo'},
        '528': {'nome': 'Reparo de DNA / Milagres', 'meta': 'Sincronia Biológica'},
        '639': {'nome': 'Conexão / Relacionamentos', 'meta': 'Ponte de Consciência'},
        '741': {'nome': 'Despertar Intuição', 'meta': 'Claridade de Sinal'},
        '852': {'nome': 'Retorno à Ordem Espiritual', 'meta': 'Frequência de Origem'}
    }

    def __init__(self):
        self.last_ping_time = 0
        self.is_active = False

    def emitir_ping(self, freq_key):
        """
        Simula o disparo de um ping no backend.
        O som real é gerado no frontend via Web Audio API.
        """
        if freq_key not in self.FREQUENCIES:
            return {'status': 'erro', 'msg': 'Frequência não catalogada'}
        
        freq_info = self.FREQUENCIES[freq_key]
        self.last_ping_time = time.time()
        self.is_active = True
        
        # O Ping aumenta a sensibilidade da Aura temporariamente
        aura_state.coerencia = min(100, aura_state.coerencia + 5)
        aura_state.adicionar_mensagem('SISTEMA', f'PULSO QUÂNTICO EMITIDO: {freq_key}Hz ({freq_info["nome"]})')
        
        return {
            'status': 'ok',
            'frequencia': freq_key,
            'info': freq_info,
            'timestamp': time.strftime('%H:%M:%S')
        }

    def calcular_eco(self, visual_anomalies):
        """
        Verifica se houve uma reação visual imediata após o ping.
        """
        if not self.is_active:
            return 0
        
        tempo_desde_ping = time.time() - self.last_ping_time
        if tempo_desde_ping > 5: # Efeito dura 5 segundos
            self.is_active = False
            return 0
        
        # Se houver anomalia visual logo após o ping, o "Eco" é alto
        if visual_anomalies:
            return 1.5 # Multiplicador de sensibilidade
        
        return 1.1

quantum_ping = QuantumPingService()
