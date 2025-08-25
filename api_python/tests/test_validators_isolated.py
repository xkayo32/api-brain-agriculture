"""
Teste isolado dos validadores sem dependencias do FastAPI
"""
import sys
import os

# Adicionar diretorio pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.utils.validators import validate_cpf, validate_cnpj, validate_document, format_document

def test_cpf_valid():
    """Testa CPFs validos"""
    assert validate_cpf("11144477735") == True
    assert validate_cpf("12345678909") == True
    assert validate_cpf("98765432100") == True

def test_cpf_valid_with_formatting():
    """Testa CPFs validos com formatacao"""
    assert validate_cpf("111.444.777-35") == True
    assert validate_cpf("123.456.789-09") == True

def test_cpf_invalid():
    """Testa CPFs invalidos"""
    assert validate_cpf("11144477736") == False
    assert validate_cpf("11111111111") == False
    assert validate_cpf("1234567890") == False

def test_cnpj_valid():
    """Testa CNPJs validos"""
    # Usar CNPJs reais validos
    assert validate_cnpj("11222333000181") == True  # CNPJ valido corrigido
    assert validate_cnpj("11444777000161") == True  # Outro CNPJ valido

def test_cnpj_valid_with_formatting():
    """Testa CNPJs validos com formatacao"""
    assert validate_cnpj("11.222.333/0001-81") == True

def test_cnpj_invalid():
    """Testa CNPJs invalidos"""
    assert validate_cnpj("11222333000192") == False
    assert validate_cnpj("11111111111111") == False

def test_format_cpf():
    """Testa formatacao de CPF"""
    assert format_document("11144477735") == "111.444.777-35"

def test_format_cnpj():
    """Testa formatacao de CNPJ"""
    assert format_document("11222333000181") == "11.222.333/0001-81"

if __name__ == "__main__":
    print("Executando testes dos validadores...")
    
    try:
        test_cpf_valid()
        print("OK test_cpf_valid passou")
        
        test_cpf_valid_with_formatting()
        print("OK test_cpf_valid_with_formatting passou")
        
        test_cpf_invalid()
        print("OK test_cpf_invalid passou")
        
        test_cnpj_valid()
        print("OK test_cnpj_valid passou")
        
        test_cnpj_valid_with_formatting()
        print("OK test_cnpj_valid_with_formatting passou")
        
        test_cnpj_invalid()
        print("OK test_cnpj_invalid passou")
        
        test_format_cpf()
        print("OK test_format_cpf passou")
        
        test_format_cnpj()
        print("OK test_format_cnpj passou")
        
        print("\nTodos os testes dos validadores passaram com sucesso!")
        
    except AssertionError as e:
        print(f"ERRO: Teste falhou: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERRO: Erro durante teste: {e}")
        sys.exit(1)