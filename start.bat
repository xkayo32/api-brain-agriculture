@echo off

echo Iniciando sistema de Produtores Rurais...

REM Verificar se Docker esta instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker nao encontrado. Por favor instale o Docker primeiro.
    exit /b 1
)

REM Limpar containers antigos
echo Parando containers antigos...
docker-compose down

REM Iniciar servicos
echo Iniciando servicos...
docker-compose up -d postgres

REM Aguardar postgres iniciar
echo Aguardando PostgreSQL iniciar...
timeout /t 5 /nobreak >nul

REM Iniciar APIs
echo Iniciando APIs...
docker-compose up --build api-python api-scala

echo Sistema iniciado!
echo API Python: http://localhost:8000
echo API Scala: http://localhost:8080