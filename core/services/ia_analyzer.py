"""
Ghost Station — Serviço de Análise IA (Gemini Vision).
Analisa imagens de evidências e classifica anomalias.
"""
import os
from django.conf import settings

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False


import json

SYSTEM_PROMPT = """Você é o módulo de análise do GHOST STATION, um sistema de investigação paranormal.
Sua tarefa é ANALISAR A IMAGEM e responder SOMENTE EM JSON formatado exatamente como a estrutura abaixo.

ESTRUTURA JSON EXIGIDA:
{
    "classificacao": "string curta (Ex: Pareidolia, Reflexo, Anomalia Inexplicada, Pessoa Real, Nada Detectado)",
    "confianca": float (0.0 até 100.0),
    "analise": "string descritiva detalhada (Possíveis explicações racionais vs paranormais)",
    "nota_paranormal": int (0 até 10)
}

Regras:
- Responda em português.
- NUNCA retorne blocos de código markdown como ```json
- Retorne apenas o objeto JSON válido.
- Seja científico, investigativo, mas mantenha a mente aberta."""

def analisar_evidencia(imagem_path: str) -> dict:
    """Analisa uma imagem de evidência usando Gemini Vision e força saída JSON."""
    if not HAS_GEMINI:
        return {
            'classificacao': 'IA Indisponível',
            'confianca': 0,
            'analise': 'Módulo google-generativeai não instalado.',
            'nota_paranormal': 0,
        }

    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return {
            'classificacao': 'IA Não Configurada',
            'confianca': 0,
            'analise': 'GEMINI_API_KEY não definida nas configurações.',
            'nota_paranormal': 0,
        }

    try:
        genai.configure(api_key=api_key)
        # Using response_mime_type to force JSON on gemini-2.0-flash
        model = genai.GenerativeModel(
            'gemini-2.0-flash',
            generation_config={"response_mime_type": "application/json"}
        )

        full_path = os.path.join(settings.BASE_DIR, imagem_path.lstrip('/'))
        if not os.path.exists(full_path):
            return {
                'classificacao': 'Erro',
                'confianca': 0,
                'analise': f'Arquivo não encontrado: {full_path}',
                'nota_paranormal': 0,
            }

        with open(full_path, 'rb') as f:
            image_data = f.read()

        response = model.generate_content([
            SYSTEM_PROMPT,
            {"mime_type": "image/jpeg", "data": image_data}
        ])

        texto = response.text.strip()
        
        # Fallback to remove ```json if the model still includes it 
        if texto.startswith("```json"):
            texto = texto.replace("```json", "", 1).replace("```", "")
        
        data = json.loads(texto)

        return {
            'classificacao': str(data.get('classificacao', 'Desconhecido'))[:30],
            'confianca': float(data.get('confianca', 0)),
            'analise': str(data.get('analise', 'Nenhuma análise detalhada retornada.')),
            'nota_paranormal': int(data.get('nota_paranormal', 0)),
        }

    except json.JSONDecodeError as e:
        return {
            'classificacao': 'Falha de Parse',
            'confianca': 0,
            'analise': f'O modelo não retornou um JSON válido. Raw: {response.text}',
            'nota_paranormal': 0,
        }
    except Exception as e:
        return {
            'classificacao': 'Erro na Análise',
            'confianca': 0,
            'analise': f'Erro ao processar a requisição: {str(e)}',
            'nota_paranormal': 0,
        }


def analisar_evidencia_async(evidencia_id: int):
    """Analisa e salva o resultado no banco (para uso em background)."""
    from .models import Evidencia
    try:
        ev = Evidencia.objects.get(id=evidencia_id)
        resultado = analisar_evidencia(ev.imagem_url)
        ev.analise_ia = resultado['analise']
        ev.ia_classificacao = resultado['classificacao']
        ev.ia_confianca = resultado['confianca']
        ev.save()
        return resultado
    except Evidencia.DoesNotExist:
        return None
