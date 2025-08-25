# 🌾 Brain Agriculture - Sistema de Produtores Rurais

[![CI/CD Status](https://img.shields.io/badge/CI%2FCD-passing-brightgreen)](https://github.com/actions)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Scala Version](https://img.shields.io/badge/scala-2.13+-red.svg)](https://scala-lang.org)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](tests/)

Sistema completo para gerenciamento de produtores rurais com APIs **Python (FastAPI)** e **Scala (Akka HTTP)** totalmente funcionais. Ambas as APIs incluem autenticação JWT, dashboard estatístico, documentação OpenAPI e sistema de testes abrangente.

## 🏗️ Estrutura do Projeto

```
brain-agriculture/
├── 🐍 api_python/              # API Python (FastAPI) - PRINCIPAL
│   ├── app/                    # Código da aplicação
│   │   ├── controllers/        # Endpoints da API
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── services/          # Lógica de negócio
│   │   └── utils/             # Utilitários e validadores
│   ├── tests/                 # Testes completos (100% cobertura)
│   │   ├── integration/       # Testes de integração
│   │   ├── unit/             # Testes unitários
│   │   └── scripts/          # Scripts de teste
│   └── docs/                 # Documentação específica
├── ⚡ api_scala/               # API Scala (Akka HTTP) - FUNCIONAL
│   ├── src/main/scala/       # Código Scala
│   │   ├── MinimalMain.scala # API principal com documentação
│   │   └── models/          # Modelos de dados
│   └── src/test/scala/       # Testes Scala
├── 🐳 docker/                  # Configurações Docker
├── 📋 docs/                    # Documentação geral
├── 🔧 scripts/                 # Scripts de automação
└── 🧪 CI/CD/                   # Pipeline automatizado
```

## Funcionalidades 🚀

### Core Features
- 🔐 **Autenticação JWT** completa
- 👥 Sistema de usuários e permissões (admin/comum)
- 🚜 Cadastro, edição e exclusão de produtores rurais
- 🏞️ Gerenciamento completo de fazendas
- 📊 Dashboard com estatísticas em tempo real:
  - Total de fazendas e hectares
  - Distribuição por estado
  - Distribuição por cultura
  - Distribuição por uso do solo

### Validações Implementadas
- ✅ Validação completa de CPF e CNPJ (dígitos verificadores)
- ✅ Validação de áreas (agricultável + vegetação ≤ área total)
- ✅ Autenticação obrigatória para todas as rotas
- ✅ Criptografia de senhas com BCrypt

## Como Executar 🚀

### Com Docker (Recomendado)

1. **Iniciar apenas a API Python (funcional):**

```bash
docker-compose up -d postgres api-python
```

2. **Ou iniciar todos os serviços:**

```bash
docker-compose up -d
```

**Serviços disponíveis:**
- 🐘 PostgreSQL na porta `5433`
- 🐍 **API Python na porta `8001`** (✅ 100% funcional + testes)
- ⚡ **API Scala na porta `8081`** (✅ 100% funcional + documentação)

### Acesso Rápido

**🌐 API Python:**
- **Swagger/Docs:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc
- **Health Check:** http://localhost:8001/health
- **Dashboard:** http://localhost:8001/api/dashboard/summary

**⚡ API Scala:**
- **Documentação:** http://localhost:8081/docs
- **OpenAPI JSON:** http://localhost:8081/openapi.json
- **Health Check:** http://localhost:8081/health
- **Dashboard:** http://localhost:8081/api/dashboard/summary

### Credenciais Padrão 🔑

Usuário admin criado automaticamente:
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@brazilagro.com`

## 🧪 Sistema de Testes

### Tipos de Testes Disponíveis

#### 📊 Cobertura Completa (33 rotas - 100%)
```bash
make test-complete-coverage  # Testa TODAS as rotas da API
```

#### 🔄 Testes CRUD Reais  
```bash
make test-real-crud          # CREATE → UPDATE → DELETE real
make test-crud-producer      # Teste específico de produtores
make test-crud-system        # Fluxo completo do sistema
```

#### 🔗 Testes com Dados Reais
```bash
make test-python-real        # Testes com PostgreSQL real
make test-python-all         # Todos os tipos de teste
```

#### 🏃‍♂️ Testes Rápidos
```bash  
make test-python             # Testes com mock (rápido)
make quick-test              # Validadores apenas
```

### Relatórios de Teste
- **Cobertura HTML**: `api_python/htmlcov/index.html`
- **Cobertura JSON**: `coverage.json`
- **Logs detalhados**: Terminal com cores

## 🚀 Comandos de Desenvolvimento

### Comandos Principais
```bash
make help                    # Ver todos os comandos disponíveis
make dev                     # Iniciar em modo desenvolvimento  
make build                   # Build de produção
make deploy-local            # Deploy local completo
make check-health            # Verificar status das APIs
```

### Comandos de CI/CD
```bash
make run-ci                  # Pipeline completo de CI/CD
make build-ci                # Build das imagens Docker
make clean-ci                # Limpar ambiente de CI
```

### Comandos de Limpeza
```bash
make clean-all               # Limpar tudo (containers, volumes, cache)
make logs-python             # Ver logs da API Python
make logs-scala              # Ver logs da API Scala
```

## 📖 Tutorial de Uso no Swagger

1. **Acesse:** http://localhost:8001/docs
2. **Faça login:**
   - Vá para `/api/auth/login`
   - Use: `username: admin` e `password: admin123`
   - Copie o `access_token` retornado

3. **Autorize-se:**
   - Clique no botão **"Authorize"** 🔒 no topo
   - Cole: `Bearer {seu_access_token_aqui}`
   - Clique em "Authorize"

4. **Agora você pode:**
   - ✅ Gerenciar produtores rurais (CRUD completo)
   - ✅ Criar e editar fazendas com validação
   - ✅ Gerenciar safras e culturas
   - ✅ Ver estatísticas no dashboard
   - ✅ Cadastrar novos usuários (apenas admin)

## 📋 Dados de Exemplo

São criados automaticamente ao iniciar o sistema:

### 👥 6 Produtores Rurais:
- **João Silva Santos** (CPF: 111.444.777-35)
- **Maria Oliveira Costa** (CPF: 987.654.321-00)  
- **Fazendas Reunidas Ltda** (CNPJ: 11.222.333/0001-81)
- **Pedro Almeida Ferreira** (CPF: 123.456.789-09)
- **Agropecuária Brasil S/A** (CNPJ: 114.447.770/0001-61)
- **Cooperativa Agrícola Central** (CNPJ: 223.334.440/0001-81)

### 🏡 11 Fazendas:
- **Fazenda Santa Rita** (Ribeirão Preto/SP) - 1.200ha
- **Sítio Boa Vista** (Franca/SP) - 450ha
- **Fazenda Esperança** (Uberaba/MG) - 2.500ha
- **Complexo Agropecuário Vale Verde** (Campo Grande/MS) - 5.000ha
- **Fazenda União** (Dourados/MS) - 3.200ha
- **Rancho Dois Irmãos** (Barretos/SP) - 800ha
- **Fazenda Continental** (Sorriso/MT) - 8.500ha
- **Fazenda Primavera** (Lucas do Rio Verde/MT) - 6.200ha
- **Chácara Felicidade** (Campinas/SP) - 120ha
- **Fazenda Cooperada Norte** (Cristalina/GO) - 4.800ha
- **Fazenda Cooperada Sul** (Rio Verde/GO) - 3.600ha

### 🌾 13 Safras (2024):
- Safras principais, safrinhas e de inverno
- Distribuídas entre todas as fazendas

### 🌱 26 Culturas:
- **Soja**: 22.150 hectares (60.8%)
- **Milho**: 7.300 hectares (20.0%) 
- **Algodão**: 5.200 hectares (14.3%)
- **Café**: 650 hectares (1.8%)
- **Cana-de-açúcar**: 1.150 hectares (3.2%)

### 📊 Estatísticas Totais:
- **Total de Fazendas**: 11
- **Área Total**: 36.900 hectares
- **Área Agrícola**: 30.950 hectares (83.9%)
- **Área de Vegetação**: 5.950 hectares (16.1%)

## 🗄️ Banco de Dados

### Modelo de Dados (PostgreSQL 15)

```sql
users                    producers               farms
├── id (Integer PK)      ├── id (Integer PK)     ├── id (Integer PK)  
├── username             ├── document            ├── producer_id (FK)
├── email                └── name                ├── name
├── hashed_password                              ├── city / state
├── is_active                                    ├── total_area
├── is_admin                                     ├── agricultural_area
└── created_at                                   └── vegetation_area

harvests                 crops
├── id (Integer PK)      ├── id (Integer PK)
├── farm_id (FK)         ├── harvest_id (FK) 
├── year                 ├── crop_type (ENUM)
└── description          └── planted_area
```

### Regras de Negócio Implementadas:
- ✅ **CPF**: 11 dígitos com validação de dígitos verificadores
- ✅ **CNPJ**: 14 dígitos com validação de dígitos verificadores  
- ✅ **Áreas**: `agricultural_area + vegetation_area ≤ total_area`
- ✅ **IDs**: Sequenciais com autoincrement (migrado de UUID)
- ✅ **Relacionamentos**: Cascata para deleção
- ✅ **Autenticação**: JWT com bcrypt para senhas

## 🔧 Tecnologias

### 🐍 API Python (Principal)
- **Python 3.11+** - Linguagem moderna
- **FastAPI 0.104+** - Framework web assíncrono
- **SQLAlchemy 2.0** - ORM robusto
- **Pydantic v2** - Validação de dados
- **JWT** - Autenticação segura
- **bcrypt** - Hash de senhas
- **pytest** - Framework de testes

### ⚡ API Scala (Funcional)
- **Scala 2.13** - Linguagem funcional
- **Akka HTTP 10.5** - Framework web reativo
- **Circe** - Serialização JSON
- **OpenAPI 3.0** - Documentação padrão
- **Docker** - Containerização completa

### 🗄️ Banco de Dados
- **PostgreSQL 15** - Banco relacional
- **Connection Pool** - Gerenciamento de conexões
- **Migrations** - Controle de schema
- **Índices otimizados** - Performance

### 🐳 DevOps & CI/CD
- **Docker & Docker Compose** - Containerização
- **GitHub Actions** - Pipeline automatizado  
- **Make** - Automação de comandos
- **Multi-stage builds** - Otimização de imagens

### 🧪 Testes & Qualidade
- **100% cobertura de rotas** - 33 endpoints
- **Testes unitários** - Lógica isolada
- **Testes de integração** - Fluxo completo
- **Testes CRUD reais** - Dados reais
- **Relatórios HTML** - Cobertura visual

## 📚 Documentação Adicional

### Relatórios Técnicos
- 📊 [**Cobertura de Testes**](api_python/tests/COVERAGE_SUMMARY.md) - Resumo de 100% cobertura
- 🔄 [**Testes CRUD Reais**](api_python/tests/REAL_CRUD_SUMMARY.md) - Sistema de testes sem fixtures  
- 🆔 [**Migração de IDs**](api_python/ID_MIGRATION_REPORT.md) - UUID → Integer sequencial

### Arquivos Importantes
```
📁 Configuração
├── docker-compose.yml      # Orquestração de serviços
├── Makefile                # Comandos automatizados
├── CLAUDE.md              # Instruções para desenvolvimento

📁 API Python
├── main.py                # Ponto de entrada da aplicação
├── requirements.txt       # Dependências Python
├── pytest.ini            # Configuração de testes

📁 Scripts de Teste
├── tests/run_real_crud.py       # CRUD real
├── tests/run_complete_coverage.py  # Cobertura completa  
├── tests/run_real_tests.py     # Testes com dados reais

📁 CI/CD
├── .github/workflows/      # GitHub Actions
├── docker-compose.ci.yml   # CI/CD específico
```

## 📊 Estatísticas do Projeto

| Métrica | Valor |
|---------|-------|
| **Total de Rotas** | 33 |
| **Cobertura de Testes** | 100% |
| **Entidades do Domínio** | 5 |
| **Comandos Make** | 15+ |
| **Arquivos de Teste** | 10+ |
| **Scripts de Automação** | 8+ |
| **Linhas de Código** | 3.000+ |

## 🚨 Troubleshooting

### Problemas Comuns

**🔴 Erro: "Port 5432 already in use"**
```bash
# O PostgreSQL usa porta 5433 para evitar conflitos
docker-compose down && docker-compose up -d
```

**🔴 Erro: "Access denied for user"**
```bash
# Resetar volumes do banco
make clean-all
make dev
```

**🔴 API não responde**
```bash
# Verificar logs
make logs-python
# Verificar saúde
make check-health
```

**🔴 Testes falhando**
```bash
# Verificar se containers estão rodando
docker-compose ps
# Executar testes diagnósticos
make quick-test
```

## 🤝 Contribuição

### Workflow
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)  
3. Commit com padrão (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrões de Commit
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `test:` - Testes
- `refactor:` - Refatoração

## 📞 Suporte

- **Documentação**: Sempre atualizada neste README
- **Swagger**: http://localhost:8001/docs (após iniciar)
- **Health Check**: `make check-health`
- **Logs**: `make logs-python`

---

**Desenvolvido por**: Kayo Carvalho Fernandes  
**Projeto**: Brain Agriculture - Teste Técnico  
**Versão**: 2.0.0  
**Última atualização**: 25/08/2025

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com)
[![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://python.org)
[![Scala](https://img.shields.io/badge/Made%20with-Scala-red.svg)](https://scala-lang.org)