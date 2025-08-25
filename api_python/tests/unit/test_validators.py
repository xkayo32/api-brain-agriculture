"""
Testes unitarios dos validadores
"""
import pytest
from app.utils.validators import validate_cpf, validate_cnpj, validate_document, format_document

class TestCPFValidator:
    """Testes de validacao de CPF"""
    
    @pytest.mark.unit
    def test_cpf_valid(self):
        """Testa CPFs validos"""
        # CPFs validos comuns
        assert validate_cpf("11144477735") == True
        assert validate_cpf("12345678909") == True
        assert validate_cpf("98765432100") == True
        
    @pytest.mark.unit
    def test_cpf_valid_with_formatting(self):
        """Testa CPFs validos com formatacao"""
        assert validate_cpf("111.444.777-35") == True
        assert validate_cpf("123.456.789-09") == True
        assert validate_cpf("987.654.321-00") == True
    
    @pytest.mark.unit
    def test_cpf_invalid_wrong_digits(self):
        """Testa CPFs com digitos verificadores errados"""
        assert validate_cpf("11144477736") == False  # ultimo digito errado
        assert validate_cpf("11144477725") == False  # penultimo digito errado
        assert validate_cpf("12345678901") == False  # ambos errados
    
    @pytest.mark.unit
    def test_cpf_invalid_same_digits(self):
        """Testa CPFs com todos os digitos iguais"""
        assert validate_cpf("11111111111") == False
        assert validate_cpf("22222222222") == False
        assert validate_cpf("00000000000") == False
    
    @pytest.mark.unit
    def test_cpf_invalid_length(self):
        """Testa CPFs com tamanho incorreto"""
        assert validate_cpf("1234567890") == False   # 10 digitos
        assert validate_cpf("123456789012") == False # 12 digitos
        assert validate_cpf("") == False             # vazio
        assert validate_cpf("abc") == False          # muito pequeno
    
    @pytest.mark.unit
    def test_cpf_invalid_non_numeric(self):
        """Testa CPFs com caracteres nao numericos"""
        assert validate_cpf("1234567890a") == False
        assert validate_cpf("abcdefghijk") == False

class TestCNPJValidator:
    """Testes de validacao de CNPJ"""
    
    @pytest.mark.unit
    def test_cnpj_valid(self):
        """Testa CNPJs validos"""
        assert validate_cnpj("11222333000181") == True
        assert validate_cnpj("11444777000161") == True
        
    @pytest.mark.unit
    def test_cnpj_valid_with_formatting(self):
        """Testa CNPJs validos com formatacao"""
        assert validate_cnpj("11.222.333/0001-81") == True
        assert validate_cnpj("11.444.777/0001-61") == True
    
    @pytest.mark.unit
    def test_cnpj_invalid_wrong_digits(self):
        """Testa CNPJs com digitos verificadores errados"""
        assert validate_cnpj("11222333000191") == False
        assert validate_cnpj("11222333000192") == False
    
    @pytest.mark.unit
    def test_cnpj_invalid_same_digits(self):
        """Testa CNPJs com todos os digitos iguais"""
        assert validate_cnpj("11111111111111") == False
        assert validate_cnpj("00000000000000") == False
    
    @pytest.mark.unit
    def test_cnpj_invalid_length(self):
        """Testa CNPJs com tamanho incorreto"""
        assert validate_cnpj("1122233300019") == False   # 13 digitos
        assert validate_cnpj("112223330001911") == False # 15 digitos
        assert validate_cnpj("") == False                # vazio

class TestDocumentValidator:
    """Testes do validador generico de documentos"""
    
    @pytest.mark.unit
    def test_validate_document_cpf(self):
        """Testa validacao de CPF via validate_document"""
        assert validate_document("11144477735") == True
        assert validate_document("111.444.777-35") == True
        assert validate_document("11144477736") == False
    
    @pytest.mark.unit
    def test_validate_document_cnpj(self):
        """Testa validacao de CNPJ via validate_document"""
        assert validate_document("11222333000181") == True
        assert validate_document("11.222.333/0001-81") == True
        assert validate_document("11222333000192") == False
    
    @pytest.mark.unit
    def test_validate_document_invalid_length(self):
        """Testa documentos com tamanho invalido"""
        assert validate_document("123456789") == False    # nem CPF nem CNPJ
        assert validate_document("123456789012345") == False # muito grande

class TestDocumentFormatter:
    """Testes do formatador de documentos"""
    
    @pytest.mark.unit
    def test_format_cpf(self):
        """Testa formatacao de CPF"""
        assert format_document("11144477735") == "111.444.777-35"
        assert format_document("12345678909") == "123.456.789-09"
        
    @pytest.mark.unit
    def test_format_cnpj(self):
        """Testa formatacao de CNPJ"""
        assert format_document("11222333000191") == "11.222.333/0001-91"
        assert format_document("34073077000102") == "34.073.077/0001-02"
    
    @pytest.mark.unit
    def test_format_already_formatted(self):
        """Testa formatacao de documento ja formatado"""
        # Se o documento nao tem o tamanho certo, retorna como esta
        formatted_cpf = format_document("111.444.777-35")
        assert formatted_cpf == "111.444.777-35"  # retorna como esta
    
    @pytest.mark.unit
    def test_format_invalid_document(self):
        """Testa formatacao de documento invalido"""
        assert format_document("123") == "123"        # retorna como esta
        assert format_document("invalid") == "invalid" # retorna como esta