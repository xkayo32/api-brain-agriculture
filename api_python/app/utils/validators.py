def validate_cpf(cpf: str) -> bool:
    """
    Valida se o CPF e valido
    """
    # Remove caracteres nao numericos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se tem 11 digitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os digitos sao iguais
    if len(set(cpf)) == 1:
        return False
    
    # Calcula o primeiro digito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    if digito1 >= 10:
        digito1 = 0
    
    # Verifica o primeiro digito
    if int(cpf[9]) != digito1:
        return False
    
    # Calcula o segundo digito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    if digito2 >= 10:
        digito2 = 0
    
    # Verifica o segundo digito
    return int(cpf[10]) == digito2

def validate_cnpj(cnpj: str) -> bool:
    """
    Valida se o CNPJ e valido
    """
    # Remove caracteres nao numericos
    cnpj = ''.join(filter(str.isdigit, cnpj))
    
    # Verifica se tem 14 digitos
    if len(cnpj) != 14:
        return False
    
    # Verifica se todos os digitos sao iguais
    if len(set(cnpj)) == 1:
        return False
    
    # Pesos para o calculo
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Calcula o primeiro digito verificador
    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Verifica o primeiro digito
    if int(cnpj[12]) != digito1:
        return False
    
    # Calcula o segundo digito verificador
    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica o segundo digito
    return int(cnpj[13]) == digito2

def validate_document(document: str) -> bool:
    """
    Valida se e um CPF ou CNPJ valido
    """
    # Remove caracteres nao numericos
    clean_doc = ''.join(filter(str.isdigit, document))
    
    if len(clean_doc) == 11:
        return validate_cpf(clean_doc)
    elif len(clean_doc) == 14:
        return validate_cnpj(clean_doc)
    else:
        return False

def format_document(document: str) -> str:
    """
    Formata CPF ou CNPJ para exibicao
    """
    clean_doc = ''.join(filter(str.isdigit, document))
    
    if len(clean_doc) == 11:
        # Formato CPF: 000.000.000-00
        return f"{clean_doc[:3]}.{clean_doc[3:6]}.{clean_doc[6:9]}-{clean_doc[9:]}"
    elif len(clean_doc) == 14:
        # Formato CNPJ: 00.000.000/0000-00
        return f"{clean_doc[:2]}.{clean_doc[2:5]}.{clean_doc[5:8]}/{clean_doc[8:12]}-{clean_doc[12:]}"
    else:
        return document