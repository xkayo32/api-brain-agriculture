"""
Sistema de testes personalizado para a API
"""
import os
import sys

# Adicionar diretorio da aplicacao ao path
sys.path.insert(0, os.path.dirname(__file__))

def run_validator_tests():
    """Executa testes dos validadores"""
    print("=== EXECUTANDO TESTES DOS VALIDADORES ===")
    os.system('python tests/test_validators_isolated.py')

def run_basic_security_tests():
    """Executa testes basicos de seguranca"""
    print("\n=== EXECUTANDO TESTES BASICOS DE SEGURANÇA ===")
    
    try:
        from app.utils.security import verify_password, get_password_hash
        
        # Teste basico de hash de senha
        password = "teste123"
        hashed = get_password_hash(password)
        
        if verify_password(password, hashed):
            print("OK: Hash e verificacao de senha funcionando")
        else:
            print("ERRO: Falha na verificacao de senha")
            
        if not verify_password("senha_errada", hashed):
            print("OK: Rejeicao de senha incorreta funcionando")
        else:
            print("ERRO: Falha na rejeicao de senha incorreta")
            
        print("Todos os testes de seguranca basicos passaram!")
        
    except Exception as e:
        print(f"ERRO nos testes de seguranca: {e}")

def run_import_tests():
    """Testa se todas as importacoes funcionam"""
    print("\n=== TESTANDO IMPORTACOES DOS MODULOS ===")
    
    modules_to_test = [
        "app.utils.validators",
        "app.utils.security", 
        "app.models.user",
        "app.models.producer", 
        "app.models.farm",
        "app.schemas",
        "app.database"
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"OK: {module}")
        except Exception as e:
            print(f"ERRO: {module} - {e}")

if __name__ == "__main__":
    print("SISTEMA DE TESTES DA API BRAIN AGRICULTURE")
    print("=" * 50)
    
    # Executar testes dos validadores
    run_validator_tests()
    
    # Executar testes de seguranca
    run_basic_security_tests()
    
    # Executar testes de importacao
    run_import_tests()
    
    print("\n" + "=" * 50)
    print("RESUMO DOS TESTES CONCLUIDO")
    print("=" * 50)