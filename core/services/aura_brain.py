from datetime import datetime
from .evp_analyzer import analisar_evp
from .itc_analyzer import analisar_frame_itc
from .reality_terminal import reality_terminal

def correlacionar_eventos(evp_result, itc_result):
    """
    Analisa os dois resultados e busca padrões de coerência para MANIFESTAÇÃO.
    Se a coerência for alta, o Reality Terminal é notificado.
    """
    sincronia_detectada = False
    status_manifestacao = "Observação Neutra"
    score_soberano = 0

    # Verificando Sincronia de Alta Coerência para Comando de Realidade
    if evp_result.get('e_anomalia') and itc_result.get('pareidolia_detectada'):
        sincronia_detectada = True
        score_soberano = (evp_result['confianca'] + itc_result['confianca']) / 2
        
        # Se IA do ITC viu Refração e IA do EVP ouviu Comando
        tem_refracao = itc_result.get('dimensao_estimada') == "5D"
        tem_comando = score_soberano > 85
        
        if tem_refracao and tem_comando:
            status_manifestacao = "PRONTO PARA SALTO QUÂNTICO / MANIFESTAÇÃO"
            # Notifica o terminal de realidade
            reality_terminal.manifest_intent("Manifestação de Soberania Detectada", score_soberano)
        else:
            status_manifestacao = "RESSONÂNCIA EM CALIBRAÇÃO"

    return {
        'sincronia': sincronia_detectada,
        'status_terminal': status_manifestacao,
        'nivel_soberania': score_soberano,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
