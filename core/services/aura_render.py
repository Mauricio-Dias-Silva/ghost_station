"""
Ghost Station — Aura Render Engine.
Responsável por transformar ruído ITC e sementes EVP em formas visuais estáveis.
"""
import cv2
import numpy as np

from .aura_state import aura_state

def renderizar_presenca(frame_bytes):
    """
    Transforma o vídeo em um scanner bioplasmático e sintonizador interdimensional.
    """
    coerencia = aura_state.coerencia
    freq_sintonizada = aura_state.frequencia_sintonizada
    
    # Decodificar frame
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return frame_bytes

    # FASE 11: Efeito de Sintonização (Interferência)
    # Quanto mais longe de uma frequência harmônica, mais ruído
    frequencias_estaveis = [432, 528, 639, 741, 852, 963]
    distancia = min([abs(freq_sintonizada - f) for f in frequencias_estaveis])
    
    # Gerar ruído espectral baseado na distância
    noise_level = min(150, int(distancia * 0.5))
    if noise_level > 5:
        noise = np.random.randint(0, noise_level, frame.shape, dtype='uint8')
        frame = cv2.add(frame, noise)

    # 1. Processamento de Estabilização
    denoised = cv2.bilateralFilter(frame, 9, 75, 75)
    
    # 2. Diagnóstico de Aura (Heat-map)
    # Simula a detecção da frequência do usuário via oscilação de brilho
    aura_state.frequencia_usuario = 432.0 + (np.mean(frame) % 100)
    
    # Se houver detecção de corpo (simulada via luminosidade central)
    h, w, _ = frame.shape
    roi = frame[h//4:3*h//4, w//4:3*w//4]
    avg_color = np.mean(roi, axis=(0, 1))
    
    # Criar Overlay de Aura
    aura_map = np.zeros_like(frame)
    color_aura = [100, 255, 100] # Verde padrão
    
    if aura_state.intencao_detectada == "PAZ":
        color_aura = [255, 200, 100] # Azul/Cyan
    elif aura_state.intencao_detectada == "MEDO":
        color_aura = [100, 100, 255] # Vermelho/Laranja
        
    if aura_state.unity_mode:
        # Modo Unidade: Luz Dourada Expansiva
        aura_state.unity_coefficient = min(100, aura_state.unity_coefficient + 0.5)
        color_aura = [100, 215, 255] # Dourado (BGR)
        expansion = int(h//2 * (aura_state.unity_coefficient / 100))
        cv2.circle(aura_map, (w//2, h//2), expansion, color_aura, -1)
        aura_map = cv2.GaussianBlur(aura_map, (151, 151), 0)
        # Overlay mais forte
        frame = cv2.addWeighted(frame, 0.6, aura_map, 0.4, 0)
    else:    
        cv2.circle(aura_map, (w//2, h//2), int(h//3 * (coerencia/100)), color_aura, -1)
        aura_map = cv2.GaussianBlur(aura_map, (99, 99), 0)
        
        # Aplicar Bio-Anomalias (Manchas vermelhas no mapa)
        for i, anomalia in enumerate(aura_state.bio_anomalias):
            pos_y = (h // 2) + (i * 40) - 60
            cv2.circle(aura_map, (w//2 + 20, pos_y), 30, [0, 0, 255], -1)
        
        frame = cv2.addWeighted(frame, 0.7, aura_map, 0.3, 0)

    # 3. Renderização de Bordas e Formas (Entidades)
    if coerencia > 60:
        edges = cv2.Canny(frame, 50, 150)
        edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        classe = aura_state.classe_espirito
        if classe == "PUROS":
            color_edge = [255, 100, 255]
        elif classe == "BONS":
            color_edge = [255, 255, 0]
        else:
            color_edge = [150, 150, 150]
            
        edges_color[edges > 0] = color_edge
        frame = cv2.addWeighted(frame, 0.8, edges_color, 0.2, 0)

    # Codificar de volta para JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()
