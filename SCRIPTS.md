# 🔧 Scripts e Comandos - Guia Completo

## 📋 Visão Geral

Este documento lista todos os scripts e comandos disponíveis no projeto Brain Agriculture, organizados por categoria e função.

## 🐍 Scripts Python

### Scripts Principais

#### `api_python/test_runner.py`
**Função**: Sistema de testes personalizado da API Python
**Uso**:
```bash
cd api_python
python test_runner.py
```
**O que faz**:
- ✅ Executa testes dos validadores (CPF/CNPJ)
- ✅ Testa segurança básica (hash de senhas)
- ✅ Verifica importações dos módulos
- ✅ Relatório consolidado de status

#### `api_python/main.py`
**Função**: Ponto de entrada da aplicação FastAPI
**Uso**:
```bash
cd api_python
python main.py
# ou
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Scripts de Teste

#### `api_python/tests/run_complete_coverage.py`
**Função**: Executa cobertura completa de todas as 33 rotas
**Uso**:
```bash
cd api_python
python tests/run_complete_coverage.py --report
```
**Funcionalidades**:
- 🎯 Testa todas as 33 rotas da API
- 📊 Gera relatório de cobertura HTML
- ✅ Validação completa de endpoints

#### `api_python/tests/run_real_crud.py`
**Função**: Testes CRUD reais (CREATE → READ → UPDATE → DELETE)
**Uso**:
```bash
# Todos os testes CRUD
cd api_python && python tests/run_real_crud.py

# Teste específico
python tests/run_real_crud.py --test producer
python tests/run_real_crud.py --test system
```
**Opções disponíveis**:
- `producer`: Teste CRUD de produtores
- `farm`: Teste CRUD de fazendas
- `harvest`: Teste CRUD de safras
- `crop`: Teste CRUD de culturas
- `system`: Fluxo completo end-to-end

#### `api_python/tests/run_real_tests.py`
**Função**: Executa testes com dados reais do PostgreSQL
**Uso**:
```bash
cd api_python
python tests/run_real_tests.py --real-only  # Apenas testes reais
python tests/run_real_tests.py --all        # Mock + real
```

#### `api_python/tests/run_tests.py`
**Função**: Execução simples de testes unitários
**Uso**:
```bash
cd api_python
python tests/run_tests.py
```

#### `api_python/tests/test_validators_isolated.py`
**Função**: Testes isolados dos validadores (CPF/CNPJ)
**Uso**:
```bash
cd api_python
python tests/test_validators_isolated.py
```

### Scripts Utilitários Python

#### `api_python/app/seed_data.py`
**Função**: Popula banco com dados de exemplo
**Uso**:
```bash
cd api_python
python -c "from app.seed_data import create_sample_data; create_sample_data()"
```

#### `api_python/app/init_db.py`
**Função**: Inicializa banco de dados
**Uso**:
```bash
cd api_python
python app/init_db.py
```

## ⚡ Scripts Scala

### Scripts Principais

#### `api_scala/src/main/scala/Main.scala`
**Função**: Ponto de entrada da aplicação Scala
**Uso**:
```bash
cd api_scala
sbt run
```

#### `api_scala/src/test/scala/TestRunner.scala`
**Função**: Sistema customizado de testes Scala
**Uso**:
```bash
cd api_scala
sbt "runMain TestRunner"
```

## 🌍 Scripts Globais

#### `test_runner_global.py`
**Função**: Sistema de testes para ambas APIs (Python + Scala)
**Uso**:
```bash
python test_runner_global.py
```
**O que faz**:
- 🔍 Verifica estrutura do projeto
- 🐍 Executa testes Python
- ⚡ Informa sobre testes Scala
- 📊 Gera resumo final consolidado

## 🐳 Scripts Docker e CI/CD

### Scripts de Inicialização

#### `start.sh` (Linux/macOS)
```bash
chmod +x start.sh
./start.sh
```

#### `start.bat` (Windows)
```cmd
start.bat
```

#### `docker-compose.yml`
**Função**: Orquestração principal dos serviços
**Uso**:
```bash
# Iniciar todos os serviços
docker-compose up -d

# Apenas API Python + PostgreSQL
docker-compose up -d postgres api-python
```

#### `docker-compose.ci.yml`
**Função**: Configuração específica para CI/CD
**Uso**:
```bash
docker-compose -f docker-compose.ci.yml up --build
```

## 🛠️ Makefile - Comandos Automatizados

### Comandos de Teste

```bash
make test                    # Todos os testes
make test-python             # Testes Python com mock
make test-python-real        # Testes Python com PostgreSQL real
make test-python-coverage    # Cobertura de testes Python
make test-complete-coverage  # Cobertura de TODAS as rotas (33)
make test-real-crud          # Testes CRUD reais
make test-crud-producer      # CRUD específico de produtores
make test-crud-system        # Fluxo completo do sistema
make test-scala              # Testes Scala
```

### Comandos de Desenvolvimento

```bash
make dev                     # Modo desenvolvimento
make build                   # Build de produção
make deploy-local            # Deploy local completo
make clean-all               # Limpar tudo
make setup                   # Setup inicial
```

### Comandos de Monitoramento

```bash
make check-health            # Verificar saúde das APIs
make logs-python             # Logs da API Python
make logs-scala              # Logs da API Scala
make status                  # Status dos serviços
```

### Comandos de CI/CD

```bash
make build-ci                # Build para CI
make run-ci                  # Pipeline completo CI
make clean-ci                # Limpar ambiente CI
```

## 📊 Scripts de Análise

### Comandos de Cobertura

```bash
# Relatório de cobertura HTML
cd api_python && pytest tests/ --cov=app --cov-report=html

# Cobertura completa (33 rotas)
make test-complete-coverage

# Cobertura JSON
cd api_python && pytest tests/ --cov=app --cov-report=json
```

### Comandos de Qualidade

```bash
# Scala
cd api_scala && sbt scalafmt              # Formatar código
cd api_scala && sbt scalafmtCheck         # Verificar formatação

# Python (se tiver)
cd api_python && black .                  # Formatar código Python
cd api_python && flake8                   # Linter Python
```

## 🔄 Workflows Comuns

### Desenvolvimento Completo

```bash
# 1. Setup inicial
make setup

# 2. Iniciar desenvolvimento
make dev

# 3. Executar testes
make test-python-real

# 4. Verificar cobertura
make test-complete-coverage

# 5. Verificar saúde
make check-health
```

### Teste CRUD Completo

```bash
# 1. Testar produtores
make test-crud-producer

# 2. Testar sistema completo
make test-crud-system

# 3. Cobertura completa
make test-complete-coverage
```

### Deploy e Monitoramento

```bash
# 1. Deploy local
make deploy-local

# 2. Verificar saúde
make check-health

# 3. Monitorar logs
make logs-python
```

## 🎯 Scripts por Caso de Uso

### Para Desenvolvedores

1. **Setup inicial**: `make setup`
2. **Desenvolvimento**: `make dev`
3. **Testes rápidos**: `make quick-test`
4. **Testes completos**: `make test-python-real`

### Para QA/Testes

1. **Cobertura completa**: `make test-complete-coverage`
2. **Testes CRUD**: `make test-real-crud`
3. **Testes específicos**: `make test-crud-producer`
4. **Fluxo end-to-end**: `make test-crud-system`

### Para DevOps

1. **Build CI**: `make build-ci`
2. **Pipeline completo**: `make run-ci`
3. **Deploy local**: `make deploy-local`
4. **Monitoramento**: `make check-health`

### Para Demonstração

1. **Iniciar sistema**: `docker-compose up -d postgres api-python`
2. **Verificar saúde**: `make check-health`
3. **Acessar documentação**: http://localhost:8001/docs

## ⚠️ Troubleshooting de Scripts

### Problemas Comuns

**🔴 "pytest not found"**
```bash
cd api_python && pip install pytest
```

**🔴 "sbt not found"**
```bash
# Instalar SBT para testes Scala
# Ver: https://www.scala-sbt.org/download.html
```

**🔴 "Port already in use"**
```bash
make clean-all  # Limpa tudo
docker-compose down --volumes
```

**🔴 "Permission denied (Linux/macOS)"**
```bash
chmod +x start.sh
chmod +x scripts/*.sh  # se houver pasta scripts
```

## 📈 Métricas dos Scripts

| Categoria | Quantidade |
|-----------|------------|
| **Scripts Python** | 8 |
| **Scripts Scala** | 2 |
| **Scripts Docker** | 3 |
| **Comandos Make** | 20+ |
| **Scripts de Teste** | 6 |
| **Scripts Utilitários** | 4 |

## 🔗 Referências

- **Makefile Principal**: Todos os comandos automatizados
- **Python Scripts**: Diretório `api_python/` e `api_python/tests/`
- **Scala Scripts**: Diretório `api_scala/src/`
- **Docker Scripts**: Arquivos `docker-compose.*.yml`
- **Documentação de Testes**: `api_python/tests/REAL_CRUD_SUMMARY.md`

---

**Última atualização**: 25/08/2025  
**Projeto**: Brain Agriculture - Sistema de Produtores Rurais