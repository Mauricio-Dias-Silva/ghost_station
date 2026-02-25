"""
Ghost Station — Aura Fusion Core.
Centraliza a cognição unindo dados de áudio (EVP) e vídeo (ITC).
Responsável por identificar Síncrons e Classificar Origem Galáctica.
"""
from datetime import datetime
from .evp_analyzer import analisar_evp
from .itc_analyzer import analisar_frame_itc

def correlacionar_eventos(evp_result, itc_result):
    """
    Analisa os dois resultados e busca padrões de coerência.
    Se ambos detectarem anomalias, o nível de alerta e dimensão sobem.
    """
    sincronia_detectada = False
    classificacao_fusao = "Evento Isolado"
    score_coerencia = 0
    origem_estimada = "Local / Terrestre"

    # Verificando Sincronia de Alta Coerência
    if evp_result.get('e_anomalia') and itc_result.get('pareidolia_detectada'):
        sincronia_detectada = True
        score_coerencia = (evp_result['confianca'] + itc_result['confianca']) / 2
        classificacao_fusao = "SINCRONIA MULTIDIMENSIONAL"
        
        # Lógica de Origem baseada nos prompts novos
        # Se IA do ITC viu geometria e IA do EVP ouviu Harmônicos/Conceitos Cósmicos
        tem_geometria = itc_result.get('assinatura_inteligente', False)
        tem_cosmico = "Galáctica" in evp_result.get('classificacao', '') or evp_result.get('nota_paranormal', 0) > 7
        
        if tem_geometria and tem_cosmico:
            origem_estimada = "INTELIGÊNCIA GALÁCTICA / EU SUPERIOR"
        elif tem_geometria or tem_cosmico:
            origem_estimada = "SINAL INTERDIMENSIONAL (4D/5D)"
        else:
            origem_estimada = "FENÔMENO PARANORMAL LOCAL (3D+)"

    return {
        'sincronia': sincronia_detectada,
        'classificacao': classificacao_fusao,
        'coerencia': score_coerencia,
        'origem': origem_estimada,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
