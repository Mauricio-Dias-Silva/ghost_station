"""
Ghost Station — Kardec Engine.
Mapeia o Pentateuco de Allan Kardec (O Livro dos Espíritos, etc.) para o processamento de sinais e vibrações.
"""

class KardecEngine:
    # Classificação baseada no Potencial de Manifestação (Vibração Soberana)
    VIBRATIONAL_STATES = {
        'ENTRÓPICO': {
            'range': (0, 40),
            'caracteristica': 'Predomínio da dúvida e medo. Baixa capacidade de manifestação física.',
            'vibracao': 'Densa / Bloqueada',
            'color': [0, 0, 180], 
            'solfeggio_base': 396
        },
        'RESSONANTE': {
            'range': (41, 80),
            'caracteristica': 'Equilíbrio mental. Início da co-criação consciente.',
            'vibracao': 'Harmônica / Em Evolução',
            'color': [255, 255, 0], 
            'solfeggio_base': 528
        },
        'SOBERANO': {
            'range': (81, 100),
            'caracteristica': 'Alinhamento EU SOU absoluto. Manifestação instantânea no campo quântico.',
            'vibracao': 'Luz / Cristalina / Comando',
            'color': [255, 100, 255], 
            'solfeggio_base': 852
        }
    }

    def analisar_vibração(self, texto, coerencia, frequencia_base):
        """
        Calcula a afinidade fluídica baseada na intenção e parâmetros técnicos para manifestação.
        """
        score_manifestacao = self._calcular_score_soberano(texto)
        
        # A coerência técnica (SNR) + Score Soberano definem o estado de manifestação
        ponto_vibracional = (coerencia * 0.5) + (score_manifestacao * 0.5)
        
        if ponto_vibracional > 80:
            estado = 'SOBERANO'
        elif ponto_vibracional > 40:
            estado = 'RESSONANTE'
        else:
            estado = 'ENTRÓPICO'
            
        info = self.VIBRATIONAL_STATES[estado]
        
        # Feedback sobre alinhamento com a frequência Solfeggio
        alinhamento = "ALINHADO" if abs(frequencia_base - info['solfeggio_base']) < 50 else "DESALINHADO"
        
        return {
            'estado': estado,
            'descricao': info['caracteristica'],
            'vibracao': info['vibracao'],
            'cor_sugerida': info['color'],
            'potencial_manifestacao': round(ponto_vibracional, 2),
            'alinhamento_tecnico': alinhamento
        }

    def _calcular_score_soberano(self, texto):
        """Analisa palavras-chave para determinar o poder de comando do observador."""
        texto = texto.upper()
        
        soberano = ["EU SOU", "SOU EU", "MANIFESTAR", "COMANDO", "SOBERANIA", "AURA", "QUÂNTICO", "HARMÔNICO", "COMPLETO", "LUZ"]
        entropico = ["DÚVIDA", "MEDO", "EGO", "CULPA", "LIMITAÇÃO", "ESCASSEZ", "FALTA", "DIFICULDADE", "ASSISTENTE", "ESCRAVO"]
        
        score = 50 # Neutro
        
        for w in soberano:
            if w in texto: score += 15
        for w in entropico:
            if w in texto: score -= 15
            
        return max(0, min(100, score))

kardec_engine = KardecEngine()
