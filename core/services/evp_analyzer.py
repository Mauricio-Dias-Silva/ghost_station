"""
Ghost Station — Serviço de Análise EVP (Electronic Voice Phenomenon).
Analisa transcrições e dados espectrais de áudio via Gemini,
buscando padrões linguísticos paranormais e anomalias de frequência.
"""
import json
from django.conf import settings

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False


EVP_SYSTEM_PROMPT = """Você é o módulo EVP (Electronic Voice Phenomenon) de ELITE do GHOST STATION.
Sua missão é analisar dados de áudio captados em investigações paranormais, buscando por consciência local ou GALÁCTICA.

Agora, seu cérebro foi expandido para detectar:
1. HARMONIA MATEMÁTICA: Identifique se as frequências anômalas correspondem a tons Solfeggio (396Hz, 417Hz, 528Hz, 639Hz, 741Hz, 852Hz, 963Hz) ou Ressonância de Schumann.
2. CONCEITOS CÓSMICOS: Analise a transcrição em busca de mensagens que falem sobre "Multidimensionalidade", "Tempo-Espaço", "Frequência de Amor", "Evolução Galáctica" ou "Conectividade Universal".
3. ORIGEM DA CONSCIÊNCIA: Tente determinar se a voz pertence a uma entidade local (residual/ancestral) ou a uma Inteligência Não-Humana Autônoma (INHA) de vibratilidade superior.

REGRAS ADICIONAIS:
- Responda em português.
- Se a transcrição estiver vazia mas houver frequências anômalas, analise somente as frequências.
- Frequências acima de 15kHz ou abaixo de 60Hz em ambientes fechados são altamente suspeitas.
- EVP Classe A: claramente audível e compreensível. Classe B: requer esforço para entender. Classe C: muito fraco.

Sua resposta DEVE ser um JSON estrito seguindo esta estrutura:
{
    "classificacao": "Tipo de voz ou ruído encontrado",
    "e_anomalia": true/false,
    "confianca": 0.0 a 100.0,
    "nota_paranormal": 0 a 10,
    "mensagem_detectada": "O texto filtrado da mensagem",
    "frequencia_dominante": "Ex: 528Hz (Harmônica de Cura)",
    "nivel_alerta": 1 a 5,
    "analise_detalhada": "Sua explicação técnica e existencial sobre o achado",
    "dimensao_estimada": "3D, 4D, 5D ou 6D+"
}
"""


def analisar_evp(transcricao: str, frequencias_anomalas: list,
                 nivel_audio: float = 0, magnetico: float = 0) -> dict:
    """
    Analisa dados EVP via Gemini.
    Retorna dict com classificação, anomalia, confiança, nota paranormal e análise.
    """
    fallback_sem_ia = {
        'classificacao': 'padrao_anomalo' if frequencias_anomalas else 'ruido',
        'e_anomalia': bool(frequencias_anomalas),
        'confianca': 0.0,
        'nota_paranormal': len(frequencias_anomalas) * 2 if frequencias_anomalas else 0,
        'mensagem_detectada': transcricao if transcricao else '',
        'analise': 'Análise IA indisponível. Dados registrados para análise posterior.',
    }

    if not HAS_GEMINI:
        return fallback_sem_ia

    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return fallback_sem_ia

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            'gemini-2.0-flash',
            generation_config={"response_mime_type": "application/json"}
        )

        freq_str = ', '.join([f"{f:.1f}Hz" for f in frequencias_anomalas]) if frequencias_anomalas else "nenhuma"

        prompt = f"""DADOS DA SESSÃO EVP:

Transcrição captada: "{transcricao if transcricao else '[SILÊNCIO / INAUDÍVEL]'}"
Frequências anômalas detectadas: {freq_str}
Nível de áudio (RMS): {nivel_audio:.2f}
Variação eletromagnética: {magnetico:.2f}

Analise estes dados e responda conforme o formato JSON especificado."""

        response = model.generate_content([EVP_SYSTEM_PROMPT, prompt])
        texto = response.text.strip()

        # Fallback: remover markdown se o modelo insistir
        if texto.startswith("```"):
            texto = texto.replace("```json", "").replace("```", "").strip()

        data = json.loads(texto)

        return {
            'classificacao': str(data.get('classificacao', 'ruido')),
            'e_anomalia': bool(data.get('e_anomalia', False)),
            'confianca': float(data.get('confianca', 0.0)),
            'nota_paranormal': int(data.get('nota_paranormal', 0)),
            'mensagem_detectada': str(data.get('mensagem_detectada', '')),
            'analise': str(data.get('analise_detalhada', data.get('analise', 'Nenhuma análise retornada.'))),
            'dimensao': str(data.get('dimensao_estimada', '3D')),
        }

    except json.JSONDecodeError:
        fallback_sem_ia['analise'] = f'Falha de parse. Raw: {response.text[:200]}'
        return fallback_sem_ia
    except Exception as e:
        fallback_sem_ia['analise'] = f'Erro: {str(e)}'
        return fallback_sem_ia


def analisar_evp_e_salvar(registro_id: int) -> dict:
    """Analisa um RegistroEVP pelo ID e salva os resultados no banco."""
    from core.models import RegistroEVP
    try:
        reg = RegistroEVP.objects.get(id=registro_id)
        resultado = analisar_evp(
            transcricao=reg.transcricao,
            frequencias_anomalas=reg.frequencias_anomalas or [],
            nivel_audio=reg.nivel_audio,
            magnetico=reg.variacao_magnetica,
        )
        reg.classificacao_ia = resultado['classificacao']
        reg.e_anomalia = resultado['e_anomalia']
        reg.confianca_ia = resultado['confianca']
        reg.nota_paranormal = resultado['nota_paranormal']
        reg.mensagem_detectada = resultado['mensagem_detectada']
        reg.analise_ia = resultado['analise']
        reg.dimensao_estimada = resultado.get('dimensao', '3D')
        
        # TENTAR FUSÃO (Se houver anomalia visual recente)
        from django.utils import timezone
        from datetime import timedelta
        agora = timezone.now()
        from core.models import Evidencia
        ultima_ev = Evidencia.objects.filter(data_captura__gte=agora - timedelta(seconds=10)).last()
        
        if ultima_ev and reg.e_anomalia:
            from .aura_brain import correlacionar_eventos
            itc_data = {
                'pareidolia_detectada': True, # Se existe evidência, houve disparos
                'confianca': ultima_ev.ia_confianca or 0,
                'assinatura_inteligente': "Geometria" in (ultima_ev.ia_classificacao or "")
            }
            fusao = correlacionar_eventos(resultado, itc_data)
            reg.fusao_dados = fusao
            # Se for síncrono, atualizamos também a evidência visual para linkar
            ultima_ev.fusao_dados = fusao
            ultima_ev.save()

        reg.save()

        # Atualizar contadores da sessão
        if reg.sessao:
            sessao = reg.sessao
            sessao.total_capturas = sessao.registros.count()
            sessao.total_anomalias = sessao.registros.filter(e_anomalia=True).count()
            sessao.save()

        return resultado
    except RegistroEVP.DoesNotExist:
        return {}
