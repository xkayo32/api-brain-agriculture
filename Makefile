.PHONY: help test test-python test-scala build-ci run-ci clean-ci deploy-local check-health

# Ajuda - mostra todos os comandos disponíveis
help:
	@echo "🚀 Brain Agriculture - Comandos Disponíveis"
	@echo "=========================================="
	@echo ""
	@echo "📋 TESTES:"
	@echo "  test                    - Executar todos os testes (Python + Scala)"
	@echo "  test-python             - Executar apenas testes Python (com mock)"
	@echo "  test-python-real        - Testes Python com dados reais (PostgreSQL)"
	@echo "  test-python-coverage    - Testes Python com relatório de cobertura"
	@echo "  test-complete-coverage  - Cobertura completa de TODAS as rotas"
	@echo "  test-real-crud          - Testes CRUD reais (CREATE→UPDATE→DELETE)"
	@echo "  test-crud-producer      - Teste CRUD específico de produtores"
	@echo "  test-crud-system        - Teste de fluxo completo do sistema"
	@echo "  test-scala              - Executar apenas testes Scala"
	@echo "  test-global             - Executar sistema de testes global"
	@echo ""
	@echo "🐳 CI/CD e DOCKER:"
	@echo "  build-ci          - Build imagens para CI/CD"
	@echo "  run-ci            - Executar pipeline completo de CI"
	@echo "  clean-ci          - Limpar containers e volumes de CI"
	@echo ""
	@echo "🌐 DESENVOLVIMENTO:"
	@echo "  dev               - Executar APIs em modo desenvolvimento"
	@echo "  build             - Build das APIs de produção"
	@echo "  deploy-local      - Deploy local completo"
	@echo ""
	@echo "🔍 HEALTH CHECKS:"
	@echo "  check-health      - Verificar saúde das APIs"
	@echo "  logs-python       - Ver logs da API Python"
	@echo "  logs-scala        - Ver logs da API Scala"

# Executar todos os testes
test:
	@echo "🧪 Executando todos os testes..."
	@$(MAKE) test-python
	@$(MAKE) test-scala
	@$(MAKE) test-global

# Executar testes Python
test-python:
	@echo "🐍 Executando testes Python..."
	@cd api_python && python test_runner.py

# Executar testes Python com dados reais
test-python-real:
	@echo "🔍 Executando testes Python com dados reais do PostgreSQL..."
	@cd api_python && python tests/run_real_tests.py --real-only

# Executar todos os testes Python (mock + real)
test-python-all:
	@echo "🧪 Executando todos os testes Python (mock + real)..."
	@cd api_python && python tests/run_real_tests.py --all

# Executar testes Python com relatório de cobertura
test-python-coverage:
	@echo "📊 Executando testes Python com cobertura..."
	@cd api_python && pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html
	@echo "📈 Relatório HTML disponível em: api_python/htmlcov/index.html"

# Executar testes de cobertura completa de TODAS as rotas
test-complete-coverage:
	@echo "🎯 Executando testes de cobertura completa (TODAS as rotas)..."
	@cd api_python && python tests/run_complete_coverage.py --report

# Executar testes de CRUD real (criar, atualizar, deletar registros reais)
test-real-crud:
	@echo "🔄 Executando testes de CRUD real (CREATE → UPDATE → DELETE)..."
	@cd api_python && python tests/run_real_crud.py

# Executar teste específico de CRUD
test-crud-producer:
	@echo "👨‍🌾 Testando CRUD de produtores..."
	@cd api_python && python tests/run_real_crud.py --test producer

test-crud-farm:
	@echo "🏡 Testando CRUD de fazendas..."
	@cd api_python && python tests/run_real_crud.py --test farm

test-crud-system:
	@echo "🚀 Testando fluxo completo do sistema..."
	@cd api_python && python tests/run_real_crud.py --test system

# Executar testes Scala
test-scala:
	@echo "⚡ Executando testes Scala..."
	@cd api_scala && sbt compile
	@cd api_scala && sbt "runMain TestRunner" || echo "Testes Scala podem precisar de SBT instalado"

# Executar sistema de testes global
test-global:
	@echo "🌍 Executando sistema de testes global..."
	@python test_runner_global.py

# Build para CI/CD
build-ci:
	@echo "🏗️ Fazendo build das imagens para CI..."
	@docker-compose -f docker-compose.ci.yml build

# Executar pipeline de CI completo
run-ci:
	@echo "🚀 Executando pipeline de CI/CD..."
	@docker-compose -f docker-compose.ci.yml up --build --abort-on-container-exit
	@$(MAKE) clean-ci

# Limpar containers e volumes de CI
clean-ci:
	@echo "🧹 Limpando ambiente de CI..."
	@docker-compose -f docker-compose.ci.yml down --volumes --remove-orphans

# Executar em modo desenvolvimento
dev:
	@echo "🔧 Iniciando modo desenvolvimento..."
	@docker-compose up --build

# Build das APIs de produção
build:
	@echo "🏭 Fazendo build de produção..."
	@docker-compose build

# Deploy local completo
deploy-local:
	@echo "🌐 Executando deploy local..."
	@docker-compose up -d --build
	@sleep 10
	@$(MAKE) check-health

# Verificar saúde das APIs
check-health:
	@echo "🩺 Verificando saúde das APIs..."
	@echo "Python API (porta 8000):"
	@curl -f http://localhost:8000/docs -s > /dev/null && echo "✅ Python API OK" || echo "❌ Python API indisponível"
	@echo "Scala API (porta 8080):"
	@curl -f http://localhost:8080/health -s > /dev/null && echo "✅ Scala API OK" || echo "❌ Scala API indisponível"

# Ver logs da API Python
logs-python:
	@docker-compose logs -f brain-api-python

# Ver logs da API Scala
logs-scala:
	@docker-compose logs -f brain-api-scala

# Comandos para CI (usado pelo GitHub Actions)
ci-python:
	@echo "🤖 CI: Testando Python..."
	@cd api_python && python tests/test_validators_isolated.py
	@cd api_python && python test_runner.py

ci-scala:
	@echo "🤖 CI: Testando Scala..."
	@cd api_scala && sbt compile
	@cd api_scala && sbt "runMain TestRunner"

ci-integration:
	@echo "🤖 CI: Testes de integração..."
	@python test_runner_global.py

# Limpar tudo
clean-all:
	@echo "🧹 Limpando tudo..."
	@docker-compose down --volumes --remove-orphans
	@docker-compose -f docker-compose.ci.yml down --volumes --remove-orphans
	@docker system prune -f
	@cd api_python && find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@cd api_scala && sbt clean || true

# Setup inicial do projeto
setup:
	@echo "⚙️ Configurando projeto inicial..."
	@cd api_python && pip install -r requirements.txt
	@echo "Python dependencies installed ✅"
	@echo "Para Scala, certifique-se de ter SBT instalado"
	@echo "Setup concluído! Use 'make help' para ver comandos"

# Comandos rápidos para desenvolvimento
quick-test:
	@echo "⚡ Testes rápidos..."
	@cd api_python && python tests/test_validators_isolated.py

# Status dos serviços
status:
	@echo "📊 Status dos serviços:"
	@docker-compose ps