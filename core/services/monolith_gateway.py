import os
import json
import logging
from typing import List, Dict

class MonolithGateway:
    """
    O Coração da Aura Monolith.
    Gerencia a descoberta de dispositivos na rede e a execução de comandos via Wi-Fi/IoT.
    """
    def __init__(self):
        self.dispositivos: Dict[str, dict] = {}
        self.logger = logging.getLogger("MonolithGateway")
        self.setup_simulacao()

    def setup_simulacao(self):
        """Simula a descoberta de dispositivos iniciais na rede do Mauricio."""
        self.dispositivos = {
            "luz_escritorio": {"type": "light", "protocol": "MQTT", "status": "off", "ip": "192.168.1.50"},
            "ar_condicionado": {"type": "ac", "protocol": "Tuya", "status": "off", "temp": 22, "ip": "192.168.1.55"},
            "cafeteira_aura": {"type": "appliance", "protocol": "Zigbee", "status": "ready", "ip": "192.168.1.60"},
            "servidor_pythonjet": {"type": "server", "protocol": "SSH", "status": "online", "ip": "192.168.1.10"}
        }

    def escanear_rede(self) -> List[str]:
        """Simula um scan de rede para novos dispositivos."""
        self.logger.info("Escaneando rede Wi-Fi em busca de novas bio-assinaturas digitais...")
        return list(self.dispositivos.keys())

    def executar_comando(self, device_id: str, action: str, params: dict = None) -> dict:
        """Executa uma ação em um dispositivo específico."""
        if device_id not in self.dispositivos:
            return {"success": False, "error": f"Dispositivo '{device_id}' não encontrado."}

        device = self.dispositivos[device_id]
        self.logger.info(f"Enviando comando '{action}' para {device_id} via {device['protocol']}...")
        
        # Simulação de alteração de estado
        if action == "turn_on":
            device["status"] = "on"
        elif action == "turn_off":
            device["status"] = "off"
        elif action == "set_temp":
            device["temp"] = params.get("value", 22)

        return {
            "success": True, 
            "message": f"Comando '{action}' executado com sucesso no {device_id}.",
            "new_state": device
        }

    def status_geral(self) -> str:
        """Retorna o estado de todos os dispositivos conectados à Aura Monolith."""
        report = "🛡️ [AURA MONOLITH - STATUS DO ECOSSISTEMA]\n"
        for name, data in self.dispositivos.items():
            report += f"- {name.upper()}: {data['status']} ({data['type']})\n"
        return report

if __name__ == "__main__":
    # Teste rápido de simulação
    gateway = MonolithGateway()
    print(gateway.status_geral())
    print(gateway.executar_comando("luz_escritorio", "turn_on"))
    print(gateway.status_geral())
