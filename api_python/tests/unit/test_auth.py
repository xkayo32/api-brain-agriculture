"""
Testes unitarios de autenticacao
"""
import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from app.utils.security import (
    verify_password, 
    get_password_hash, 
    authenticate_user, 
    create_access_token,
    get_current_user
)
from app.models.user import User
from datetime import datetime, timedelta


class TestPasswordSecurity:
    """Testes de seguranca de senha"""
    
    @pytest.mark.unit
    def test_password_hash(self):
        """Testa geracao de hash da senha"""
        password = "password123"
        hashed = get_password_hash(password)
        
        # Hash deve ser diferente da senha original
        assert hashed != password
        # Hash deve ter tamanho esperado do bcrypt
        assert len(hashed) > 50
        
    @pytest.mark.unit
    def test_verify_password_correct(self):
        """Testa verificacao de senha correta"""
        password = "password123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) == True
        
    @pytest.mark.unit
    def test_verify_password_incorrect(self):
        """Testa verificacao de senha incorreta"""
        password = "password123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) == False


class TestUserAuthentication:
    """Testes de autenticacao de usuario"""
    
    @pytest.mark.unit
    def test_authenticate_user_success(self, db):
        """Testa autenticacao bem sucedida"""
        # Criar usuario de teste
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password=get_password_hash("password123"),
            is_active=True
        )
        db.add(user)
        db.commit()
        
        # Autenticar
        authenticated_user = authenticate_user(db, "testuser", "password123")
        
        assert authenticated_user is not False
        assert authenticated_user.username == "testuser"
        assert authenticated_user.email == "test@test.com"
        
    @pytest.mark.unit
    def test_authenticate_user_wrong_password(self, db):
        """Testa autenticacao com senha errada"""
        # Criar usuario de teste
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password=get_password_hash("password123"),
            is_active=True
        )
        db.add(user)
        db.commit()
        
        # Tentar autenticar com senha errada
        authenticated_user = authenticate_user(db, "testuser", "wrongpassword")
        
        assert authenticated_user == False
        
    @pytest.mark.unit
    def test_authenticate_user_nonexistent(self, db):
        """Testa autenticacao de usuario inexistente"""
        authenticated_user = authenticate_user(db, "nonexistent", "password123")
        
        assert authenticated_user == False
        
    @pytest.mark.unit
    def test_authenticate_user_inactive(self, db):
        """Testa autenticacao de usuario inativo"""
        # Criar usuario inativo
        user = User(
            username="inactive_user",
            email="inactive@test.com",
            hashed_password=get_password_hash("password123"),
            is_active=False
        )
        db.add(user)
        db.commit()
        
        # Tentar autenticar
        authenticated_user = authenticate_user(db, "inactive_user", "password123")
        
        assert authenticated_user == False


class TestJWTToken:
    """Testes de token JWT"""
    
    @pytest.mark.unit
    def test_create_access_token(self):
        """Testa criacao de token de acesso"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        # Token deve ser uma string nao vazia
        assert isinstance(token, str)
        assert len(token) > 0
        # Token JWT tem 3 partes separadas por ponto
        assert len(token.split('.')) == 3
        
    @pytest.mark.unit
    def test_create_access_token_with_expires(self):
        """Testa criacao de token com expiracao customizada"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=5)
        token = create_access_token(data, expires_delta)
        
        assert isinstance(token, str)
        assert len(token) > 0
        assert len(token.split('.')) == 3
        
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_current_user_valid_token(self, db):
        """Testa obtencao de usuario com token valido"""
        # Criar usuario de teste
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password=get_password_hash("password123"),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Criar token valido
        token = create_access_token({"sub": "testuser"})
        
        # Obter usuario atual
        current_user = await get_current_user(token, db)
        
        assert current_user.username == "testuser"
        assert current_user.email == "test@test.com"
        
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self, db):
        """Testa obtencao de usuario com token invalido"""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(invalid_token, db)
            
        assert exc_info.value.status_code == 401
        
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_current_user_nonexistent_user(self, db):
        """Testa obtencao de usuario inexistente com token valido"""
        # Criar token para usuario que nao existe no banco
        token = create_access_token({"sub": "nonexistent_user"})
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token, db)
            
        assert exc_info.value.status_code == 401
        
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_current_user_inactive_user(self, db):
        """Testa obtencao de usuario inativo"""
        # Criar usuario inativo
        user = User(
            username="inactive_user",
            email="inactive@test.com",
            hashed_password=get_password_hash("password123"),
            is_active=False
        )
        db.add(user)
        db.commit()
        
        # Criar token valido
        token = create_access_token({"sub": "inactive_user"})
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token, db)
            
        assert exc_info.value.status_code == 400