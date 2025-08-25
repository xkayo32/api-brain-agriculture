# 👨‍💻 Guia de Desenvolvimento - Brain Agriculture

## 🎯 Visão Geral

Este guia orienta desenvolvedores sobre como contribuir, configurar o ambiente e seguir as melhores práticas no projeto Brain Agriculture.

## 🏗️ Arquitetura do Sistema

### Estrutura Geral

```
brain-agriculture/
├── 🐍 api_python/              # API Principal (FastAPI)
│   ├── app/                    # Core da aplicação
│   │   ├── controllers/        # Endpoints REST
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── services/          # Lógica de negócio
│   │   ├── utils/             # Validadores e utilitários
│   │   └── schemas.py         # Esquemas Pydantic
│   └── tests/                 # Testes (100% cobertura)
├── ⚡ api_scala/               # API Alternativa (Akka HTTP)
│   ├── src/main/scala/        # Código Scala
│   │   ├── controllers/       # Controllers REST
│   │   ├── models/           # Modelos de domínio
│   │   ├── services/         # Serviços de negócio
│   │   ├── repositories/     # Acesso a dados
│   │   └── utils/           # Utilitários e validadores
│   └── src/test/scala/       # Testes Scala
└── 🐳 docker/                 # Configurações Docker
```

### Camadas da Aplicação

#### Python (FastAPI) - Principal

```
┌─────────────────────────────┐
│     Controllers             │  ← REST Endpoints
├─────────────────────────────┤
│     Services                │  ← Lógica de Negócio
├─────────────────────────────┤
│     Models (SQLAlchemy)     │  ← ORM / Banco de Dados
├─────────────────────────────┤
│     Utils / Validators      │  ← CPF/CNPJ, Segurança
└─────────────────────────────┘
```

#### Scala (Akka HTTP) - Alternativa

```
┌─────────────────────────────┐
│     Controllers             │  ← Akka HTTP Routes
├─────────────────────────────┤
│     Services                │  ← Business Logic
├─────────────────────────────┤
│     Repositories            │  ← Data Access (Slick)
├─────────────────────────────┤
│     Models                  │  ← Case Classes
└─────────────────────────────┘
```

## 🚀 Setup do Ambiente

### Pré-requisitos

```bash
# Obrigatórios
- Docker & Docker Compose
- Git
- Make (Linux/macOS) ou equivalente (Windows)

# Para desenvolvimento Python
- Python 3.11+
- pip

# Para desenvolvimento Scala (opcional)
- Java 11+
- SBT (Scala Build Tool)
```

### Setup Inicial

```bash
# 1. Clonar repositório
git clone <repository-url>
cd brain-agriculture

# 2. Setup automático
make setup

# 3. Iniciar ambiente de desenvolvimento
make dev

# 4. Verificar se está funcionando
make check-health
```

### Configuração Manual (Python)

```bash
# 1. Entrar no diretório Python
cd api_python

# 2. Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env  # se existir
```

### Configuração Manual (Scala)

```bash
# 1. Entrar no diretório Scala
cd api_scala

# 2. Compilar projeto
sbt compile

# 3. Executar testes
sbt test
```

## 🛠️ Workflow de Desenvolvimento

### Desenvolvimento Diário

```bash
# 1. Atualizar código
git pull origin main

# 2. Iniciar ambiente
make dev

# 3. Fazer alterações no código
# ... desenvolvimento ...

# 4. Executar testes
make test-python-real

# 5. Verificar cobertura
make test-complete-coverage

# 6. Commit e push
git add .
git commit -m "feat: nova funcionalidade"
git push
```

### Adicionando Nova Funcionalidade

#### Python (Recomendado)

1. **Controller** (`api_python/app/controllers/`)
```python
# exemplo: new_controller.py
from fastapi import APIRouter, Depends
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/new-entity", tags=["new-entity"])

@router.post("/")
async def create_entity(data: EntitySchema, user = Depends(get_current_user)):
    # implementação
    pass
```

2. **Service** (`api_python/app/services/`)
```python
# exemplo: new_service.py
class NewEntityService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_entity(self, data: EntitySchema) -> Entity:
        # lógica de negócio
        pass
```

3. **Model** (`api_python/app/models/`)
```python
# exemplo: new_model.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class NewEntity(Base):
    __tablename__ = "new_entities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
```

4. **Schema** (`api_python/app/schemas.py`)
```python
from pydantic import BaseModel

class EntitySchema(BaseModel):
    name: str
    
class EntityResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
```

5. **Testes** (`api_python/tests/`)
```python
# exemplo: test_new_entity.py
def test_create_entity(client, admin_token):
    response = client.post("/api/new-entity/", 
                          json={"name": "Test"}, 
                          headers={"Authorization": admin_token})
    assert response.status_code == 201
```

#### Scala (Alternativo)

1. **Controller** (`api_scala/src/main/scala/controllers/`)
2. **Service** (`api_scala/src/main/scala/services/`)
3. **Model** (`api_scala/src/main/scala/models/`)
4. **Repository** (`api_scala/src/main/scala/repositories/`)
5. **Testes** (`api_scala/src/test/scala/`)

## 📋 Padrões e Convenções

### Nomenclatura

#### Python
- **Arquivos**: `snake_case.py`
- **Classes**: `PascalCase`
- **Funções/Métodos**: `snake_case`
- **Constantes**: `UPPER_CASE`
- **Variáveis**: `snake_case`

#### Scala
- **Arquivos**: `PascalCase.scala`
- **Classes**: `PascalCase`
- **Objetos**: `PascalCase`
- **Métodos**: `camelCase`
- **Variáveis**: `camelCase`

### Estrutura de Commits

```bash
# Padrão: tipo(escopo): descrição
feat(producer): adiciona validação de CPF
fix(auth): corrige geração de token JWT
docs(api): atualiza documentação da API
test(crud): adiciona testes de integração
refactor(models): simplifica modelo de fazenda
```

**Tipos de commit**:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `test`: Testes
- `refactor`: Refatoração
- `perf`: Performance
- `chore`: Tarefas gerais

### Regras de Validação

#### CPF/CNPJ (Obrigatório)
```python
# Python
from app.utils.validators import validate_cpf, validate_cnpj

# Scala  
import utils.DocumentValidator.{validateCPF, validateCNPJ}
```

#### Áreas de Fazenda (Obrigatório)
```python
# agricultural_area + vegetation_area <= total_area
if (agricultural_area + vegetation_area) > total_area:
    raise ValueError("Área agrícola + vegetação não pode exceder área total")
```

### Tratamento de Erros

#### Python
```python
from fastapi import HTTPException, status

# Erro 404
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Produtor não encontrado"
)

# Erro 400
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="CPF inválido"
)
```

#### Scala
```scala
import akka.http.scaladsl.model.StatusCodes
import akka.http.scaladsl.server.Directives._

// Erro 404
complete(StatusCodes.NotFound -> "Produtor não encontrado")

// Erro 400
complete(StatusCodes.BadRequest -> "CPF inválido")
```

## 🧪 Estratégia de Testes

### Pirâmide de Testes

```
        /\
       /  \
      / UI \          ← Testes E2E (poucos)
     /______\
    /        \
   / INTEGRA  \       ← Testes de Integração
  /_____ÇÃO___\
 /            \
/ TESTES       \      ← Testes Unitários (maioria)
\   UNITÁRIOS  /
 \____________/
```

### Tipos de Testes Implementados

1. **Testes Unitários** (`api_python/tests/unit/`)
   - Validadores CPF/CNPJ
   - Funções utilitárias
   - Lógica de negócio isolada

2. **Testes de Integração** (`api_python/tests/integration/`)
   - Endpoints da API
   - Integração com banco
   - Fluxos completos

3. **Testes CRUD Reais** (`api_python/tests/integration/test_real_crud_flow.py`)
   - CREATE → READ → UPDATE → DELETE
   - Dados reais (não fixtures)
   - Limpeza automática

4. **Testes de Cobertura Completa** (`api_python/tests/run_complete_coverage.py`)
   - Todas as 33 rotas testadas
   - 100% cobertura de endpoints

### Executando Testes

```bash
# Testes rápidos (unitários)
make quick-test

# Testes com dados reais
make test-python-real

# Cobertura completa
make test-complete-coverage

# CRUD específico
make test-crud-producer
make test-crud-system

# Relatório HTML
cd api_python && pytest --cov=app --cov-report=html
```

## 📊 Monitoramento e Debug

### Logs da Aplicação

```bash
# Logs Python
make logs-python

# Logs Scala
make logs-scala

# Todos os logs
docker-compose logs -f
```

### Debugging

#### Python
```python
import pdb; pdb.set_trace()  # Breakpoint

# ou usando logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

#### Scala
```scala
// Usando println para debug simples
println(s"Debug: $variavel")

// Usando logging (se configurado)
logger.debug("Debug message")
```

### Health Checks

```bash
# Verificar saúde das APIs
make check-health

# Manualmente
curl http://localhost:8001/health  # Python
curl http://localhost:8080/health  # Scala
```

## 🔒 Segurança

### Autenticação JWT

#### Python
```python
from app.utils.security import create_access_token, verify_token

# Criar token
token = create_access_token(data={"sub": user.username})

# Verificar token
payload = verify_token(token)
```

#### Hash de Senhas
```python
from app.utils.security import get_password_hash, verify_password

# Hash
hashed = get_password_hash("senha123")

# Verificar
is_valid = verify_password("senha123", hashed)
```

### Variáveis de Ambiente

```bash
# api_python/.env
DATABASE_URL=postgresql://user:pass@localhost:5433/brain_agriculture
SECRET_KEY=seu_secret_key_jwt
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🚀 Deploy e CI/CD

### Pipeline Automatizado

O projeto possui CI/CD automático que executa:

1. **Testes Python** - Todos os testes unitários e integração
2. **Testes Scala** - Compilação e testes básicos  
3. **Build Docker** - Construção das imagens
4. **Testes E2E** - Testes end-to-end se configurado

### Deploy Local

```bash
# Deploy completo
make deploy-local

# Apenas produção
make build
docker-compose up -d --build
```

### Deploy Manual

```bash
# 1. Build das imagens
docker-compose build

# 2. Subir serviços  
docker-compose up -d

# 3. Verificar saúde
make check-health
```

## 📈 Performance e Otimização

### Banco de Dados

- **Índices**: Criados automaticamente para FKs
- **Connection Pool**: Configurado no SQLAlchemy
- **Migrations**: Controladas via SQLAlchemy

### Cache (Se necessário)

```python
# Exemplo com Redis (se implementado)
from functools import lru_cache

@lru_cache(maxsize=100)
def get_dashboard_data():
    # dados do dashboard com cache
    pass
```

### Monitoramento de Performance

```bash
# Tempo de resposta das APIs
time curl http://localhost:8001/api/dashboard/summary

# Uso de memória dos containers
docker stats
```

## 🤝 Contribuindo

### Pull Request Process

1. **Fork** do repositório
2. **Branch** feature: `git checkout -b feature/nova-funcionalidade`
3. **Commits** seguindo convenções
4. **Testes** passando: `make test-python-real`
5. **Pull Request** com descrição detalhada

### Checklist de PR

- [ ] Testes passando (`make test-python-real`)
- [ ] Cobertura mantida (`make test-complete-coverage`)
- [ ] Código formatado (se configurado)
- [ ] Documentação atualizada (se necessário)
- [ ] Sem secrets commitados
- [ ] Validações implementadas (CPF/CNPJ/áreas)

### Code Review

Pontos de atenção:

- ✅ **Segurança**: Senhas hasheadas, JWT válido
- ✅ **Validações**: CPF/CNPJ corretos, áreas válidas
- ✅ **Testes**: Cobertura mantida ou aumentada
- ✅ **Performance**: Queries otimizadas
- ✅ **Padrões**: Nomenclatura e estrutura consistentes

## 🆘 Troubleshooting

### Problemas Comuns

**🔴 Porta em uso**
```bash
make clean-all
docker-compose down --volumes
```

**🔴 Banco não conecta**
```bash
# Verificar se PostgreSQL está rodando
docker-compose ps postgres

# Resetar volumes
make clean-all && make dev
```

**🔴 Testes falhando**
```bash
# Verificar dependências
cd api_python && pip install -r requirements.txt

# Limpar cache Python
find . -name "__pycache__" -type d -exec rm -rf {} +
```

**🔴 Import errors Python**
```bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/api_python"

# ou rodar de dentro do diretório
cd api_python && python tests/...
```

### Logs de Debug

```bash
# Logs detalhados
docker-compose logs -f --tail=100 api-python

# Logs de erro específicos
docker-compose logs api-python 2>&1 | grep ERROR
```

## 📚 Recursos Adicionais

### Documentação da API

- **Swagger**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **Health**: http://localhost:8001/health

### Arquivos Importantes

- `README.md` - Documentação principal
- `SCRIPTS.md` - Todos os comandos disponíveis
- `api_python/tests/REAL_CRUD_SUMMARY.md` - Testes CRUD
- `api_python/tests/COVERAGE_SUMMARY.md` - Cobertura de testes
- `CLAUDE.md` - Instruções para Claude Code

### Tecnologias de Referência

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **Pydantic**: https://pydantic-docs.helpmanual.io/
- **Pytest**: https://docs.pytest.org/
- **Akka HTTP**: https://doc.akka.io/docs/akka-http/
- **Scala**: https://docs.scala-lang.org/

---

**Desenvolvido por**: Kayo Carvalho Fernandes  
**Projeto**: Brain Agriculture - Sistema de Produtores Rurais  
**Última atualização**: 25/08/2025