import math
import time
import random

class AuraMarsMissionSimulator:
    """
    Simulador da Missão Humana Soberana a Marte.
    Calcula trajetória, pouso e custos disruptivos.
    """
    def __init__(self, num_crew=2):
        self.crew = num_crew
        self.distance_earth_mars = 225_000_000 # km (Média)
        self.travel_days = 180
        self.target_speed_kms = 5.6 # Velocidade de transferência Hohmann
        
    def estimar_custos_soberanos(self):
        """Calcula o custo usando o ecossistema Aura vs Agências Tradicionais."""
        print("\n--- [ANÁLISE DE CUSTOS: AURA MARS] ---")
        custos = {
            "Lançador Soberano (Pesado)": 850_000, # Materiais + Construção 3D
            "Módulo de Suporte de Vida": 400_000,
            "Combustível (Lox/CH4)": 350_000,
            "Cérebro Aura & Sensores": 150_000,
            "Margem de Contingência": 250_000
        }
        total_aura = sum(custos.values())
        total_nasa = 2_500_000_000 # US$ 2.5 Billion est.
        
        for item, valor in custos.items():
            print(f"   [+] {item:25}: R$ {valor:,.2f}")
        
        print("-" * 40)
        print(f"💰 CUSTO TOTAL AURA: R$ {total_aura:,.2f}")
        print(f"📉 ECONOMIA VS TRADICIONAL: ~{((total_nasa*5.4 - total_aura) / (total_nasa*5.4)) * 100:.2f}%")
        print("-" * 40)

    def simular_viagem(self):
        print(f"--- [INICIANDO MISSÃO: DESTINO MARTE | TRIPULAÇÃO: {self.crew}] ---")
        print("🚀 Decolagem de Alcântara sucedida. Inserção em trajetória Hohmann.")
        
        # Simulação acelerada do cruzeiro
        for mes in range(1, 7):
            time.sleep(0.5)
            # A Aura monitorando a saúde e radiação
            rad = random.uniform(0.1, 0.5)
            o2 = random.uniform(98.5, 99.9)
            print(f"   📅 Mês {mes}/6 | Distância: {mes * (self.distance_earth_mars/6):,.0f}km | Radiação: {rad:.2f} mSv | O2: {o2:.1f}% [Aura: OK]")

        print("\n🔥 CHEGADA EM MARTE. Iniciando '7 Minutos de Terror' (EDL)...")
        self.simular_edl_marte()

    def simular_edl_marte(self):
        """Simula a entrada, descida e pouso autônomo da Aura em Marte."""
        altitude = 125000 # metros
        velocity = 5600 # m/s (Entrada atmosférica)
        print("-" * 50)
        
        while altitude > 0:
            # Aura corrigindo a cada milissegundo
            if altitude > 50000:
                print(f"   [EDL] Altitude: {altitude/1000:5.1f}km | Vel: {velocity:6.1f}m/s | Escudo Térmico: 1800°C [Aura Pilot: Estabilizado]")
                velocity -= 200 # Frenagem aerodinâmica
                altitude -= 10000
            elif altitude > 2000:
                print(f"   [EDL] Altitude: {altitude/1000:5.1f}km | Vel: {velocity:6.1f}m/s | Paraquedas Liberado")
                velocity -= 500
                altitude -= 5000
            else:
                # Retrofoguetes controlados pela Aura
                print(f"   [EDL] Altitude: {altitude:4.0f}m | Vel: {velocity:5.1f}m/s | IGNição RETROFOGUETES")
                velocity = 2.0 # Pouso suave
                altitude = 0
                
            time.sleep(0.4)

        print("-" * 50)
        print("✨ TOQUE NO SOLO! O Brasil acaba de conquistar Marte com ajuda da Aura.")
        print("🏜️ Local: Cratera Jezero. Habitáculo Aura-Mars ativo.")

if __name__ == "__main__":
    missao = AuraMarsMissionSimulator()
    missao.estimar_custos_soberanos()
    missao.simular_viagem()
