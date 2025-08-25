"""
Testes de integração com dados reais do banco PostgreSQL
Estes testes rodam contra o banco real com dados populados pelo seed_data.py
"""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Usar banco real para estes testes
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ruraluser:ruralpass@localhost:5433/rural_producers_db")

@pytest.fixture(scope="module")
def real_db_client():
    """Cliente que conecta ao banco real com dados populados"""
    from main import app
    
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def admin_token_real(real_db_client):
    """Token de admin do banco real"""
    response = real_db_client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin123"}
    )
    if response.status_code == 200:
        return f"Bearer {response.json()['access_token']}"
    return None

@pytest.mark.integration
@pytest.mark.real_data
class TestRealDataIntegration:
    """Testes com dados reais populados pelo seed_data.py"""
    
    def test_list_real_producers(self, real_db_client, admin_token_real):
        """Testa listagem de produtores reais do banco"""
        if not admin_token_real:
            pytest.skip("Admin user not available in real database")
            
        response = real_db_client.get(
            "/api/producers/",
            headers={"Authorization": admin_token_real}
        )
        
        assert response.status_code == 200
        producers = response.json()
        
        # Verificar que temos os produtores do seed_data
        assert len(producers) >= 6
        
        # Verificar produtores especificos
        producer_names = [p["name"] for p in producers]
        expected_names = [
            "João Silva Santos",
            "Maria Oliveira Costa", 
            "Fazendas Reunidas Ltda",
            "Pedro Almeida Ferreira",
            "Agropecuária Brasil S/A",
            "Cooperativa Agrícola Central"
        ]
        
        for name in expected_names:
            assert name in producer_names, f"Produtor {name} não encontrado"
    
    def test_real_dashboard_summary(self, real_db_client):
        """Testa dashboard com dados reais"""
        response = real_db_client.get("/api/dashboard/summary")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar valores esperados do seed_data
        assert data["total_farms"] == 11
        assert data["total_area"] == 36900.0
    
    def test_real_dashboard_by_state(self, real_db_client):
        """Testa distribuição por estado com dados reais"""
        response = real_db_client.get("/api/dashboard/by-state")
        
        assert response.status_code == 200
        states = response.json()
        
        # Converter para dict para facilitar verificação
        state_dict = {s["state"]: s["count"] for s in states}
        
        # Verificar estados esperados do seed_data
        expected_distribution = {
            "SP": 4,  # 4 fazendas em SP
            "GO": 2,  # 2 fazendas em GO
            "MT": 2,  # 2 fazendas em MT
            "MS": 2,  # 2 fazendas em MS
            "MG": 1   # 1 fazenda em MG
        }
        
        for state, count in expected_distribution.items():
            assert state_dict.get(state) == count, f"Estado {state} deveria ter {count} fazendas"
    
    def test_real_dashboard_by_crop(self, real_db_client):
        """Testa distribuição por cultura com dados reais"""
        response = real_db_client.get("/api/dashboard/by-crop")
        
        assert response.status_code == 200
        crops = response.json()
        
        # Converter para dict
        crop_dict = {c["crop_type"]: c["total_area"] for c in crops}
        
        # Verificar culturas esperadas
        expected_crops = {
            "SOJA": 22150.0,
            "MILHO": 7300.0,
            "ALGODAO": 5200.0,
            "CAFE": 650.0,
            "CANA_DE_ACUCAR": 1150.0
        }
        
        for crop, area in expected_crops.items():
            assert crop_dict.get(crop) == area, f"Cultura {crop} deveria ter {area} hectares"
    
    def test_real_producer_details(self, real_db_client, admin_token_real):
        """Testa detalhes de um produtor específico com suas fazendas"""
        if not admin_token_real:
            pytest.skip("Admin user not available in real database")
            
        # Primeiro pegar lista de produtores
        response = real_db_client.get(
            "/api/producers/",
            headers={"Authorization": admin_token_real}
        )
        
        assert response.status_code == 200
        producers = response.json()
        
        # Pegar o primeiro produtor (João Silva Santos)
        joao = next((p for p in producers if p["name"] == "João Silva Santos"), None)
        assert joao is not None
        
        # Buscar detalhes deste produtor
        response = real_db_client.get(
            f"/api/producers/{joao['id']}",
            headers={"Authorization": admin_token_real}
        )
        
        assert response.status_code == 200
        producer_detail = response.json()
        
        assert producer_detail["name"] == "João Silva Santos"
        assert producer_detail["document"] == "11144477735"
    
    def test_real_farms_list(self, real_db_client, admin_token_real):
        """Testa listagem de fazendas reais"""
        if not admin_token_real:
            pytest.skip("Admin user not available in real database")
            
        response = real_db_client.get(
            "/api/farms/",
            headers={"Authorization": admin_token_real}
        )
        
        assert response.status_code == 200
        farms = response.json()
        
        # Verificar quantidade de fazendas
        assert len(farms) == 11
        
        # Verificar fazendas específicas
        farm_names = [f["name"] for f in farms]
        expected_farms = [
            "Fazenda Santa Rita",
            "Sítio Boa Vista",
            "Fazenda Esperança",
            "Complexo Agropecuário Vale Verde",
            "Fazenda União",
            "Rancho Dois Irmãos",
            "Fazenda Continental",
            "Fazenda Primavera",
            "Fazenda Cooperada Norte",
            "Fazenda Cooperada Sul",
            "Fazenda Nova Era"
        ]
        
        for farm in expected_farms:
            assert farm in farm_names, f"Fazenda {farm} não encontrada"
    
    def test_real_land_use_distribution(self, real_db_client):
        """Testa distribuição de uso da terra com dados reais"""
        response = real_db_client.get("/api/dashboard/land-use")
        
        assert response.status_code == 200
        land_use = response.json()
        
        # Valores esperados calculados do seed_data
        assert land_use["agricultural_area"] == 30950.0
        assert land_use["vegetation_area"] == 5950.0
        
        # Verificar percentuais
        assert 83 < land_use["agricultural_percentage"] < 84
        assert 16 < land_use["vegetation_percentage"] < 17
    
    def test_create_new_producer_real_db(self, real_db_client, admin_token_real):
        """Testa criação de novo produtor no banco real"""
        if not admin_token_real:
            pytest.skip("Admin user not available in real database")
            
        new_producer = {
            "document": "11122233344",  # CPF válido
            "name": "Teste Integração Real"
        }
        
        response = real_db_client.post(
            "/api/producers/",
            json=new_producer,
            headers={"Authorization": admin_token_real}
        )
        
        assert response.status_code == 201
        created = response.json()
        
        assert created["name"] == new_producer["name"]
        assert created["document"] == new_producer["document"]
        assert "id" in created
        
        # Limpar - deletar o produtor criado
        delete_response = real_db_client.delete(
            f"/api/producers/{created['id']}",
            headers={"Authorization": admin_token_real}
        )
        assert delete_response.status_code == 204
    
    def test_auth_endpoints_real_db(self, real_db_client):
        """Testa endpoints de autenticação com banco real"""
        # Teste de login com credenciais corretas
        response = real_db_client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "admin123"}
        )
        
        assert response.status_code == 200
        token_data = response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        
        # Teste do endpoint /me
        token = f"Bearer {token_data['access_token']}"
        response = real_db_client.get(
            "/api/auth/me",
            headers={"Authorization": token}
        )
        
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["username"] == "admin"
        assert user_data["email"] == "admin@brazilagro.com"
        assert user_data["is_admin"] == True
        
        # Teste de login com credenciais incorretas
        response = real_db_client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "wrong_password"}
        )
        
        assert response.status_code == 401
    
    def test_complete_flow_with_real_data(self, real_db_client, admin_token_real):
        """Teste completo: criar produtor, fazenda, listar e deletar"""
        if not admin_token_real:
            pytest.skip("Admin user not available in real database")
            
        headers = {"Authorization": admin_token_real}
        
        # 1. Criar novo produtor
        producer_data = {
            "document": "44455566677",
            "name": "Produtor Teste Completo"
        }
        
        producer_response = real_db_client.post(
            "/api/producers/",
            json=producer_data,
            headers=headers
        )
        assert producer_response.status_code == 201
        producer = producer_response.json()
        
        # 2. Criar fazenda para este produtor
        farm_data = {
            "producer_id": producer["id"],
            "name": "Fazenda Teste Completo",
            "city": "Teste City",
            "state": "TS",
            "total_area": 100.0,
            "agricultural_area": 70.0,
            "vegetation_area": 30.0
        }
        
        farm_response = real_db_client.post(
            "/api/farms/",
            json=farm_data,
            headers=headers
        )
        assert farm_response.status_code == 201
        farm = farm_response.json()
        
        # 3. Verificar que aparecem nas listagens
        producers_list = real_db_client.get("/api/producers/", headers=headers).json()
        farms_list = real_db_client.get("/api/farms/", headers=headers).json()
        
        assert any(p["id"] == producer["id"] for p in producers_list)
        assert any(f["id"] == farm["id"] for f in farms_list)
        
        # 4. Verificar dashboard atualizado
        summary = real_db_client.get("/api/dashboard/summary").json()
        assert summary["total_farms"] == 12  # 11 originais + 1 nova
        assert summary["total_area"] == 37000.0  # 36900 + 100
        
        # 5. Limpar - deletar fazenda e produtor
        real_db_client.delete(f"/api/farms/{farm['id']}", headers=headers)
        real_db_client.delete(f"/api/producers/{producer['id']}", headers=headers)
        
        # 6. Verificar que voltou ao normal
        summary_after = real_db_client.get("/api/dashboard/summary").json()
        assert summary_after["total_farms"] == 11
        assert summary_after["total_area"] == 36900.0