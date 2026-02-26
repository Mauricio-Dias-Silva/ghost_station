"""
Ghost Station — Neuro-Vocalizer Service.
Traduz picos neurais em estados semânticos e síntese de fala.
"""
import time
from .aura_state import aura_state

class NeuroVocalizer:
    def process_neural_input(self):
        """
        Analisa o estado atual das ondas cerebrais e dispara gatilhos de fala.
        """
        if not aura_state.vocalizer_active:
            return None

        waves = aura_state.brain_waves
        # Lógica de detecção de 'Picos' ou 'Foco'
        # Ex: Se Gamma > 80, o usuário está focado em um pensamento positivo/afirmativo
        
        target_phrase = ""
        
        if waves.get('gamma', 0) > 80:
            target_phrase = aura_state.neural_keywords.get("GAMMA_FOCUS", "SIM")
        elif waves.get('theta', 0) > 80:
            target_phrase = aura_state.neural_keywords.get("THETA_PEAK", "NÃO")
        elif waves.get('beta', 0) > 70:
            target_phrase = aura_state.neural_keywords.get("BETA_PEAK", "QUERO")
        elif waves.get('alpha', 0) > 90:
            target_phrase = aura_state.neural_keywords.get("ALPHA_STEADY", "PAZ")

        if target_phrase and target_phrase != aura_state.last_phrase:
            aura_state.last_phrase = target_phrase
            aura_state.adicionar_mensagem('NEURO-VOICE', target_phrase)
            return target_phrase
            
        return None

neuro_vocalizer = NeuroVocalizer()
