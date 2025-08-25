"""
Configuracao dos testes com fixtures
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models.user import User
from app.utils.security import get_password_hash
from main import app

# Banco de dados em memoria para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override da funcao get_db para usar banco de teste"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override da dependencia
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    """Cria event loop para testes async"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db():
    """Fixture do banco de dados de teste"""
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # Limpar tabelas apos cada teste
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    """Cliente de teste da API"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def admin_user(db):
    """Cria um usuario admin para testes"""
    user = User(
        username="admin_test",
        email="admin@test.com",
        hashed_password=get_password_hash("password123"),
        is_active=True,
        is_admin=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def regular_user(db):
    """Cria um usuario comum para testes"""
    user = User(
        username="user_test",
        email="user@test.com",
        hashed_password=get_password_hash("password123"),
        is_active=True,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def admin_token(client, admin_user):
    """Gera token JWT para usuario admin"""
    response = client.post(
        "/api/auth/login",
        data={"username": "admin_test", "password": "password123"}
    )
    token = response.json()["access_token"]
    return f"Bearer {token}"

@pytest.fixture(scope="function")
def user_token(client, regular_user):
    """Gera token JWT para usuario comum"""
    response = client.post(
        "/api/auth/login",
        data={"username": "user_test", "password": "password123"}
    )
    token = response.json()["access_token"]
    return f"Bearer {token}"

@pytest.fixture(scope="function")
def auth_headers_admin(admin_token):
    """Headers de autenticacao para admin"""
    return {"Authorization": admin_token}

@pytest.fixture(scope="function")
def auth_headers_user(user_token):
    """Headers de autenticacao para usuario comum"""
    return {"Authorization": user_token}