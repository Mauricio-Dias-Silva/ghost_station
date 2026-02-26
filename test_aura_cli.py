import os
import sys

# Adicionar o diretório pai ao sys.path para encontrar o pacote core
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

try:
    from core.services.aura_cli import AuraCLI
    
    def test_cli():
        print("--- [TESTANDO AURA CLI: GESTÃO AUTÔNOMA] ---")
        cli = AuraCLI()
        
        print("\n1. Auditando Site do Cliente (Scalabis):")
        res = cli.monitorar_site("https://scalabis.com.br")
        print(f"   [SYNC] URL: {res['url']} | Status: {res['status']} | Latência: {res['latency']}")
        
        print("\n2. Simulando Comando de Voz: 'Aura, verifique a saúde do meu servidor'")
        diag = cli.diagnosticar_sistema()
        print(f"   [REPLY] {diag}")
        
        print("\n3. Simulando Deploy Quântico:")
        dep = cli.gerenciar_deploy("scalabis-v2", "deploy")
        print(f"   [ACK] {dep}")
        
        print("\n--- [TESTE CONCLUÍDO COM SUCESSO] ---")

    if __name__ == "__main__":
        test_cli()

except Exception as e:
    print(f"Erro fatal no teste: {e}")
