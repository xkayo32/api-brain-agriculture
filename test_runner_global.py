"""
Sistema de testes global para ambas as APIs (Python e Scala)
"""
import os
import sys
import subprocess

def run_python_tests():
    """Executa testes da API Python"""
    print("=" * 60)
    print("EXECUTANDO TESTES DA API PYTHON")
    print("=" * 60)
    
    python_dir = "api_python"
    if os.path.exists(python_dir):
        os.chdir(python_dir)
        
        try:
            # Executar sistema de testes Python
            result = subprocess.run([sys.executable, "test_runner.py"], 
                                  capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            os.chdir("..")
            return result.returncode == 0
        except Exception as e:
            print(f"ERRO ao executar testes Python: {e}")
            os.chdir("..")
            return False
    else:
        print("Diretorio api_python nao encontrado")
        return False

def run_scala_tests():
    """Executa testes da API Scala"""
    print("\n" + "=" * 60)
    print("EXECUTANDO TESTES DA API SCALA")
    print("=" * 60)
    
    scala_dir = "api_scala"
    if os.path.exists(scala_dir):
        print("Diretorio Scala encontrado")
        print("NOTA: Para executar testes Scala, use:")
        print("  cd api_scala")
        print("  make test-custom")
        print("  # ou")
        print("  sbt 'runMain TestRunner'")
        print("\nEstrutura de testes Scala criada com:")
        print("- DocumentValidatorSpec: Validadores CPF/CNPJ")
        print("- AuthServiceSpec: Autenticacao JWT") 
        print("- ProducerSpec: Modelo de Produtor")
        print("- FarmSpec: Modelo de Fazenda")
        print("- TestRunner: Sistema customizado")
        return True
    else:
        print("Diretorio api_scala nao encontrado")
        return False

def check_project_structure():
    """Verifica estrutura do projeto"""
    print("=" * 60)
    print("VERIFICANDO ESTRUTURA DO PROJETO")
    print("=" * 60)
    
    expected_dirs = [
        "api_python",
        "api_scala"
    ]
    
    python_test_files = [
        "api_python/test_runner.py",
        "api_python/tests/test_validators_isolated.py",
        "api_python/tests/conftest.py",
        "api_python/pytest.ini",
        "api_python/TESTS.md"
    ]
    
    scala_test_files = [
        "api_scala/src/test/scala/TestRunner.scala",
        "api_scala/src/test/scala/utils/DocumentValidatorSpec.scala",
        "api_scala/src/test/scala/services/AuthServiceSpec.scala",
        "api_scala/src/test/scala/models/ProducerSpec.scala",
        "api_scala/src/test/scala/models/FarmSpec.scala",
        "api_scala/Makefile",
        "api_scala/TESTS.md"
    ]
    
    print("Verificando diretórios principais:")
    for dir_name in expected_dirs:
        if os.path.exists(dir_name):
            print(f"OK {dir_name}")
        else:
            print(f"X  {dir_name}")
    
    print("\nVerificando arquivos de teste Python:")
    for file_path in python_test_files:
        if os.path.exists(file_path):
            print(f"OK {file_path}")
        else:
            print(f"X  {file_path}")
    
    print("\nVerificando arquivos de teste Scala:")
    for file_path in scala_test_files:
        if os.path.exists(file_path):
            print(f"OK {file_path}")
        else:
            print(f"X  {file_path}")

def main():
    """Funcao principal"""
    print("SISTEMA DE TESTES - BRAIN AGRICULTURE")
    print("APIs Python e Scala")
    print("Desenvolvido por: Kayo Carvalho Fernandes")
    
    # Verificar estrutura
    check_project_structure()
    
    # Executar testes Python
    python_success = run_python_tests()
    
    # Informações sobre testes Scala
    scala_info = run_scala_tests()
    
    print("\n" + "=" * 60)
    print("RESUMO FINAL")
    print("=" * 60)
    
    if python_success:
        print("OK Testes Python: SUCESSO")
    else:
        print("X  Testes Python: FALHA")
    
    if scala_info:
        print("OK Estrutura Scala: CONFIGURADA")
    else:
        print("X  Estrutura Scala: PROBLEMA")
    
    print("\nPara executar testes Scala:")
    print("  cd api_scala && make test-custom")
    
    print("\nPara executar testes Python:")
    print("  cd api_python && python test_runner.py")
    
    print("\nDocumentacao:")
    print("  api_python/TESTS.md")
    print("  api_scala/TESTS.md")

if __name__ == "__main__":
    main()