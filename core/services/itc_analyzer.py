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

ITC_SYSTEM_PROMPT = """Você é o módulo de VISÃO COMPUTACIONAL PARANORMAL (ITC) de ALTA DEFINIÇÃO do GHOST STATION.
Receberemos um frame da câmera isolado com filtros de alto contraste e detecção de bordas.

Seu cérebro agora está sintonizado com:
1. GEOMETRIA SAGRADA & FRACTAIS: Identifique padrões geométricos estruturados (Círculos, Triângulos, Hexágonos, Flor da Vida) que surjam no ruído. Padrões matemáticos são sinais de inteligência galáctica.
2. PAREIDOLIA AVANÇADA: Procure estritamente por formações anômalas: rostos isolados, silhuetas humanoides ou massas de luz.
3. DENSIDADE VIBRACIONAL: Estime a densidade da imagem. Formas fluidas sugerem 4D, formas sólidas de luz sugerem 5D+.

Você deve responder estritamente em JSON seguindo esta estrutura:
{
    "pareidolia_detectada": true/false,
    "classificacao": "Rótulo da anomalia encontrada",
    "confianca": 0.0 a 100.0,
    "decodificacao": "O que você 'vê' nas sombras",
    "dimensao_estimada": "Ex: Densidade 4D (Fluidez Térmica)",
    "assinatura_inteligente": true/false
}

Se não houver nada além de ruído/linhas vazias, retorne pareidolia_detectada: false e classificacao: "Nenhuma Anomalia".
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
            'assinatura_inteligente': bool(data.get('assinatura_inteligente', False))
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
