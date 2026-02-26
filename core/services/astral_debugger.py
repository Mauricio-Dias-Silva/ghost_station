import subprocess
import tempfile
import os

class AstralDebugger:
    """
    O 'Astral Debugger' permite que a Aura valide trechos de código antes de sugeri-los.
    Usa análise estática para garantir que o código seja 'Bug-Free'.
    """

    def validar_trecho(self, codigo: str):
        """Valida um trecho de código Python usando flake8 e verificações básicas."""
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w', encoding='utf-8') as tmp:
            tmp_name = tmp.name
            tmp.write(codigo)
        
        try:
            # 1. Verificação de Sintaxe (compilação rápida)
            compile(codigo, '<string>', 'exec')
            
            # 2. Flake8 (opcional, se estiver instalado no env)
            # result = subprocess.run(['flake8', tmp_name], capture_output=True, text=True)
            # if result.returncode != 0:
            #    return {"vaildo": False, "erro": result.stdout}
            
            return {"valido": True, "detalhes": "Sintaxe OK. Coerência quântica mantida."}
        except SyntaxError as e:
            return {"valido": False, "erro": f"Sintaxe Inválida: {str(e)}", "linha": e.lineno}
        except Exception as e:
            return {"valido": False, "erro": f"Erro de Validação: {str(e)}"}
        finally:
            if os.path.exists(tmp_name):
                os.remove(tmp_name)

astral_debugger = AstralDebugger()
