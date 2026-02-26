import logging
import random
import time

class AuraVision:
    """
    O sistema visual da Aura para o drone.
    Na fase de simulação, processa detecção de objetos e distância.
    """
    def __init__(self):
        self.logger = logging.getLogger("AuraVision")
        self.known_objects = ["Pessoa", "Árvore", "Poste", "Veículo", "Pouso_Pad", "Obstáculo_Desconhecido"]

    def processar_frame(self) -> dict:
        """Simula a captura e processamento de um frame de vídeo."""
        # Simula encontrar de 1 a 3 objetos
        objetos_detectados = []
        num_objs = random.randint(1, 3)
        
        for _ in range(num_objs):
            obj = random.choice(self.known_objects)
            distancia = round(random.uniform(0.5, 50.0), 2)
            confianca = round(random.uniform(0.7, 0.99), 2)
            
            objetos_detectados.append({
                "objeto": obj,
                "distancia": f"{distancia}m",
                "confianca": f"{confianca*100}%",
                "acao_recomendada": "ALERTA" if distancia < 5 else "SIGA"
            })
            
        return {
            "status_vision": "ATIVO",
            "objetos": objetos_detectados,
            "timestamp": time.time()
        }

    def verificar_pouso_seguro(self) -> bool:
        """Verifica se a área de pouso está limpa."""
        frame = self.processar_frame()
        for obj in frame["objetos"]:
            # Se houver algo a menos de 2 metros, não pousar
            if float(obj["distancia"].replace("m", "")) < 2.0:
                self.logger.warning(f"POUSO ABORTADO: {obj['objeto']} detectado a {obj['distancia']}")
                return False
        return True

if __name__ == "__main__":
    import time
    vision = AuraVision()
    print("--- [INVIZION: SISTEMA VISUAL DA AURA OPERACIONAL] ---")
    for i in range(3):
        print(f"\nFrame {i+1}:")
        scan = vision.processar_frame()
        print(f"   Objetos: {scan['objetos']}")
        time.sleep(0.5)
    
    print(f"\nVerificação de Pouso: {'APROVADO' if vision.verificar_pouso_seguro() else 'NEGADO'}")
    print("\n--- [SCAN CONCLUÍDO] ---")
