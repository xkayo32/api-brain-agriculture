#!/bin/bash

echo "Iniciando sistema de Produtores Rurais..."

# Verificar se Docker esta instalado
if ! command -v docker &> /dev/null; then
    echo "Docker nao encontrado. Por favor instale o Docker primeiro."
    exit 1
fi

# Limpar containers antigos
echo "Parando containers antigos..."
docker-compose down

# Iniciar servicos
echo "Iniciando servicos..."
docker-compose up -d postgres

# Aguardar postgres iniciar
echo "Aguardando PostgreSQL iniciar..."
sleep 5

# Iniciar APIs
echo "Iniciando APIs..."
docker-compose up --build api-python api-scala

echo "Sistema iniciado!"
echo "API Python: http://localhost:8000"
echo "API Scala: http://localhost:8080"