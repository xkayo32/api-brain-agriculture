"""
Testes de integracao dos endpoints de autenticacao
"""
import pytest


class TestAuthEndpoints:
    """Testes dos endpoints de autenticacao"""
    
    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_success(self, client, admin_user):
        """Testa login bem sucedido"""
        response = client.post(
            "/api/auth/login",
            data={"username": "admin_test", "password": "password123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
        
    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_wrong_password(self, client, admin_user):
        """Testa login com senha errada"""
        response = client.post(
            "/api/auth/login",
            data={"username": "admin_test", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_nonexistent_user(self, client):
        """Testa login com usuario inexistente"""
        response = client.post(
            "/api/auth/login",
            data={"username": "nonexistent", "password": "password123"}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_missing_credentials(self, client):
        """Testa login sem credenciais"""
        response = client.post("/api/auth/login", data={})
        
        assert response.status_code == 422  # Unprocessable Entity
        
    @pytest.mark.integration
    @pytest.mark.auth
    def test_get_current_user_with_token(self, client, auth_headers_admin):
        """Testa obtencao de usuario atual com token valido"""
        response = client.get("/api/auth/me", headers=auth_headers_admin)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["username"] == "admin_test"
        assert data["email"] == "admin@test.com"
        assert data["is_active"] == True
        assert data["is_admin"] == True
        assert "id" in data
        
    @pytest.mark.integration
    @pytest.mark.auth
    def test_get_current_user_without_token(self, client):
        """Testa obtencao de usuario atual sem token"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    @pytest.mark.auth
    def test_get_current_user_invalid_token(self, client):
        """Testa obtencao de usuario atual com token invalido"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    @pytest.mark.auth
    def test_protected_endpoint_without_auth(self, client):
        """Testa acesso a endpoint protegido sem autenticacao"""
        response = client.get("/api/producers/")
        
        assert response.status_code == 401
        
    @pytest.mark.integration
    @pytest.mark.auth
    def test_protected_endpoint_with_auth(self, client, auth_headers_admin):
        """Testa acesso a endpoint protegido com autenticacao"""
        response = client.get("/api/producers/", headers=auth_headers_admin)
        
        # Deve retornar 200 (sucesso) ou dados validos
        assert response.status_code == 200
        
    @pytest.mark.integration
    @pytest.mark.auth
    def test_admin_endpoint_with_regular_user(self, client, auth_headers_user):
        """Testa acesso a endpoint admin com usuario comum"""
        # Tentar acessar endpoint que requer admin
        response = client.delete("/api/producers/999", headers=auth_headers_user)
        
        # Deve retornar 403 (forbidden) se houver restricao de admin
        # ou 404 se o recurso nao existir (ambos sao aceitaveis)
        assert response.status_code in [403, 404]
        
    @pytest.mark.integration
    @pytest.mark.auth
    def test_token_refresh_flow(self, client, admin_user):
        """Testa fluxo completo de token"""
        # Login inicial
        response = client.post(
            "/api/auth/login",
            data={"username": "admin_test", "password": "password123"}
        )
        
        assert response.status_code == 200
        token = response.json()["access_token"]
        
        # Usar token para acessar endpoint protegido
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["username"] == "admin_test"