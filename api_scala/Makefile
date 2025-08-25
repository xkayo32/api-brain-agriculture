.PHONY: compile test test-unit test-integration clean run package docker help

# Compilar o projeto
compile:
	sbt compile

# Executar todos os testes
test:
	sbt test

# Executar teste customizado
test-custom:
	sbt "runMain TestRunner"

# Executar apenas testes unitarios
test-unit:
	sbt "testOnly *Spec"

# Executar testes de validadores
test-validators:
	sbt "testOnly utils.DocumentValidatorSpec"

# Executar testes de modelos
test-models:
	sbt "testOnly models.*"

# Executar testes de servicos
test-services:
	sbt "testOnly services.*"

# Executar aplicacao
run:
	sbt run

# Executar aplicacao com recarga automatica
dev:
	sbt ~run

# Executar com Docker
docker-run:
	docker-compose -f ../docker-compose.yml up scala-api --build

# Limpar arquivos compilados
clean:
	sbt clean
	rm -rf target/
	rm -rf project/target/

# Gerar package
package:
	sbt assembly

# Executar testes com cobertura
test-coverage:
	sbt clean coverage test coverageReport

# Verificar estilo de codigo (se scalastyle estiver configurado)
lint:
	sbt scalastyle || echo "Scalastyle não configurado"

# Executar todos os checks
check: clean compile test

# Executar aplicacao em modo de producao
prod:
	sbt "runMain Main" -Dconfig.resource=application.prod.conf

# Verificar dependencias
deps:
	sbt dependencyTree

# Console interativo Scala
console:
	sbt console

# Help - mostrar comandos disponiveis
help:
	@echo "Comandos disponíveis:"
	@echo "  compile       - Compilar o projeto Scala"
	@echo "  test          - Executar todos os testes com SBT"
	@echo "  test-custom   - Executar sistema de testes customizado"
	@echo "  test-unit     - Executar apenas testes unitários"
	@echo "  test-validators - Executar testes dos validadores"
	@echo "  test-models   - Executar testes dos modelos"
	@echo "  test-services - Executar testes dos serviços"
	@echo "  run           - Executar aplicação"
	@echo "  dev           - Executar com recarga automática"
	@echo "  docker-run    - Executar com Docker"
	@echo "  clean         - Limpar arquivos compilados"
	@echo "  package       - Gerar package da aplicação"
	@echo "  test-coverage - Executar testes com relatório de cobertura"
	@echo "  lint          - Verificar estilo de código"
	@echo "  check         - Limpar + compilar + testar"
	@echo "  prod          - Executar em modo produção"
	@echo "  deps          - Verificar árvore de dependências"
	@echo "  console       - Console interativo Scala"