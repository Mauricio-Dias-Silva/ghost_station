"""
Ghost Station — Kardec Engine.
Mapeia o Pentateuco de Allan Kardec (O Livro dos Espíritos, etc.) para o processamento de sinais e vibrações.
"""

class KardecEngine:
    # Classificação baseada na Escala Espírita (Livro dos Espíritos, Questão 100)
    ORDERS = {
        'IMPERFEITOS': {
            'range': (0, 40),
            'caracteristica': 'Predomínio da matéria sobre o espírito. Proclividade ao mal, ignorância.',
            'vibracao': 'Densa / Baixa Frequência',
            'color': [0, 0, 180], # Azul Escuro / Amber conforme o humor
            'solfeggio_base': 396
        },
        'BONS': {
            'range': (41, 80),
            'caracteristica': 'Predomínio do espírito sobre a matéria. Desejo do bem. Sabedoria e bondade.',
            'vibracao': 'Harmônica / Média Frequência',
            'color': [255, 255, 0], # Ciano
            'solfeggio_base': 528
        },
        'PUROS': {
            'range': (81, 100),
            'caracteristica': 'Nenhuma influência da matéria. Superioridade intelectual e moral absoluta.',
            'vibracao': 'Luz / Alta Frequência / Fractal',
            'color': [255, 100, 255], # Magenta/Branco
            'solfeggio_base': 852
        }
    }

    def analisar_vibração(self, texto, coerencia, frequencia_base):
        """
        Calcula a afinidade fluídica baseada no léxico moral e parâmetros técnicos.
        """
        score_moral = self._calcular_score_moral(texto)
        
        # A coerência técnica (SNR) + Score Moral definem a Classe do Espírito
        ponto_vibracional = (coerencia * 0.6) + (score_moral * 0.4)
        
        if ponto_vibracional > 80:
            classe = 'PUROS'
        elif ponto_vibracional > 40:
            classe = 'BONS'
        else:
            classe = 'IMPERFEITOS'
            
        info = self.ORDERS[classe]
        
        # Feedback sobre alinhamento
        alinhamento = "ALINHADO" if abs(frequencia_base - info['solfeggio_base']) < 50 else "DESALINHADO"
        
        return {
            'classe': classe,
            'descricao': info['caracteristica'],
            'vibracao': info['vibracao'],
            'cor_sugerida': info['color'],
            'afinidade': round(ponto_vibracional, 2),
            'alinhamento_tecnico': alinhamento
        }

    def _calcular_score_moral(self, texto):
        """Analisa palavras-chave do Pentateuco para determinar a elevação do sinal."""
        texto = texto.upper()
        
        elevado = ["CARIDADE", "DEUS", "LUZ", "PROGRESSO", "PERDÃO", "BONDADE", "EVOLUÇÃO", "AMOR", "PAZ", "HARMÔNICO"]
        baixo = ["MEDO", "ÓDIO", "VINGANÇA", "MATÉRIA", "DOR", "TREVAS", "MORTAL", "PRISÃO", "EGO", "MAL"]
        
        score = 50 # Neutro
        
        for w in elevado:
            if w in texto: score += 15
        for w in baixo:
            if w in texto: score -= 15
            
        return max(0, min(100, score))

kardec_engine = KardecEngine()
