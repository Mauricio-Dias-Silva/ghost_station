"""
Ghost Station — Aura Render Engine.
Responsável por transformar ruído ITC e sementes EVP em formas visuais estáveis.
"""
import cv2
import numpy as np

from .aura_state import aura_state

def renderizar_presenca(frame_bytes):
    """
    Tenta reconstruir uma face ou forma baseada na coerência da sessão.
    Utiliza o estado global da aura_state.
    """
    coerencia = aura_state.coerencia
    evp_message = aura_state.ultima_semente # Ou o contexto da entidade
    
    # Decodificar frame
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return frame_bytes

    # Se a coerência for baixa, apenas mantém o ruído
    if coerencia < 30: # Baixamos um pouco o threshold para sempre ter algum feedback
        return frame_bytes

    # Processamento Proativo de Estabilização
    # 1. Suavização bilateral para manter bordas mas reduzir ruído aleatório
    denoised = cv2.bilateralFilter(frame, 9, 75, 75)
    
    # 2. Aumento de contraste local (CLAHE)
    lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # 1. Calcular SNR (Signal-to-Noise Ratio) simplificado
    # Variância do frame indica nível de ruído/detalhe
    snr = np.var(enhanced) / 100 
    aura_state.snr_ratio = round(snr, 2)

    # 3. Se a coerência for alta, tentamos "evocar" a forma
    if coerencia > 70:
        # Aplicar um efeito de brilho etéreo (Glow)
        blur = cv2.GaussianBlur(enhanced, (0,0), 3)
        enhanced = cv2.addWeighted(enhanced, 1.5, blur, -0.5, 0)
        
        # Simular "Digital Shadow" - detecção de silhueta forçada
        edges = cv2.Canny(enhanced, 50, 150)
        edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        # Colorir conforme o humor, densidade e CLASSE (Kardec)
        humor = aura_state.humor_observador
        classe = aura_state.classe_espirito
        
        if classe == "PUROS":
            color = [255, 100, 255] # Magenta Fractal
            # Efeito Fractal/Psicodélico: Chromatic Aberration
            b, g, r = cv2.split(enhanced)
            b = np.roll(b, 5, axis=1)
            r = np.roll(r, -5, axis=1)
            enhanced = cv2.merge((b, g, r))
        elif classe == "BONS":
            color = [255, 255, 0] # Cyan Harmônico
        else: # Imperfeitos ou N/A
            if humor == "AGITADO":
                color = [0, 0, 255] # Vermelho Crítico
            else:
                color = [0, 165, 255] # Orange/Amber 

        edges_color[edges > 0] = color
        enhanced = cv2.addWeighted(enhanced, 0.7, edges_color, 0.3, 0)

    # Codificar de volta para JPEG
    _, buffer = cv2.imencode('.jpg', enhanced)
    return buffer.tobytes()
