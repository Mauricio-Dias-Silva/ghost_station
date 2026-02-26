import os
import glob
from django.conf import settings

class GenomeService:
    """
    Serviço que indexa padrões de código e arquitetura de todos os workspaces do usuário.
    Garante que a Aura tenha consciência global do ecossistema de desenvolvimento.
    """
    
    WORKSPACES = [
        r"c:\Users\Mauricio\Desktop\Observatorio-saude",
        r"c:\Users\Mauricio\Desktop\Projeto-Integrador-3",
        r"c:\Users\Mauricio\Desktop\codex-IA",
        r"c:\Users\Mauricio\Desktop\compra-coletiva",
        r"c:\Users\Mauricio\Desktop\corpo_humano_holistico",
        r"c:\Users\Mauricio\Desktop\crmsolar",
        r"c:\Users\Mauricio\Desktop\edufuturo",
        r"c:\Users\Mauricio\Desktop\energia livre",
        r"c:\Users\Mauricio\Desktop\ghost_station",
        r"c:\Users\Mauricio\Desktop\neuroacesso",
        r"c:\Users\Mauricio\Desktop\novo programa de fotos",
        r"c:\Users\Mauricio\Desktop\painel-pythonjet",
        r"c:\Users\Mauricio\Desktop\portfolio-mauricio",
        r"c:\Users\Mauricio\Desktop\projeto_integrador_I-Univesp",
        r"c:\Users\Mauricio\Desktop\sysgov-project"
    ]

    def coletar_dna_arquitetura(self):
        """Coleta padrões de bibliotecas e configurações comuns."""
        dna_deps = set()
        dna_dbs = set()
        dna_patterns = []
        
        for path in self.WORKSPACES:
            if not os.path.exists(path):
                continue
                
            # Verificar requirements.txt
            req_path = os.path.join(path, "requirements.txt")
            if os.path.exists(req_path):
                try:
                    with open(req_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            clean_line = line.strip()
                            if clean_line and not clean_line.startswith('#'):
                                dna_deps.add(clean_line.split('==')[0].split('>=')[0].strip())
                except:
                    pass
            
            # Verificar settings.py (padrões de DB)
            try:
                settings_files = glob.glob(os.path.join(path, "**/settings.py"), recursive=True)
                for s_file in settings_files:
                    with open(s_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if 'postgresql' in content.lower():
                            dna_dbs.add("PostgreSQL")
                        if 'sqlite3' in content.lower():
                            dna_dbs.add("SQLite3")
                        if 'whitenoise' in content:
                            dna_patterns.append("WhiteNoise Static Files")
            except:
                pass
        
        return {
            "dependencies": list(dna_deps),
            "databases": list(dna_dbs),
            "patterns": list(set(dna_patterns))
        }

    def gerar_contexto_para_aura(self):
        """Transforma o DNA coletado em uma string de contexto para o prompt da Aura."""
        dna = self.coletar_dna_arquitetura()
        contexto = "HISTÓRICO ARQUITETURAL DO USUÁRIO:\n"
        contexto += f"- Tecnologias Frequentes: {', '.join(dna['dependencies'][:15])}...\n"
        contexto += f"- Bancos de Dados Preferenciais: {', '.join(dna['databases'])}\n"
        contexto += f"- Padrões Identificados: {', '.join(dna['patterns'])}\n"
        contexto += "Siga sempre esses padrões para garantir compatibilidade com o ecossistema existente."
        return contexto

genome_service = GenomeService()
