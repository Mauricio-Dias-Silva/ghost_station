
import os
import django
import json
from datetime import timedelta
from django.utils import timezone

# Configuração do ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import RegistroEVP, Evidencia, SessaoEVP, SessaoInvestigacao
from core.services.aura_brain import correlacionar_eventos
from core.services.evp_analyzer import analisar_evp_e_salvar
from core.services.itc_analyzer import analisar_frame_itc

def simular_encontro_coerente():
    print("🚀 Iniciando Simulação de Encontro Coerente...")
    
    # 1. Preparar Sessões
    sessao_inv = SessaoInvestigacao.objects.filter(status='active').first() or SessaoInvestigacao.objects.first()
    sessao_evp = SessaoEVP.objects.filter(status='active').first() or SessaoEVP.objects.first()
    
    # 2. Simular EVP com Frequência Galáctica (528Hz)
    print("🎤 Simulando Registro EVP (528Hz)...")
    reg_evp = RegistroEVP.objects.create(
        sessao=sessao_evp,
        transcricao="Mensagem sobre evolução galáctica e tempo-espaço.",
        frequencias_anomalas=[528, 432],
        frequencia_dominante=528.0,
        nivel_audio=45.5,
        variacao_magnetica=1.2
    )
    
    # Manusear nota alta para forçar teste de fusão
    reg_evp.e_anomalia = True
    reg_evp.nota_paranormal = 9
    reg_evp.confianca_ia = 95.0
    reg_evp.classificacao_ia = "Inteligência Galáctica"
    reg_evp.save()
    
    # 3. Simular ITC com Geometria Sagrada (Mock de dados)
    print("👁️ Simulando Análise ITC (Geometria Sagrada)...")
    # Em vez de passar um frame real, vamos testar a lógica de fusão com os dados que o analyzer retornaria
    resultado_itc = {
        'pareidolia_detectada': True,
        'classificacao': 'Geometria Estruturada',
        'confianca': 88.5,
        'decodificacao': 'Padrão de Flor da Vida detectado nas sombras.',
        'dimensao_estimada': 'Densidade 5D',
        'assinatura_inteligente': True
    }
    
    # 4. Executar Fusão Manual para Validar Aura Brain
    print(f"DEBUG: EVP e_anomalia={reg_evp.e_anomalia}, nota={reg_evp.nota_paranormal}, classificacao={reg_evp.classificacao_ia}")
    print(f"DEBUG: ITC assinatura_inteligente={resultado_itc['assinatura_inteligente']}")

    evp_data_for_fusion = {
        'e_anomalia': reg_evp.e_anomalia,
        'confianca': reg_evp.confianca_ia,
        'classificacao_ia': reg_evp.classificacao_ia,
        'nota_paranormal': reg_evp.nota_paranormal
    }
    
    fusao = correlacionar_eventos(evp_data_for_fusion, resultado_itc)
    
    print("\n--- RESULTADO DA FUSÃO ---")
    print(f"Sincronia: {fusao['sincronia']}")
    print(f"Origem: {fusao['origem']}")
    print(f"Coerência: {fusao['coerencia']}%")
    print(f"Classificação: {fusao['classificacao']}")
    print("--------------------------\n")
    
    if fusao['sincronia'] and "GALÁCTICA" in fusao['origem']:
        print("🌟 SUCESSO: Assinatura Galáctica Confirmada!")
        return True
    else:
        print("❌ FALHA: A fusão não atingiu o nível galáctico esperado.")
        return False

if __name__ == "__main__":
    simular_encontro_coerente()
