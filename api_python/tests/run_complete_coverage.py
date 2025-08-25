#!/usr/bin/env python
"""
Script para executar testes com cobertura completa de TODAS as rotas
"""
import subprocess
import sys
import os

def run_complete_coverage():
    """Executa testes de cobertura completa"""
    
    print("=" * 70)
    print("EXECUTANDO TESTES DE COBERTURA COMPLETA DE TODAS AS ROTAS")
    print("=" * 70)
    
    # Listar todas as rotas que serão testadas
    routes_summary = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                    ROTAS TESTADAS                               ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║ AUTENTICAÇÃO (4 rotas)                                          ║
    ║   • POST /api/auth/register                                     ║
    ║   • POST /api/auth/login                                        ║
    ║   • GET  /api/auth/me                                          ║
    ║   • GET  /api/auth/users                                       ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║ PRODUTORES (5 rotas)                                           ║
    ║   • GET    /api/producers/                                     ║
    ║   • GET    /api/producers/{id}                                 ║
    ║   • POST   /api/producers/                                     ║
    ║   • PUT    /api/producers/{id}                                 ║
    ║   • DELETE /api/producers/{id}                                 ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║ FAZENDAS (5 rotas)                                             ║
    ║   • GET    /api/farms/                                         ║
    ║   • GET    /api/farms/{id}                                     ║
    ║   • POST   /api/farms/                                         ║
    ║   • PUT    /api/farms/{id}                                     ║
    ║   • DELETE /api/farms/{id}                                     ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║ SAFRAS (5 rotas)                                               ║
    ║   • GET    /api/harvests/                                      ║
    ║   • GET    /api/harvests/{id}                                  ║
    ║   • POST   /api/harvests/                                      ║
    ║   • DELETE /api/harvests/{id}                                  ║
    ║   • GET    /api/harvests/farm/{farm_id}                        ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║ CULTURAS (6 rotas)                                             ║
    ║   • GET    /api/crops/                                         ║
    ║   • GET    /api/crops/{id}                                     ║
    ║   • POST   /api/crops/                                         ║
    ║   • DELETE /api/crops/{id}                                     ║
    ║   • GET    /api/crops/harvest/{harvest_id}                     ║
    ║   • GET    /api/crops/type/{crop_type}                         ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║ DASHBOARD (4 rotas)                                            ║
    ║   • GET /api/dashboard/summary                                 ║
    ║   • GET /api/dashboard/by-state                                ║
    ║   • GET /api/dashboard/by-crop                                 ║
    ║   • GET /api/dashboard/land-use                                ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║ UTILITÁRIAS (4 rotas)                                          ║
    ║   • GET /health                                                ║
    ║   • GET /                                                      ║
    ║   • GET /docs                                                  ║
    ║   • GET /openapi.json                                          ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║ TOTAL: 33 ROTAS COM COBERTURA COMPLETA                         ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    
    print(routes_summary)
    
    # Comando pytest para rodar testes completos
    cmd = [
        "pytest",
        "tests/integration/test_all_routes_complete.py",
        "-v",  # Verbose
        "-s",  # Mostrar prints
        "--tb=short",  # Traceback curto
        "--color=yes",
        "--cov=app",  # Cobertura
        "--cov-report=term-missing",  # Mostrar linhas não cobertas
        "--cov-report=html",  # Gerar relatório HTML
        "--cov-report=json"  # Gerar relatório JSON
    ]
    
    print("\n" + "=" * 70)
    print("Executando testes...")
    print("=" * 70 + "\n")
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        if result.returncode == 0:
            print("\n" + "=" * 70)
            print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
            print("=" * 70)
            print("\n📊 Relatórios de cobertura gerados:")
            print("   • Terminal: Veja acima")
            print("   • HTML: htmlcov/index.html")
            print("   • JSON: coverage.json")
        else:
            print("\n" + "=" * 70)
            print("❌ ALGUNS TESTES FALHARAM")
            print("=" * 70)
            
        return result.returncode
        
    except FileNotFoundError:
        print("\n❌ ERRO: pytest não encontrado. Instale com: pip install pytest pytest-cov")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO ao executar testes: {e}")
        return 1

def generate_coverage_report():
    """Gera relatório detalhado de cobertura"""
    print("\n" + "=" * 70)
    print("Gerando relatório detalhado de cobertura...")
    print("=" * 70)
    
    try:
        # Gerar relatório de cobertura detalhado
        subprocess.run(["coverage", "report", "--show-missing"], capture_output=False)
        
        # Abrir relatório HTML no navegador
        import webbrowser
        import os
        html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "htmlcov", "index.html")
        if os.path.exists(html_path):
            webbrowser.open(f"file://{os.path.abspath(html_path)}")
            print(f"\n✅ Relatório HTML aberto no navegador")
    except:
        pass

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Executar testes de cobertura completa")
    parser.add_argument(
        "--report",
        action="store_true",
        help="Gerar e abrir relatório de cobertura após os testes"
    )
    
    args = parser.parse_args()
    
    exit_code = run_complete_coverage()
    
    if args.report and exit_code == 0:
        generate_coverage_report()
    
    sys.exit(exit_code)