#!/usr/bin/env python
"""
Script para executar testes de CRUD real
Testa criação, atualização e deleção de registros reais
"""
import subprocess
import sys
import os

def run_real_crud_tests():
    """Executa testes de CRUD real"""
    
    print("=" * 70)
    print("🔄 EXECUTANDO TESTES DE CRUD REAL")
    print("=" * 70)
    
    description = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                    TESTES DE CRUD REAL                          ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║ Estes testes fazem o ciclo completo:                            ║
    ║                                                                  ║
    ║ 🟢 CREATE  - Criar registros reais                             ║
    ║ 🔵 READ    - Ler e verificar dados                             ║
    ║ 🟡 UPDATE  - Atualizar registros                               ║
    ║ 🔴 DELETE  - Deletar registros                                 ║
    ║ ✅ VERIFY  - Verificar que foram deletados                     ║
    ║                                                                  ║
    ║ Entidades testadas:                                              ║
    ║   • Produtores Rurais                                           ║
    ║   • Fazendas                                                    ║
    ║   • Safras                                                      ║
    ║   • Culturas                                                    ║
    ║   • Fluxo completo do sistema                                   ║
    ║                                                                  ║
    ║ ⚠️  Não usa fixtures pré-criadas                                ║
    ║ ✅  Cria dados reais durante os testes                         ║
    ║ 🧹  Limpa tudo após cada teste                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    
    print(description)
    
    # Comando pytest para rodar testes de CRUD real
    cmd = [
        "pytest",
        "tests/integration/test_real_crud_flow.py",
        "-v",  # Verbose
        "-s",  # Mostrar prints
        "--tb=short",  # Traceback curto
        "--color=yes"
    ]
    
    print("\n" + "=" * 70)
    print("Executando testes de CRUD real...")
    print("=" * 70 + "\n")
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        if result.returncode == 0:
            print("\n" + "=" * 70)
            print("✅ TODOS OS TESTES DE CRUD REAL PASSARAM!")
            print("=" * 70)
            print("\n🎉 Ciclos testados com sucesso:")
            print("   • Produtores: CREATE → READ → UPDATE → DELETE ✅")
            print("   • Fazendas: CREATE → UPDATE → DELETE ✅")
            print("   • Safras: CREATE → READ → DELETE ✅")
            print("   • Culturas: CREATE → READ → DELETE ✅")
            print("   • Sistema completo: Fluxo end-to-end ✅")
        else:
            print("\n" + "=" * 70)
            print("❌ ALGUNS TESTES DE CRUD FALHARAM")
            print("=" * 70)
            
        return result.returncode
        
    except FileNotFoundError:
        print("\n❌ ERRO: pytest não encontrado. Instale com: pip install pytest")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO ao executar testes: {e}")
        return 1

def run_specific_test(test_name):
    """Executa um teste específico"""
    
    test_mapping = {
        "producer": "TestRealProducerCRUD::test_complete_producer_lifecycle",
        "farm": "TestRealFarmCRUD::test_complete_farm_lifecycle", 
        "harvest": "TestRealHarvestCRUD::test_complete_harvest_lifecycle",
        "crop": "TestRealCropCRUD::test_complete_crop_lifecycle",
        "system": "TestCompleteSystemFlow::test_complete_system_lifecycle"
    }
    
    if test_name not in test_mapping:
        print(f"❌ Teste '{test_name}' não encontrado.")
        print(f"Testes disponíveis: {list(test_mapping.keys())}")
        return 1
    
    test_path = f"tests/integration/test_real_crud_flow.py::{test_mapping[test_name]}"
    
    cmd = [
        "pytest",
        test_path,
        "-v",
        "-s", 
        "--tb=short",
        "--color=yes"
    ]
    
    print(f"\n🎯 Executando teste específico: {test_name}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        return result.returncode
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return 1

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Executar testes de CRUD real")
    parser.add_argument(
        "--test",
        choices=["producer", "farm", "harvest", "crop", "system"],
        help="Executar teste específico"
    )
    
    args = parser.parse_args()
    
    if args.test:
        exit_code = run_specific_test(args.test)
    else:
        exit_code = run_real_crud_tests()
    
    sys.exit(exit_code)