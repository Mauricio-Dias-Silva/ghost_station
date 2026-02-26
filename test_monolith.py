import os
import sys

# Ensure the project root and its parent are in the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(project_root)) # Adds c:\Users\Mauricio\Desktop
sys.path.append(project_root) # Adds c:\Users\Mauricio\Desktop\ghost_station

try:
    from core.services.monolith_gateway import MonolithGateway
except ImportError:
    from ghost_station.core.services.monolith_gateway import MonolithGateway

def run_simulation():
    print("--- [AURA MONOLITH BOOT SEQUENCE] ---")
    gateway = MonolithGateway()
    
    print("\n1. Escaneando dispositivos na rede do Mauricio...")
    devs = gateway.escanear_rede()
    for d in devs:
        print(f"   [SYNCED] {d}")
        
    print("\n2. Executando comando de voz simulado: 'Aura, ligue as luzes do escritório'")
    res = gateway.executar_comando("luz_escritorio", "turn_on")
    print(f"   [RESULT] {res['message']}")
    
    print("\n3. Status Final do Ecossistema:")
    print(gateway.status_geral())
    
    print("\n--- [AURA MONOLITH ONLINE] ---")

if __name__ == "__main__":
    run_simulation()
