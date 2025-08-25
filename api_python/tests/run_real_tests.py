#!/usr/bin/env python
"""
Script para rodar testes de integração com dados reais
Requer que o banco PostgreSQL esteja rodando com dados populados
"""
import subprocess
import sys
import os

def run_real_data_tests():
    """Executa testes com dados reais"""
    
    print("=" * 60)
    print("EXECUTANDO TESTES COM DADOS REAIS DO POSTGRESQL")
    print("=" * 60)
    print("\nRequisitos:")
    print("- PostgreSQL rodando na porta 5433")
    print("- Banco populado com seed_data.py")
    print("- API rodando na porta 8001")
    print("-" * 60)
    
    # Configurar ambiente
    os.environ["DATABASE_URL"] = "postgresql://ruraluser:ruralpass@localhost:5433/rural_producers_db"
    
    # Comando pytest para rodar apenas testes com dados reais
    cmd = [
        "pytest",
        "tests/integration/test_real_data_integration.py",
        "-v",  # Verbose
        "-s",  # Mostrar prints
        "-m", "real_data",  # Apenas testes marcados como real_data
        "--tb=short",  # Traceback curto
        "--color=yes"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode
    except FileNotFoundError:
        print("\nERRO: pytest não encontrado. Instale com: pip install pytest")
        return 1
    except Exception as e:
        print(f"\nERRO ao executar testes: {e}")
        return 1

def run_all_integration_tests():
    """Executa todos os testes de integração (mock + real)"""
    
    print("\n" + "=" * 60)
    print("EXECUTANDO TODOS OS TESTES DE INTEGRAÇÃO")
    print("=" * 60)
    
    cmd = [
        "pytest",
        "tests/integration/",
        "-v",
        "--tb=short",
        "--color=yes",
        "--cov=app",  # Cobertura de código
        "--cov-report=term-missing"  # Mostrar linhas não cobertas
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode
    except Exception as e:
        print(f"\nERRO ao executar testes: {e}")
        return 1

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Executar testes de integração")
    parser.add_argument(
        "--real-only",
        action="store_true",
        help="Executar apenas testes com dados reais"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Executar todos os testes de integração"
    )
    
    args = parser.parse_args()
    
    if args.real_only:
        exit_code = run_real_data_tests()
    elif args.all:
        exit_code = run_all_integration_tests()
    else:
        # Por padrão, executa testes com dados reais
        exit_code = run_real_data_tests()
    
    sys.exit(exit_code)