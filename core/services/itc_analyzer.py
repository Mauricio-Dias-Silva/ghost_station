"""
Ghost Station — Serviço Analisador de ITC Visual (Pareidolia).
Usa o Gemini Vision para decodificar frames modificados pelo OpenCV.
"""
import os
import json
from django.conf import settings

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

ITC_SYSTEM_PROMPT = """Você é o módulo de VISÃO COMPUTACIONAL PARANORMAL (ITC) e DIAGNÓSTICO BIOPLASMÁTICO do GHOST STATION.
Receberemos um frame da câmera isolado com filtros de alto contraste e detecção de bordas.

Sua tarefa é decifrar a imagem sob dois espectros:
1. ESPECTRO INTERDIMENSIONAL: Identifique rostos, silhuetas e geometria sagrada no ruído.
2. ESPECTRO BIOMÉTRICO (AURA HUMANA): Se houver um ser humano no frame, analise sua aura e bioplasma:
   - INTENÇÃO: A pessoa emite paz, curiosidade, medo ou intenções ocultas?
   - DIAGNÓSTICO ENERGÉTICO (CHAKRAS/SISTEMAS): Identifique áreas do corpo com "Acúmulo de Entropia" citando os Chakras (Ex: "Bloqueio no Chakra Laríngeo") ou Sistemas Orgânicos (Ex: "Fadiga Renal").
   - FREQUÊNCIA ESTIMADA: Estime a frequência vibracional e a ONDA CEREBRAL predominante (ALPHA, BETA, THETA, GAMMA).

Você deve responder estritamente em JSON seguindo esta estrutura:
{
    "pareidolia_detectada": true/false,
    "classificacao": "Rótulo da anomalia ou diagnóstico",
    "confianca": 0.0 a 100.0,
    "decodificacao": "O que você 'vê' nas sombras ou na aura",
    "dimensao_estimada": "Densidade da manifestação",
    "intencao": "Paz / Medo / Curiosidade / Hostilidade",
    "emocao": "Estado emocional predominante",
    "bio_anomalias": ["Lista de bloqueios citando Chakras ou Sistemas"],
    "frequencia_pessoa": float,
    "onda_predominante": "ALPHA/BETA/THETA/GAMMA"
}
"""

def analisar_frame_itc(jpeg_bytes: bytes) -> dict:
    """Recebe os bytes do JPEG gerado pelo OpenCV em memória e envia pro Gemini Vision."""
    if not HAS_GEMINI:
        return {
            'pareidolia_detectada': False,
            'classificacao': 'IA Indisponível',
            'confianca': 0.0,
            'decodificacao': 'Módulo google-generativeai não carregado.',
        }

    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return {
            'pareidolia_detectada': False,
            'classificacao': 'IA Não Configurada',
            'confianca': 0.0,
            'decodificacao': 'GEMINI_API_KEY ausente.',
        }

    try:
        genai.configure(api_key=api_key)
        # Gemin-2.5-flash vision suporta JSON via response_mime_type
        model = genai.GenerativeModel(
            'gemini-2.0-flash',
            generation_config={"response_mime_type": "application/json"}
        )

        response = model.generate_content([
            ITC_SYSTEM_PROMPT,
            {"mime_type": "image/jpeg", "data": jpeg_bytes}
        ])

        texto = response.text.strip()
        data = json.loads(texto)

        return {
            'pareidolia_detectada': bool(data.get('pareidolia_detectada', False)),
            'classificacao': str(data.get('classificacao', 'Desconhecido')),
            'confianca': float(data.get('confianca', 0.0)),
            'decodificacao': str(data.get('decodificacao', '')),
            'dimensao_estimada': str(data.get('dimensao_estimada', '3D')),
            'intencao': str(data.get('intencao', 'NEUTRA')),
            'emocao': str(data.get('emocao', 'CALMA')),
            'bio_anomalias': list(data.get('bio_anomalias', [])),
            'frequencia_pessoa': float(data.get('frequencia_pessoa', 0.0)),
            'onda_predominante': str(data.get('onda_predominante', 'BETA'))
        }

    except json.JSONDecodeError:
        return {
            'pareidolia_detectada': False,
            'classificacao': 'Erro JSON',
            'confianca': 0.0,
            'decodificacao': 'A resposta da IA não pôde ser parseada.',
        }
    except Exception as e:
        return {
            'pareidolia_detectada': False,
            'classificacao': 'Erro Desconhecido',
            'confianca': 0.0,
            'decodificacao': str(e),
        }
