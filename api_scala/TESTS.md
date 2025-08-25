# Sistema de Testes - API Scala Brain Agriculture

## Visão Geral

O sistema Scala possui um conjunto abrangente de testes usando ScalaTest para garantir a qualidade e funcionalidade da API.

## Estrutura de Testes

```
src/test/scala/
├── utils/
│   └── DocumentValidatorSpec.scala    # Testes dos validadores CPF/CNPJ
├── services/
│   └── AuthServiceSpec.scala          # Testes de autenticação e JWT
├── models/
│   ├── ProducerSpec.scala             # Testes do modelo Producer
│   └── FarmSpec.scala                 # Testes do modelo Farm
├── TestRunner.scala                   # Sistema de testes customizado
└── resources/
    └── application.conf               # Configuração para testes
```

## Executando os Testes

### Opção 1: Sistema de Testes Customizado (Recomendado)
```bash
make test-custom
# ou
sbt "runMain TestRunner"
```

### Opção 2: ScalaTest Padrão
```bash
make test
# ou  
sbt test
```

### Opção 3: Testes Específicos
```bash
make test-validators    # Apenas validadores
make test-models       # Apenas modelos  
make test-services     # Apenas serviços
```

### Opção 4: Testes Individuais
```bash
sbt "testOnly utils.DocumentValidatorSpec"
sbt "testOnly models.ProducerSpec"
sbt "testOnly models.FarmSpec"
sbt "testOnly services.AuthServiceSpec"
```

## Tipos de Testes Implementados

### 1. Testes de Validadores (DocumentValidatorSpec)
- **Validação de CPF**: Algoritmo brasileiro, formatação, casos inválidos
- **Validação de CNPJ**: Algoritmo brasileiro, formatação, casos inválidos  
- **Validação Genérica**: Detecção automática CPF/CNPJ
- **Formatação**: Formatação para exibição com máscaras

### 2. Testes de Autenticação (AuthServiceSpec)
- **Hash de Senhas**: BCrypt com salt automático
- **Verificação de Senhas**: Comparação segura de hashes
- **Tokens JWT**: Geração, validação e expiração
- **Segurança**: Testes de tokens inválidos e malformados

### 3. Testes de Modelos (ProducerSpec, FarmSpec)
- **Producer**: Validação de dados, áreas, documentos
- **Farm**: Culturas, áreas, relacionamento com produtor
- **Integridade**: Soma de áreas, consistência de dados
- **Casos Extremos**: Áreas zero, múltiplas culturas, estados brasileiros

### 4. Sistema de Testes Customizado (TestRunner)
- **Execução Isolada**: Testes sem dependências externas
- **Validação Rápida**: Verificações essenciais do sistema
- **Relatórios**: Output claro e detalhado dos resultados

## Configuração do Ambiente de Testes

### Database de Testes
- **H2 In-Memory**: Banco rápido para testes unitários
- **Isolamento**: Cada teste roda com banco limpo
- **Configuração**: `src/test/resources/application.conf`

### Dependencies de Teste (build.sbt)
```scala
"org.scalatest" %% "scalatest" % "3.2.17" % Test
"com.typesafe.akka" %% "akka-http-testkit" % akkaHttpVersion % Test
"com.typesafe.akka" %% "akka-actor-testkit-typed" % akkaVersion % Test
```

## Cobertura de Testes

### Funcionalidades Testadas ✅
- ✅ Validação de CPF e CNPJ (algoritmos brasileiros)
- ✅ Hash e verificação de senhas com BCrypt  
- ✅ Geração e validação de tokens JWT
- ✅ Modelos de domínio (Producer, Farm, Crop)
- ✅ Formatação de documentos brasileiros
- ✅ Validações de áreas e relacionamentos
- ✅ Enum de culturas agrícolas
- ✅ Estados brasileiros válidos

### Funcionalidades Preparadas para Testes
- 📋 Testes de Controllers (estrutura criada)
- 📋 Testes de Repositories (aguardando implementação)  
- 📋 Testes de Integração com Akka HTTP
- 📋 Testes de Performance

## Exemplo de Output dos Testes

```
SISTEMA DE TESTES DA API BRAIN AGRICULTURE - SCALA
=======================================================
=== EXECUTANDO TESTES DOS VALIDADORES ===
OK: Testes de validação CPF passaram
OK: Testes de validação CNPJ passaram
OK: Testes de formatação passaram
Todos os testes de validadores passaram!

=== EXECUTANDO TESTES DE SEGURANÇA ===
OK: Hash de senha funcionando
OK: Verificação de senha funcionando
OK: Geração de token JWT funcionando
OK: Validação de token JWT funcionando
OK: Rejeição de token inválido funcionando
Todos os testes de segurança passaram!

=== EXECUTANDO TESTES BÁSICOS DE MODELOS ===
OK: Modelo Producer funcionando
OK: Modelo Farm funcionando
OK: Enum Crop funcionando
Todos os testes básicos de modelos passaram!
```

## Comandos Makefile Disponíveis

```bash
make test-custom      # Sistema de testes customizado
make test            # ScalaTest padrão
make test-validators # Apenas validadores  
make test-models     # Apenas modelos
make test-services   # Apenas serviços
make test-coverage   # Testes com cobertura
make check           # Limpar + compilar + testar
```

## ScalaTest Features Utilizadas

- **FlatSpec**: Estilo de testes descritivos e legíveis
- **Matchers**: Assertions expressivas (`should`, `shouldBe`)
- **ScalaFutures**: Testes assíncronos quando necessário
- **Test Fixtures**: Setup e teardown de dados de teste

## Casos de Teste Especiais

### Validadores CPF/CNPJ
- Documentos com formatação (pontos, hífens, barras)
- Documentos com todos os dígitos iguais (inválidos)
- Documentos com tamanho incorreto
- Caracteres não numéricos

### Modelos de Negócio
- Produtores com áreas zeradas
- Fazendas sem culturas plantadas
- Relacionamentos entre Producer e Farm
- Validação de estados brasileiros
- Combinações de culturas por região

### Segurança
- Passwords com diferentes níveis de complexidade
- Tokens expirados (preparado para implementação)
- Ataques de força bruta simulados
- Validação de characters especiais em tokens

## Próximos Passos

1. **Testes de Integração**: Controllers + Database
2. **Testes de Performance**: JMeter ou Gatling
3. **Testes de Contrato**: API compliance
4. **Pipeline CI/CD**: GitHub Actions para Scala
5. **Code Coverage**: Relatórios detalhados com Scoverage

---
**Sistema desenvolvido para Brain Agriculture Tech Challenge**
**Arquitetura: Scala + Akka HTTP + Slick + PostgreSQL**