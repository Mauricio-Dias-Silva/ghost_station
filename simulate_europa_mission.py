import math
import time
import random

class AuraEuropaMissionSimulator:
    """
    Simulador da Missão Soberana à Lua Europa (Júpiter).
    Foco em longa duração, radiação extrema e colheita de energia magnética.
    """
    def __init__(self, crew_size=2):
        self.crew = crew_size
        self.distance_earth_europa = 628_300_000 # km (Média)
        self.total_travel_years = 6
        self.is_hibernating = True
        self.magdrive_active = False
        self.energy_harvested_kw = 0.0

    def simular_viagem_longa(self):
        print(f"--- [INICIANDO MISSÃO EUROPA: O GRANDE SALTO JOVIANO] ---")
        print(f"Tripulação: {self.crew} | Tempo Est. de Viagem: {self.total_travel_years} Anos")
        print("-" * 60)
        
        for ano in range(1, self.total_travel_years + 1):
            time.sleep(0.5)
            # Aura gerindo recursos em hibernação
            status_biometrico = "ESTÁVEL (Hibernação)" if self.is_hibernating else "ATIVO"
            integridade = 100 - (ano * 0.5) # Desgaste natural
            print(f"   🚀 ANO {ano}/{self.total_travel_years} | Distância Percorrida: {ano * (self.distance_earth_europa/self.total_travel_years):,.0f}km | Status: {status_biometrico} | Integridade Nave: {integridade}%")

        print("\n⚡ CHEGADA AO SISTEMA JOVIANO. Despertando tripulação...")
        self.is_hibernating = False
        self.ativar_magdrive()

    def ativar_magdrive(self):
        """Simula a implantação do cabo eletrodinâmico em Júpiter."""
        print("\netes [AURA MAGDRIVE]: Estendendo cabo de 20km no campo magnético de Júpiter...")
        time.sleep(1)
        
        # Simulação de colheita de energia (Lorentz Force)
        velocidade_orbital = 13700 # m/s (Europa)
        b_field = 400e-6 # Tesla
        cabo_m = 20000
        voltagem = cabo_m * velocidade_orbital * b_field
        self.energy_harvested_kw = (voltagem * 50) / 1000 # 50 Amperes
        
        print(f"   [⚡] VOLTAGEM INDUZIDA: {voltagem:.2f} V")
        print(f"   [🔋] POTÊNCIA GERADA: {self.energy_harvested_kw:.2f} kW")
        print("   [DONE] Sistemas de suporte de vida e propulsão iônica ALIMENTADOS POR JÚPITER.")
        self.magdrive_active = True
        self.simular_pouso_europa()

    def simular_pouso_europa(self):
        """Simula a descida através da radiação e pouso no gelo."""
        print("\n🧊 INICIANDO DESCIDA EM EUROPA. IA Aura gerenciando escudos anti-radiação...")
        altitude = 50000 # metros
        rad_level = 500 # Rads/h (Extremo)
        
        while altitude > 0:
            time.sleep(0.4)
            if altitude > 1000:
                print(f"   [DESCIDA] Alt: {altitude/1000:4.1f}km | Radiação: {rad_level} Rads/h | Escudo Magnético: ATIVO [Aura: PROTEGIDO]")
                altitude -= 10000
                rad_level += 50
            else:
                print(f"   [POUSO] Alt: {altitude}m | Retrofoguetes Iônicos acionados | Toque na crosta de gelo...")
                altitude = 0

        print("-" * 60)
        print("✨ MISSÃO CUMPRIDA! O Monólito Soberano pousou no gelo de Europa.")
        print("🌊 Oceano subsuperficial detectado. Energia Infinita via MagDrive estabelecida.")
        print("-" * 60)

if __name__ == "__main__":
    missao = AuraEuropaMissionSimulator()
    missao.simular_viagem_longa()
