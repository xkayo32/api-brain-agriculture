"""
Script para executar testes sem depender do FastAPI
"""
import pytest
import sys
import os

# Adicionar o diretorio da aplicacao ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

if __name__ == "__main__":
    # Executar apenas testes unitarios basicos
    pytest.main([
        "tests/unit/test_validators.py",
        "-v",
        "--tb=short"
    ])