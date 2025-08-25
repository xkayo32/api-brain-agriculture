# API Python - Gerenciamento de Produtores Rurais

API REST desenvolvida em Python para gerenciar o cadastro de produtores rurais e suas fazendas com autenticação JWT.

## Tecnologias Utilizadas

- Python 3.11
- FastAPI (Framework web)
- SQLAlchemy (ORM)  
- PostgreSQL (Banco de dados)
- Pydantic (Validação de dados)
- JWT (Autenticação)
- BCrypt (Hash de senhas)

## Configuração do Ambiente

### Requisitos
- Python 3.11 ou superior
- PostgreSQL 15

### Instalação

1. Clone o repositório
2. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (copie o .env.example para .env)

5. Execute o projeto:

```bash
python main.py
```

A API estará disponível em `http://localhost:8000`

## Documentação Interativa e Autenticação

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Usuário Administrador Padrão

Ao iniciar pela primeira vez, um usuário admin é criado automaticamente:

- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@brazilagro.com`

### Como usar a autenticação no Swagger:

1. Acesse `http://localhost:8000/docs`
2. Faça login em `/api/auth/login` com as credenciais acima
3. Copie o `access_token` retornado
4. Clique no botão **"Authorize"** 🔒 no topo da página
5. Cole o token no formato: `Bearer {seu_token_aqui}`
6. Agora você pode acessar todas as rotas protegidas!

## Endpoints

### Autenticação 🔐

- `POST /api/auth/register` - Registrar novo usuário
- `POST /api/auth/login` - Login (retorna JWT token)
- `GET /api/auth/me` - Informações do usuário logado
- `GET /api/auth/users` - Listar todos usuários (apenas admin)

### Produtores 🚜 (Requer autenticação)

- `GET /api/producers` - Lista todos os produtores
- `GET /api/producers/{id}` - Busca produtor por ID
- `POST /api/producers` - Cria novo produtor
- `PUT /api/producers/{id}` - Atualiza produtor
- `DELETE /api/producers/{id}` - Remove produtor

### Fazendas 🏞️ (Requer autenticação)

- `GET /api/farms` - Lista todas as fazendas
- `GET /api/farms?producer_id={id}` - Lista fazendas de um produtor
- `GET /api/farms/{id}` - Busca fazenda por ID
- `POST /api/farms` - Cria nova fazenda
- `PUT /api/farms/{id}` - Atualiza fazenda
- `DELETE /api/farms/{id}` - Remove fazenda

### Dashboard 📊 (Requer autenticação)

- `GET /api/dashboard/summary` - Resumo geral
- `GET /api/dashboard/by-state` - Distribuição por estado
- `GET /api/dashboard/land-use` - Distribuição de uso do solo
- `GET /api/dashboard/by-crop` - Distribuição por cultura

## Executar com Docker

```bash
docker-compose up api-python
```

## Testes

Para executar os testes:

```bash
pytest
```

## Estrutura do Projeto

```
app/
├── controllers/   # Rotas e endpoints
├── models/       # Modelos do banco de dados
├── services/     # Lógica de negócio
├── utils/        # Validadores e utilitários
├── schemas.py    # Schemas Pydantic
├── database.py   # Configuração do banco
└── config.py     # Configurações
```

## Dados de Exemplo

Ao iniciar pela primeira vez, além do usuário admin, são criados automaticamente:

### Produtores de Exemplo:
- **João Silva Santos** (CPF: 111.444.777-35)
  - Fazenda Santa Rita (Ribeirão Preto/SP) - 1000ha
  - Sítio Boa Vista (Franca/SP) - 500ha
- **Maria Oliveira Costa** (CPF: 987.654.321-00)
  - Fazenda Esperança (Uberaba/MG) - 2000ha
- **Fazendas Reunidas Ltda** (CNPJ: 11.222.333/0001-91)
  - Complexo Vale Verde (Campo Grande/MS) - 5000ha

## Validações e Regras de Negócio

- ✅ CPF e CNPJ validados automaticamente com dígitos verificadores
- ✅ A soma das áreas agricultável e vegetação não pode ultrapassar a área total
- ✅ Autenticação JWT obrigatória para todas as rotas (exceto auth)
- ✅ Primeiro usuário automaticamente vira administrador
- ✅ Todas as áreas devem ser valores positivos
- ✅ Relacionamentos: Um produtor → Múltiplas fazendas → Múltiplas safras → Múltiplas culturas

## Culturas Suportadas

- 🌱 Soja (SOY)
- 🌽 Milho (CORN)
- 🌿 Algodão (COTTON)
- ☕ Café (COFFEE)  
- 🎋 Cana de Açúcar (SUGARCANE)

## Segurança

- 🔒 Senhas criptografadas com BCrypt
- 🎫 Tokens JWT com expiração de 30 minutos
- 👥 Sistema de permissões (admin vs usuário comum)
- 🛡️ Todas as rotas protegidas por autenticação

## Desenvolvedor

Kayo Carvalho Fernandes