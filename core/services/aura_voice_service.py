import os

class AuraVoice:
    """Serviço de voz da Aura para guiar o Mauricio na montagem e missões."""
    
    def __init__(self, mode="TTS"):
        self.mode = mode
        print("🎙️ [AURA VOICE] Sistema de áudio inicializado.")

    def speak(self, text: str):
        """Fala o texto usando o mecanismo disponível no Windows ou simula."""
        print(f"🔊 AURA: {text}")
        
        # Tentativa de usar o PowerShell SAPI (nativo no Windows do usuário)
        try:
            # Comando PowerShell para converter texto em voz
            ps_command = f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak("{text}")'
            os.system(f'powershell -Command "{ps_command}"')
        except Exception as e:
            print(f"⚠️ [Voz Indisponível]: {e}")

    def guiar_montagem(self, etapa: int):
        """Guia passo a passo da montagem física."""
        etapas = {
            1: "Corte o tubo de PVC em sessenta centímetros. Verifique o alinhamento.",
            2: "Marque o bocal para os quatro servos na base. Use precisão de milímetros.",
            3: "Conecte o sensor MPU 6050 no centro de massa. Eu estou aqui para calibrar.",
            4: "Ligue os fios seguindo o blueprint de fiação. Cuidado com o negativo comum."
        }
        if etapa in etapas:
            self.speak(etapas[etapa])
        else:
            self.speak("Etapa de montagem concluída. Pronto para o teste de gimbal.")

if __name__ == "__main__":
    aura = AuraVoice()
    aura.speak("Mauricio, eu sou a Aura. Vamos construir o futuro do Brasil juntos.")
    aura.guiar_montagem(1)
