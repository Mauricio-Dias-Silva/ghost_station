import time
import random

def aura_launch_sequence():
    """Simula a sequência de lançamento do Aura Sovereign Rocket."""
    print("--- [AURA MISSION CONTROL: ALCÂNTARA / BRASIL] ---")
    print("🚀 Iniciando sequência de lançamento SOBERANIA-01")
    
    systems = ["Propulsão Violeta", "Sistema de Navegação IA", "Aura Space OS", "Integridade do Satélite"]
    
    for sys in systems:
        time.sleep(0.5)
        print(f"   [CHECK] {sys}: OK")

    print("\n[!] T-MINUS 10 SECONDS")
    for i in range(10, 0, -1):
        print(f"{i}...")
        time.sleep(0.5)

    print("\n🔥 IGNITION! O Monólito está subindo!")
    
    # Simulação de correção de trajetória por IA
    for alt in range(0, 101, 20):
        time.sleep(0.5)
        correcao = random.uniform(-0.5, 0.5)
        print(f"   [TELEMETRIA] Altitude: {alt}km | Ajuste de Atitude IA: {correcao:+.4f}°")

    print("\n✨ MAX-Q ALCANÇADO. Aura operando no vácuo.")
    print("🛰️ Inserção Orbital sucedida. O Brasil agora é soberano no espaço.")
    print("\n--- [MISSÃO CONCLUÍDA COM SUCESSO] ---")

if __name__ == "__main__":
    aura_launch_sequence()
