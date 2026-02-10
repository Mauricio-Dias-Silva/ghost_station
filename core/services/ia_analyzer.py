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


SYSTEM_PROMPT = """Você é o módulo de análise do GHOST STATION, um sistema de investigação paranormal.
Você recebe imagens capturadas por câmeras durante investigações.

Sua tarefa é ANALISAR A IMAGEM e responder em formato estruturado:

1. CLASSIFICAÇÃO: O que você vê? (Pareidolia, Reflexo, Sombra, Artefato Digital, Anomalia Inexplicada, Pessoa Real, Animal, Nada Detectado)
2. CONFIANÇA: Qual a sua confiança na classificação? (0-100%)
3. DESCRIÇÃO: Descreva objetivamente o que aparece na imagem
4. ANÁLISE TÉCNICA: Possíveis explicações racionais (luz, reflexo, ruído digital, etc.)
5. NOTA_PARANORMAL: De 0 a 10, quão inexplicável é essa imagem? (0 = totalmente explicável, 10 = completamente anômalo)

Responda em português. Seja científico mas aberto a possibilidades.
Use tom profissional de investigação forense."""


def analisar_evidencia(imagem_path: str) -> dict:
    """Analisa uma imagem de evidência usando Gemini Vision."""
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
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Carregar imagem
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
            {"mime_type": "image/jpeg", "data": image_data},
            "Analise esta imagem capturada durante uma investigação paranormal."
        ])

        texto = response.text

        # Parse básico
        confianca = 50.0
        classificacao = 'Analisado'
        nota = 5

        for line in texto.split('\n'):
            line_lower = line.lower().strip()
            if 'confiança' in line_lower or 'confianca' in line_lower:
                import re
                nums = re.findall(r'(\d+)', line)
                if nums:
                    confianca = float(nums[0])
            if 'classificação' in line_lower or 'classificacao' in line_lower:
                classificacao = line.split(':', 1)[-1].strip() if ':' in line else classificacao
            if 'nota_paranormal' in line_lower or 'nota paranormal' in line_lower:
                import re
                nums = re.findall(r'(\d+)', line)
                if nums:
                    nota = int(nums[0])

        return {
            'classificacao': classificacao[:30],
            'confianca': confianca,
            'analise': texto,
            'nota_paranormal': nota,
        }

    except Exception as e:
        return {
            'classificacao': 'Erro na Análise',
            'confianca': 0,
            'analise': f'Erro ao processar: {str(e)}',
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
