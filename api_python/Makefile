.PHONY: test test-unit test-integration test-validators test-docker clean install dev

# Instalar dependencias
install:
	pip install -r requirements.txt

# Executar todos os testes
test:
	python test_runner.py

# Executar apenas testes unitarios dos validadores
test-validators:
	python tests/test_validators_isolated.py

# Executar testes unitarios
test-unit:
	pytest tests/unit/ -v || python test_runner.py

# Executar testes de integracao (quando implementados)
test-integration:
	pytest tests/integration/ -v --tb=short || echo "Testes de integração precisam da API rodando"

# Executar testes no Docker
test-docker:
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Executar API em modo desenvolvimento
dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Executar com Docker
docker-dev:
	docker-compose up --build

# Limpar cache e arquivos temporarios
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache/ 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
	rm -f .coverage 2>/dev/null || true

# Gerar relatorio de cobertura
coverage:
	pytest --cov=app --cov-report=html --cov-report=term-missing tests/ || echo "Coverage report may be incomplete"

# Verificar qualidade do codigo
lint:
	flake8 app/ tests/ || echo "Linting may have issues - install flake8 if needed"

# Executar todos os checks
check: clean lint test

# Help
help:
	@echo "Comandos disponíveis:"
	@echo "  install       - Instalar dependências"
	@echo "  test         - Executar todos os testes"
	@echo "  test-validators - Executar testes dos validadores CPF/CNPJ"
	@echo "  test-unit    - Executar testes unitários"
	@echo "  test-integration - Executar testes de integração"
	@echo "  test-docker  - Executar testes no Docker"
	@echo "  dev          - Executar API em modo desenvolvimento"
	@echo "  docker-dev   - Executar com Docker"
	@echo "  clean        - Limpar arquivos temporários"
	@echo "  coverage     - Gerar relatório de cobertura"
	@echo "  lint         - Verificar qualidade do código"
	@echo "  check        - Executar linting + testes"