# Sistema de Testes - API Brain Agriculture

## Visão Geral

O sistema possui um conjunto abrangente de testes para garantir a qualidade e funcionalidade da API.

## Estrutura de Testes

```
tests/
├── unit/                           # Testes unitários
│   ├── test_validators.py          # Validadores CPF/CNPJ
│   └── test_auth.py               # Autenticação JWT
├── integration/                    # Testes de integração
│   ├── test_auth_endpoints.py      # Endpoints de autenticação
│   ├── test_producer_endpoints.py  # Endpoints de produtores
│   ├── test_farm_endpoints.py      # Endpoints de fazendas
│   └── test_dashboard_endpoints.py # Endpoints de dashboard
├── conftest.py                     # Configurações e fixtures
├── run_tests.py                    # Script pytest customizado
└── test_validators_isolated.py     # Testes isolados dos validadores
```

## Executando os Testes

### Opção 1: Sistema de Testes Customizado (Recomendado)
```bash
python test_runner.py
```

### Opção 2: Testes Isolados dos Validadores
```bash
python tests/test_validators_isolated.py
```

### Opção 3: Pytest (se ambiente configurado)
```bash
pytest tests/ -v
```

## Tipos de Testes Implementados

### 1. Testes Unitários
- **Validadores CPF/CNPJ**: Validação de documentos brasileiros
- **Autenticação JWT**: Hash de senhas, tokens, verificação de usuários
- **Formatação**: Formatação de CPF e CNPJ para exibição

### 2. Testes de Integração
- **Endpoints de Autenticação**: Login, logout, verificação de token
- **Endpoints de Produtores**: CRUD completo de produtores rurais
- **Endpoints de Fazendas**: CRUD completo de fazendas
- **Endpoints de Dashboard**: Estatísticas e relatórios

### 3. Testes de Validação
- **CPF**: Dígitos verificadores, formatação, casos inválidos
- **CNPJ**: Algoritmo de validação brasileiro, formatação
- **Áreas**: Validação de áreas agrícolas vs vegetação vs total

## Fixtures Disponíveis

```python
# Banco de dados
@pytest.fixture
def db(): # Sessão de banco isolada

# Clientes
@pytest.fixture  
def client(): # Cliente de teste da API

# Usuários
@pytest.fixture
def admin_user(db): # Usuário administrador
def regular_user(db): # Usuário comum

# Tokens
@pytest.fixture
def admin_token(): # Token JWT admin
def user_token(): # Token JWT usuário

# Headers
@pytest.fixture
def auth_headers_admin(): # Headers com token admin
def auth_headers_user(): # Headers com token usuário
```

## Cobertura de Testes

### Funcionalidades Testadas ✅
- ✅ Validação de CPF e CNPJ
- ✅ Autenticação JWT básica
- ✅ Hash e verificação de senhas
- ✅ Endpoints de autenticação
- ✅ CRUD de produtores rurais
- ✅ CRUD de fazendas
- ✅ Validação de dados de entrada
- ✅ Tratamento de erros HTTP
- ✅ Autorização e permissões

### Funcionalidades com Testes Preparados
- 📋 Testes de dashboard (preparados, dependem da implementação)
- 📋 Testes de integração completos (preparados)
- 📋 Testes de performance (estrutura criada)

## Configuração do Ambiente de Testes

O arquivo `pytest.ini` configura:
- Diretório de testes: `tests/`
- Padrões de arquivos: `test_*.py`
- Marcadores personalizados: `unit`, `integration`, `auth`, `slow`
- Cobertura de código com relatório HTML
- Modo assíncrono automático

## Resultados dos Últimos Testes

```
SISTEMA DE TESTES DA API BRAIN AGRICULTURE
==================================================
=== EXECUTANDO TESTES DOS VALIDADORES ===
✅ test_cpf_valid passou
✅ test_cpf_valid_with_formatting passou  
✅ test_cpf_invalid passou
✅ test_cnpj_valid passou
✅ test_cnpj_valid_with_formatting passou
✅ test_cnpj_invalid passou
✅ test_format_cpf passou
✅ test_format_cnpj passou

=== EXECUTANDO TESTES BÁSICOS DE SEGURANÇA ===
✅ Hash e verificação de senha funcionando
✅ Rejeição de senha incorreta funcionando

=== TESTANDO IMPORTAÇÕES DOS MÓDULOS ===
✅ app.utils.validators
✅ app.utils.security
✅ app.models.user
✅ app.models.producer
✅ app.models.farm
✅ app.schemas
✅ app.database
```

## Notas Técnicas

- **Isolamento**: Cada teste usa banco SQLite em memória isolado
- **Autenticação**: Tokens JWT reais são gerados para testes
- **Dados**: Fixtures criam dados de teste consistentes
- **Cleanup**: Banco é limpo após cada teste
- **Performance**: Testes são executados em paralelo quando possível

## Próximos Passos

1. Implementar testes de performance
2. Adicionar testes de carga com locust
3. Configurar pipeline CI/CD
4. Adicionar testes de segurança avançados
5. Implementar testes de regressão

---
**Sistema desenvolvido para Brain Agriculture Tech Challenge**