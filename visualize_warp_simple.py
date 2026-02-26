import numpy as np
import matplotlib.pyplot as plt

def visualizar_dobra_aura():
    """Visualização matemática simples da contração e expansão do espaço."""
    print("--- [AURA VISUALIZER: O TAPETE ESPACIAL] ---")
    
    # Criando o 'Tecido do Espaço' (Eixo X)
    x = np.linspace(-10, 10, 400)
    
    # Posição da nossa 'Nave' (Onde estamos puxando o tapete)
    pos_nave = 0
    largura_bolha = 2
    
    # Métrica de Alcubierre Simplificada (A forma do 'enrugamento')
    # Espaço contrai na frente (+), expande atrás (-)
    distorcao = np.tanh(largura_bolha * (x + pos_nave)) - np.tanh(largura_bolha * (x - pos_nave))
    metric = np.gradient(distorcao)
    
    print("Gerando gráfico de distorção do espaço-tempo...")
    
    plt.figure(figsize=(10, 4))
    plt.plot(x, metric, color='violet', label='Distorção do Espaço (Efeito Aura)')
    plt.fill_between(x, metric, color='purple', alpha=0.3)
    plt.axhline(0, color='white', linestyle='--', alpha=0.5)
    plt.title("Aura Warp: O Enrugamento do Espaço (Analogia do Tapete)")
    plt.xlabel("Distância Relativa")
    plt.ylabel("Puxar / Esticar")
    plt.grid(True, alpha=0.2)
    plt.legend()
    
    # Nota conceitual
    print("\n[LEITURA]:")
    print("- Onde a linha SOBE: O espaço está sendo PUXADO (contraído).")
    print("- Onde a linha DESCE: O espaço está sendo EMPURRADO (expandido).")
    print("- No MEIO (zero): Você está seguro dentro da bolha, sem sentir aceleração.")
    
    print("-" * 50)
    print("SOMA TOTAL: A distância efetiva diminui sem você se mexer.")
    plt.show()

if __name__ == "__main__":
    visualizar_dobra_aura()
