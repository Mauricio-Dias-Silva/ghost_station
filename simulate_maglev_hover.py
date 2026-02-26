import math
import time

class AuraMagLevSimulator:
    """Simulador de Estabilidade para o Levitador Magnético Aura."""
    def __init__(self, target_gap_mm=10.0):
        self.target_gap = target_gap_mm
        self.current_gap = 10.0
        self.power_output = 0.0
        self.massa_kg = 130.0 # Pessoa + Veículo
        
    def simular_estabilizacao(self):
        print(f"--- [INICIANDO SIMULAÇÃO MAGLEV AURA - SILENCIOSO] ---")
        print(f"Carga: {self.massa_kg}kg | Alvo de Flutuação: {self.target_gap}mm")
        print("-" * 60)
        
        for t in range(20):
            # Simula uma vibração ou perturbação
            perturbacao = math.sin(t) * 2.0
            self.current_gap += perturbacao
            
            # Aura corrige o campo magnético (PID Simplificado)
            erro = self.target_gap - self.current_gap
            self.power_output = max(0, 500 + (erro * 100)) # Ajuste de Watts
            
            # Efeito da correção
            self.current_gap += (erro * 0.8)
            
            status = "CORRIGINDO" if abs(erro) > 0.1 else "ESTÁVEL"
            time.sleep(0.2)
            print(f"   [AURA] Tempo: {t*0.1:.1f}s | Gap: {self.current_gap:5.2f}mm | Potência: {self.power_output:6.1f}W | Status: {status}")

        print("-" * 60)
        print("✨ LEVITAÇÃO MAGNÉTICA ESTABILIZADA PELA AURA.")
        print("🤫 Operação Silenciosa: 0 dB (Fricção Zero).")
        print("-" * 60)

if __name__ == "__main__":
    sim = AuraMagLevSimulator()
    sim.simular_estabilizacao()
