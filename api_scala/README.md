# API Scala - Gerenciamento de Produtores Rurais

API REST desenvolvida em Scala para gerenciar o cadastro de produtores rurais e suas fazendas.

## Tecnologias Utilizadas

- Scala 2.13
- Akka HTTP (Framework web)
- Slick (ORM)
- PostgreSQL (Banco de dados)
- Circe (Serialização JSON)

## Configuração do Ambiente

### Requisitos
- Java 11 ou superior
- SBT 1.9+
- PostgreSQL 15

### Instalação

1. Clone o repositório
2. Configure o banco de dados no arquivo `src/main/resources/application.conf`
3. Execute o projeto:

```bash
sbt run
```

A API estará disponível em `http://localhost:8080`

## Endpoints

### Produtores

- `GET /api/producers` - Lista todos os produtores
- `GET /api/producers/{id}` - Busca produtor por ID
- `POST /api/producers` - Cria novo produtor
- `PUT /api/producers/{id}` - Atualiza produtor
- `DELETE /api/producers/{id}` - Remove produtor

### Fazendas

- `GET /api/farms` - Lista todas as fazendas
- `GET /api/farms?producerId={id}` - Lista fazendas de um produtor
- `GET /api/farms/{id}` - Busca fazenda por ID
- `POST /api/farms` - Cria nova fazenda
- `PUT /api/farms/{id}` - Atualiza fazenda
- `DELETE /api/farms/{id}` - Remove fazenda

### Dashboard

- `GET /api/dashboard/summary` - Resumo geral
- `GET /api/dashboard/by-state` - Distribuição por estado
- `GET /api/dashboard/land-use` - Distribuição de uso do solo

## Executar com Docker

```bash
docker-compose up api-scala
```

## Testes

Para executar os testes:

```bash
sbt test
```

## Estrutura do Projeto

```
src/
├── main/
│   ├── scala/
│   │   ├── controllers/   # Controladores REST
│   │   ├── models/       # Modelos de dados
│   │   ├── repositories/ # Acesso ao banco
│   │   ├── services/     # Regras de negócio
│   │   └── utils/        # Utilitários
│   └── resources/
│       └── application.conf
└── test/
```

## Validações

- CPF e CNPJ são validados automaticamente
- A soma das áreas agricultável e vegetação não pode ultrapassar a área total
- Um produtor pode ter múltiplas fazendas

## Desenvolvedor

Kayo Carvalho Fernandes