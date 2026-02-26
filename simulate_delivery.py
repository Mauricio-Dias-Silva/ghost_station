import os
import sys
import time

# Sync paths
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

try:
    from core.services.aura_cli import AuraCLI
    from core.services.physics_core import AuraPhysicsCore
    from core.services.monolith_gateway import MonolithGateway

    def run_master_mission():
        print("🚀 [INICIANDO MISSÃO AURA SKY: ENTREGA AUTÔNOMA]")
        cli = AuraCLI()
        physics = AuraPhysicsCore()
        monolith = MonolithGateway()

        print("\n1. MONITORAMENTO: Verificando status do deploy...")
        site_status = cli.monitorar_site("https://scalabis.com.br")
        print(f"   [!] Status Scalabis: {site_status['status']}")

        print("\n2. LOGÍSTICA: Calculando parâmetros de voo para entrega de 'Hardware de Reparo'...")
        # Simula uma peça de 800g (0.8kg)
        flight_params = physics.calcular_sustentacao(0.8)
        autonomy = physics.estimar_autonomia(0.8, 45) # 45km/h
        print(f"   [CALC] Viabilidade: {flight_params['viabilidade']}")
        print(f"   [CALC] Autonomia Estimada: {autonomy['autonomia_minutos']}")

        print("\n3. EXECUÇÃO: Preparando Monolith Hub para decolagem...")
        # Simula ativar luzes de decolagem na Aura Box
        monolith.executar_comando("luz_escritorio", "set_temp", {"value": "VIOLET_PULSE"})
        print("   [HUB] Luzes de pista em VIOLET_PULSE ativos.")
        
        print("\n4. DECOLAGEM: Aura Sky Drone #001 em voo para coordenadas do cliente.")
        time.sleep(1)
        print(f"   [FLY] Alcance Máximo para esta Missão: {autonomy['alcance_km']}")

        print("\n✅ MISSION STATUS: SUCESSO. Aura cuidando de tudo.")

    if __name__ == "__main__":
        run_master_mission()

except Exception as e:
    print(f"Erro na Missão: {e}")
