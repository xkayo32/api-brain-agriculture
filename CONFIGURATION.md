# ⚙️ Configuração - Brain Agriculture

## 📋 Visão Geral

Este documento descreve todas as configurações do projeto Brain Agriculture, incluindo variáveis de ambiente, arquivos de configuração e configurações específicas para desenvolvimento, teste e produção.

## 🗂️ Arquivos de Configuração

### Estrutura de Configurações

```
brain-agriculture/
├── 🐳 docker-compose.yml        # Orquestração principal
├── 🐳 docker-compose.ci.yml     # Pipeline CI/CD
├── 🔧 init-db.sql               # Inicialização do banco
├── 🐍 api_python/
│   ├── .env                     # Variáveis Python (desenvolvimento)
│   ├── pytest.ini              # Configuração de testes
│   └── requirements.txt         # Dependências Python
├── ⚡ api_scala/
│   ├── build.sbt                # Configuração SBT
│   ├── src/main/resources/
│   │   └── application.conf     # Configuração Scala
│   └── src/test/resources/
│       └── application.conf     # Configuração testes Scala
└── 🛠️ Makefile                  # Comandos automatizados
```

## 🐳 Docker Compose

### `docker-compose.yml` - Desenvolvimento

**PostgreSQL**:
```yaml
postgres:
  image: postgres:15
  container_name: rural_producers_db
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    POSTGRES_DB: rural_producers
  ports:
    - "5433:5432"  # Evita conflito com PostgreSQL local
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

**API Python**:
```yaml
api-python:
  build: ./api_python
  container_name: api_python
  ports:
    - "8001:8000"  # Externa:Interna
  environment:
    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/rural_producers
    SERVER_HOST: 0.0.0.0
    SERVER_PORT: 8000
```

**API Scala (Comentada)**:
```yaml
# api-scala:  # Temporariamente desabilitado
#   build: ./api_scala
#   ports:
#     - "8080:8080"
#   environment:
#     DATABASE_URL: jdbc:postgresql://postgres:5432/rural_producers
```

### `docker-compose.ci.yml` - CI/CD

**Características**:
- ✅ **Healthchecks**: Aguarda banco estar pronto
- ✅ **Credenciais CI**: Usuário e banco específicos
- ✅ **Pipeline**: Testa Python + Scala + Global
- ✅ **Isolamento**: Network separada para CI

**PostgreSQL CI**:
```yaml
postgres-ci:
  image: postgres:13-alpine
  environment:
    POSTGRES_DB: ci_brain_agriculture
    POSTGRES_USER: ci_user
    POSTGRES_PASSWORD: ci_pass
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U ci_user -d ci_brain_agriculture"]
    interval: 10s
    timeout: 5s
    retries: 5
```

## 🐍 Configurações Python

### `.env` - Variáveis de Ambiente

```env
# Banco de dados
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rural_producers

# Servidor
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Segurança (adicionar se necessário)
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Debug (desenvolvimento)
DEBUG=True
LOG_LEVEL=DEBUG
```

### `pytest.ini` - Configuração de Testes

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v 
    --tb=short 
    --strict-markers
    --disable-warnings
    --color=yes
markers =
    unit: marca testes unitários
    integration: marca testes de integração
    crud: marca testes CRUD reais
    coverage: marca testes de cobertura
```

### `requirements.txt` - Dependências

```txt
# Web Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0

# Database
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0

# Validation & Serialization
pydantic>=2.0.0
pydantic-settings

# Security
python-jose[cryptography]
passlib[bcrypt]
python-multipart

# Testing
pytest>=7.0.0
pytest-cov
httpx

# Development
python-dotenv
```

## ⚡ Configurações Scala

### `build.sbt` - Configuração SBT

```scala
ThisBuild / version := "1.0.0"
ThisBuild / scalaVersion := "2.13.12"

lazy val root = (project in file("."))
  .settings(
    name := "brain-agriculture-scala",
    libraryDependencies ++= Seq(
      // Akka HTTP
      "com.typesafe.akka" %% "akka-http" % "10.5.0",
      "com.typesafe.akka" %% "akka-actor-typed" % "2.8.0",
      "com.typesafe.akka" %% "akka-stream" % "2.8.0",
      
      // JSON
      "io.circe" %% "circe-core" % "0.14.0",
      "io.circe" %% "circe-generic" % "0.14.0",
      "io.circe" %% "circe-parser" % "0.14.0",
      
      // Database
      "com.typesafe.slick" %% "slick" % "3.4.1",
      "com.typesafe.slick" %% "slick-hikaricp" % "3.4.1",
      "org.postgresql" % "postgresql" % "42.6.0",
      
      // Testing
      "org.scalatest" %% "scalatest" % "3.2.16" % Test,
      "com.typesafe.akka" %% "akka-http-testkit" % "10.5.0" % Test
    )
  )
```

### `application.conf` - Configuração Principal

```hocon
# Database Configuration
database {
  url = "jdbc:postgresql://localhost:5432/rural_producers"
  url = ${?DATABASE_URL}
  user = "postgres"
  user = ${?DB_USER}
  password = "postgres"
  password = ${?DB_PASSWORD}
  driver = "org.postgresql.Driver"
  connectionPool = "HikariCP"
  keepAliveConnection = true
  numThreads = 10
  maxConnections = 20
}

# Server Configuration
server {
  host = "0.0.0.0"
  host = ${?SERVER_HOST}
  port = 8080
  port = ${?SERVER_PORT}
}

# JWT Configuration (se implementado)
jwt {
  secret = "default-jwt-secret"
  secret = ${?JWT_SECRET}
  expiration = 3600  # 1 hora em segundos
}

# Akka Configuration
akka {
  loglevel = "INFO"
  
  http {
    server {
      request-timeout = 20s
      idle-timeout = 60s
      max-connections = 1024
    }
  }
}
```

### `application.conf` - Testes

```hocon
# Test Database Configuration
database {
  url = "jdbc:postgresql://localhost:5433/test_rural_producers"
  url = ${?TEST_DATABASE_URL}
  user = "postgres"
  password = "postgres"
  driver = "org.postgresql.Driver"
  connectionPool = "HikariCP"
  numThreads = 2
  maxConnections = 5
}

# Test Server Configuration
server {
  host = "localhost"
  port = 0  # Random port for testing
}

jwt {
  secret = "test-jwt-secret"
  expiration = 300  # 5 minutos para testes
}

akka {
  loglevel = "WARNING"
  
  http {
    server {
      request-timeout = 5s
    }
  }
}
```

## 🗄️ Configuração do Banco

### `init-db.sql` - Inicialização

```sql
-- Criar banco se não existir
CREATE DATABASE IF NOT EXISTS rural_producers;

-- Criar usuário específico (se necessário)
-- CREATE USER brain_user WITH PASSWORD 'brain_pass';
-- GRANT ALL PRIVILEGES ON DATABASE rural_producers TO brain_user;

-- Configurações de performance
ALTER DATABASE rural_producers SET timezone TO 'America/Sao_Paulo';
```

### Strings de Conexão

#### Desenvolvimento
```bash
# Python
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/rural_producers

# Scala
DATABASE_URL=jdbc:postgresql://localhost:5433/rural_producers?user=postgres&password=postgres
```

#### Docker (Interno)
```bash
# Python (container interno)
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/rural_producers

# Scala (container interno)  
DATABASE_URL=jdbc:postgresql://postgres:5432/rural_producers?user=postgres&password=postgres
```

#### CI/CD
```bash
# Python CI
DATABASE_URL=postgresql://ci_user:ci_pass@postgres-ci:5432/ci_brain_agriculture

# Scala CI
DATABASE_URL=jdbc:postgresql://postgres-ci:5432/ci_brain_agriculture?user=ci_user&password=ci_pass
```

## 🔧 Variáveis de Ambiente

### Variáveis Principais

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| **DATABASE_URL** | `postgresql://postgres:postgres@localhost:5433/rural_producers` | URL completa do banco |
| **SERVER_HOST** | `0.0.0.0` | Host do servidor |
| **SERVER_PORT** | `8000` (Python) / `8080` (Scala) | Porta do servidor |
| **SECRET_KEY** | `your-secret-key-here` | Chave secreta JWT |
| **DEBUG** | `True` | Modo debug (desenvolvimento) |

### Variáveis de Segurança

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| **JWT_SECRET** | `default-jwt-secret` | Segredo para JWT |
| **ACCESS_TOKEN_EXPIRE_MINUTES** | `30` | Expiração do token (minutos) |
| **BCRYPT_ROUNDS** | `12` | Rounds do BCrypt |

### Variáveis de Banco

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| **DB_USER** | `postgres` | Usuário do banco |
| **DB_PASSWORD** | `postgres` | Senha do banco |
| **DB_HOST** | `localhost` | Host do banco |
| **DB_PORT** | `5433` | Porta do banco |
| **DB_NAME** | `rural_producers` | Nome do banco |

### Variáveis de Teste

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| **TEST_DATABASE_URL** | `postgresql://postgres:postgres@localhost:5433/test_rural_producers` | Banco para testes |
| **PYTEST_ARGS** | `-v --tb=short` | Argumentos do pytest |

## 🌍 Configurações por Ambiente

### Desenvolvimento Local

```bash
# .env para desenvolvimento
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/rural_producers
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=True
LOG_LEVEL=DEBUG
SECRET_KEY=dev-secret-key-not-for-production
```

### Testes

```bash
# .env.test
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/test_rural_producers
SERVER_HOST=localhost
SERVER_PORT=8001
DEBUG=False
LOG_LEVEL=WARNING
SECRET_KEY=test-secret-key
```

### Docker Compose

```bash
# Variáveis no docker-compose.yml
environment:
  - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/rural_producers
  - SERVER_HOST=0.0.0.0
  - SERVER_PORT=8000
```

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/ci.yml
env:
  DATABASE_URL: postgresql://ci_user:ci_pass@localhost:5432/ci_brain_agriculture
  SECRET_KEY: ${{ secrets.JWT_SECRET }}
  DEBUG: false
```

### Produção

```bash
# .env.production (exemplo)
DATABASE_URL=postgresql://prod_user:$STRONG_PASSWORD@prod-db:5432/brain_agriculture_prod
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False
LOG_LEVEL=INFO
SECRET_KEY=$JWT_SECRET_FROM_VAULT
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 🔒 Configurações de Segurança

### JWT Configuration

```python
# Python (config.py)
from datetime import timedelta

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
ALGORITHM = "HS256"
```

```scala
// Scala (application.conf)
jwt {
  secret = ${?JWT_SECRET}
  expiration = ${?JWT_EXPIRATION_SECONDS}
  algorithm = "HS256"
}
```

### BCrypt Configuration

```python
# Python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=int(os.getenv("BCRYPT_ROUNDS", "12"))
)
```

### Database Security

```sql
-- Configurações de segurança no PostgreSQL
-- Limitar conexões
ALTER DATABASE rural_producers SET max_connections = 100;

-- SSL (se necessário)
-- ALTER DATABASE rural_producers SET ssl = on;
```

## 📊 Configurações de Performance

### Connection Pool

```python
# Python (SQLAlchemy)
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

engine = create_engine(
    DATABASE_URL,
    pool_size=20,              # Conexões no pool
    max_overflow=30,           # Conexões extras
    pool_timeout=30,           # Timeout para obter conexão
    pool_recycle=3600,         # Reciclar conexões (1h)
    pool_pre_ping=True         # Verificar conexão antes de usar
)
```

```scala
// Scala (Slick HikariCP)
database {
  connectionPool = "HikariCP"
  numThreads = 10
  maxConnections = 20
  minConnections = 5
  connectionTimeout = 30000
  idleTimeout = 600000
  maxLifetime = 1800000
  leakDetectionThreshold = 60000
}
```

### Server Configuration

```python
# Python (Uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVER_PORT", "8000")),
        workers=int(os.getenv("WORKERS", "4")),
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
```

## 🚀 Configurações de Deploy

### Docker Build Args

```dockerfile
# Dockerfile com argumentos
ARG ENVIRONMENT=production
ARG DEBUG=false

ENV ENVIRONMENT=${ENVIRONMENT}
ENV DEBUG=${DEBUG}
```

### Health Checks

```yaml
# docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Resource Limits

```yaml
# docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

## ⚙️ Configurações Específicas

### Logging

```python
# Python logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["default"],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### CORS Configuration

```python
# Python FastAPI CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurar adequadamente para produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🛠️ Comandos de Configuração

### Setup Inicial

```bash
# Configurar ambiente Python
cd api_python
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt

# Configurar .env
cp .env.example .env  # se existir
# Editar .env com configurações locais
```

### Verificação de Configuração

```bash
# Verificar configuração Python
cd api_python && python -c "from app.config import *; print('Config OK')"

# Verificar configuração Scala
cd api_scala && sbt compile

# Verificar Docker
docker-compose config

# Verificar banco
make check-health
```

### Reset de Configuração

```bash
# Limpar tudo e reconfigurar
make clean-all
make setup
make dev
```

## 🔍 Troubleshooting de Configuração

### Problemas Comuns

**🔴 "Connection refused" (PostgreSQL)**
- Verificar se porta 5433 está correta
- Verificar se PostgreSQL está rodando: `docker-compose ps postgres`

**🔴 "Invalid JWT Secret"**
- Verificar se SECRET_KEY está definida
- Verificar se não contém caracteres especiais problemáticos

**🔴 "Module not found"**
- Verificar se PYTHONPATH está correto
- Verificar se dependências estão instaladas: `pip install -r requirements.txt`

**🔴 "SBT compilation error"**
- Verificar se Java 11+ está instalado
- Limpar cache SBT: `cd api_scala && sbt clean`

### Debug de Configuração

```bash
# Ver configurações carregadas (Python)
cd api_python && python -c "
import os
from app.config import *
print('DATABASE_URL:', os.getenv('DATABASE_URL'))
print('SERVER_HOST:', os.getenv('SERVER_HOST'))
print('SERVER_PORT:', os.getenv('SERVER_PORT'))
"

# Ver variáveis de ambiente do container
docker-compose exec api-python env | grep -E "(DATABASE|SERVER|SECRET)"
```

---

**Desenvolvido por**: Kayo Carvalho Fernandes  
**Projeto**: Brain Agriculture - Sistema de Produtores Rurais  
**Última atualização**: 25/08/2025