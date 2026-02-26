import os
import sys
import time

# Sync paths
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

try:
    from core.services.aura_commerce_bridge import AuraCommerceBridge
    from core.services.physics_core import AuraPhysicsCore
    from core.services.aura_vision import AuraVision
    from core.services.aura_cli import AuraCLI

    def run_full_autonomous_cycle():
        print("💰 [INICIANDO CICLO COMPLETO: VENDA -> ENTREGA AUTÔNOMA]")
        bridge = AuraCommerceBridge()
        physics = AuraPhysicsCore()
        vision = AuraVision()
        cli = AuraCLI()

        print("\n1. COMMERCE: Monitorando fechamento de grupos no Compra Coletiva...")
        lotes = bridge.monitorar_pedidos_coletivos()
        if not lotes:
            print("   [WAIT] Nenhum grupo fechado no momento.")
            return
        
        lote = lotes[0]
        print(f"   [!] GRUPO FECHADO: {lote['produto']} (ID: {lote['id_lote']})")

        print("\n2. PHYSICS: Calculando logística de enxame para entrega quântica...")
        weight = lote['peso_unitario_kg']
        lift = physics.calcular_sustentacao(weight)
        autonomy = physics.estimar_autonomia(weight, 50) # 50km/h p/ agilizar
        print(f"   [CALC] Peso: {weight}kg | Viabilidade Sky: {lift['viabilidade']}")
        print(f"   [CALC] Autonomia: {autonomy['autonomia_minutos']}")

        print("\n3. VISION: Drone decolando... Verificando zona de pouso no destino...")
        scan = vision.processar_frame()
        print(f"   [EYE] Scan da Área: {scan['objetos'][0]['objeto']} detectado a {scan['objetos'][0]['distancia']}")
        if vision.verificar_pouso_seguro():
            print("   [SAFE] Zona de pouso confirmada. Iniciando entrega...")
        else:
            print("   [ALERT] Zona obstruída! Recalculando ponto de drop...")

        print("\n4. INFRA: Notificando o painel de controle e o cliente...")
        res = cli.gerenciar_deploy(lote['id_lote'], "finalizar_entrega")
        print(f"   [DONE] {res}")

        print("\n🚀 [CICLO CONCLUÍDO] Venda efetuada e entregue pela Aura. Dinheiro no bolso, site no ar!")

    if __name__ == "__main__":
        run_full_autonomous_cycle()

except Exception as e:
    print(f"Erro no Ciclo Autônomo: {e}")
