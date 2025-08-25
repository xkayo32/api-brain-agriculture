# 🚀 Quick Start - API de Produtores Rurais

## Inicialização Rápida (5 minutos)

### 1. 🐳 Iniciar com Docker
```bash
docker-compose up -d postgres api-python
```

### 2. 🌐 Acessar a API
- **Swagger UI:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### 3. 🔐 Login Automático
Usuário admin já criado:
- **Username:** `admin`
- **Password:** `admin123`

### 4. 🎯 Testar no Swagger

1. **Login:**
   - Vá para `/api/auth/login`
   - Use as credenciais acima
   - Copie o `access_token`

2. **Autorizar:**
   - Clique em **"Authorize"** 🔒 no topo
   - Cole: `Bearer {access_token}`
   - Clique "Authorize"

3. **Usar a API:**
   - Todas as rotas agora funcionam!
   - Crie produtores, fazendas, veja dashboard

### 5. 📊 Dados Disponíveis

- ✅ 1 usuário admin
- ✅ Produtores e fazendas de exemplo
- ✅ Dashboard com estatísticas
- ✅ Validação CPF/CNPJ
- ✅ Todas as funcionalidades JWT

### 6. 🛠️ Comandos Úteis

```bash
# Ver logs
docker-compose logs -f api-python

# Parar tudo
docker-compose down

# Resetar banco (limpar tudo)
docker-compose down -v

# Rebuild
docker-compose up --build -d
```

## 🎉 Pronto!
A API está 100% funcional com autenticação JWT e dados de exemplo!

Acesse: **http://localhost:8000/docs** 🚀