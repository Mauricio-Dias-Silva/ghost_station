import requests
import time
from .aura_state import aura_state

class SiteSentinel:
    """
    Módulo de monitoramento de sites externos.
    Aura usa este "sentido" para detectar quando projetos na nuvem estão com problemas.
    """
    
    SITES_TO_MONITOR = [
        {"name": "Scalabis", "url": "https://scalabis.com.br"}, # Exemplo, ajustar se souber o real
        {"name": "PythonJet Painel", "url": "https://painel.pythonjet.app"},
        {"name": "Ghost Station Cloud", "url": "https://ghost-station.pythonjet.app"}
    ]

    def verificar_sites(self):
        """Verifica o status de todos os sites e reporta à Aura."""
        relatorio = []
        for site in self.SITES_TO_MONITOR:
            try:
                start = time.time()
                response = requests.get(site['url'], timeout=10)
                latency = (time.time() - start) * 1000
                
                if response.status_code == 200:
                    status = "ONLINE"
                else:
                    status = f"ERRO {response.status_code}"
                    aura_state.adicionar_mensagem("AURA", f"ALERTA: O site {site['name']} está apresentando instabilidade ({status}).")
                
                relatorio.append({
                    "nome": site['name'],
                    "status": status,
                    "latencia": f"{latency:.2f}ms"
                })
            except Exception as e:
                aura_state.adicionar_mensagem("AURA", f"CRÍTICO: Não consigo alcançar o site {site['name']}. Possível queda de servidor.")
                relatorio.append({
                    "nome": site['name'],
                    "status": "OFFLINE",
                    "erro": str(e)
                })
        
        return relatorio

site_sentinel = SiteSentinel()
