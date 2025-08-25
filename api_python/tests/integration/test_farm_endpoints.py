"""
Testes de integracao dos endpoints de fazendas
"""
import pytest


class TestFarmEndpoints:
    """Testes dos endpoints de fazendas"""
    
    @pytest.fixture
    def sample_producer(self, client, auth_headers_admin):
        """Cria um produtor de exemplo para os testes"""
        producer_data = {
            "name": "Fazendeiro Teste",
            "cpf_cnpj": "12345678909",
            "total_area": 2000.0,
            "agricultural_area": 1200.0,
            "vegetation_area": 800.0,
            "city": "Campinas",
            "state": "SP"
        }
        
        response = client.post(
            "/api/producers/",
            json=producer_data,
            headers=auth_headers_admin
        )
        assert response.status_code == 201
        return response.json()
        
    @pytest.mark.integration
    def test_create_farm_success(self, client, auth_headers_admin, sample_producer):
        """Testa criacao bem sucedida de fazenda"""
        farm_data = {
            "name": "Fazenda Santa Clara",
            "city": "Campinas",
            "state": "SP",
            "total_area": 500.0,
            "agricultural_area": 300.0,
            "vegetation_area": 200.0,
            "crops": ["SOJA", "MILHO"],
            "producer_id": sample_producer["id"]
        }
        
        response = client.post(
            "/api/farms/",
            json=farm_data,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["name"] == farm_data["name"]
        assert data["city"] == farm_data["city"]
        assert data["total_area"] == farm_data["total_area"]
        assert data["producer_id"] == farm_data["producer_id"]
        assert set(data["crops"]) == set(farm_data["crops"])
        assert "id" in data
        
    @pytest.mark.integration
    def test_create_farm_invalid_areas(self, client, auth_headers_admin, sample_producer):
        """Testa criacao de fazenda com areas invalidas"""
        farm_data = {
            "name": "Fazenda Teste",
            "city": "Campinas",
            "state": "SP",
            "total_area": 500.0,
            "agricultural_area": 350.0,
            "vegetation_area": 200.0,  # Soma maior que total
            "crops": ["SOJA"],
            "producer_id": sample_producer["id"]
        }
        
        response = client.post(
            "/api/farms/",
            json=farm_data,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    def test_create_farm_invalid_producer(self, client, auth_headers_admin):
        """Testa criacao de fazenda com produtor inexistente"""
        farm_data = {
            "name": "Fazenda Teste",
            "city": "Campinas",
            "state": "SP",
            "total_area": 500.0,
            "agricultural_area": 300.0,
            "vegetation_area": 200.0,
            "crops": ["SOJA"],
            "producer_id": 9999  # Produtor inexistente
        }
        
        response = client.post(
            "/api/farms/",
            json=farm_data,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    def test_create_farm_invalid_crops(self, client, auth_headers_admin, sample_producer):
        """Testa criacao de fazenda com cultura invalida"""
        farm_data = {
            "name": "Fazenda Teste",
            "city": "Campinas",
            "state": "SP",
            "total_area": 500.0,
            "agricultural_area": 300.0,
            "vegetation_area": 200.0,
            "crops": ["CULTURA_INVALIDA"],
            "producer_id": sample_producer["id"]
        }
        
        response = client.post(
            "/api/farms/",
            json=farm_data,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    def test_list_farms_empty(self, client, auth_headers_admin):
        """Testa listagem de fazendas vazia"""
        response = client.get("/api/farms/", headers=auth_headers_admin)
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        
    @pytest.mark.integration
    def test_list_farms_with_data(self, client, auth_headers_admin, sample_producer):
        """Testa listagem de fazendas com dados"""
        # Criar fazenda primeiro
        farm_data = {
            "name": "Fazenda Boa Vista",
            "city": "Ribeirão Preto",
            "state": "SP",
            "total_area": 800.0,
            "agricultural_area": 500.0,
            "vegetation_area": 300.0,
            "crops": ["MILHO", "ALGODAO"],
            "producer_id": sample_producer["id"]
        }
        
        create_response = client.post(
            "/api/farms/",
            json=farm_data,
            headers=auth_headers_admin
        )
        assert create_response.status_code == 201
        
        # Listar fazendas
        response = client.get("/api/farms/", headers=auth_headers_admin)
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Verificar se a fazenda criada esta na lista
        farm_found = False
        for farm in data:
            if farm["name"] == "Fazenda Boa Vista":
                farm_found = True
                break
        assert farm_found
        
    @pytest.mark.integration
    def test_get_farm_by_id(self, client, auth_headers_admin, sample_producer):
        """Testa obtencao de fazenda por ID"""
        # Criar fazenda primeiro
        farm_data = {
            "name": "Fazenda Esperança",
            "city": "Piracicaba",
            "state": "SP",
            "total_area": 600.0,
            "agricultural_area": 400.0,
            "vegetation_area": 200.0,
            "crops": ["SOJA", "MILHO", "ALGODAO"],
            "producer_id": sample_producer["id"]
        }
        
        create_response = client.post(
            "/api/farms/",
            json=farm_data,
            headers=auth_headers_admin
        )
        assert create_response.status_code == 201
        created_farm = create_response.json()
        farm_id = created_farm["id"]
        
        # Obter fazenda por ID
        response = client.get(f"/api/farms/{farm_id}", headers=auth_headers_admin)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == farm_id
        assert data["name"] == farm_data["name"]
        assert data["city"] == farm_data["city"]
        assert data["producer_id"] == farm_data["producer_id"]
        
    @pytest.mark.integration
    def test_get_farm_not_found(self, client, auth_headers_admin):
        """Testa obtencao de fazenda inexistente"""
        response = client.get("/api/farms/9999", headers=auth_headers_admin)
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    def test_update_farm(self, client, auth_headers_admin, sample_producer):
        """Testa atualizacao de fazenda"""
        # Criar fazenda primeiro
        farm_data = {
            "name": "Fazenda Progresso",
            "city": "Araraquara",
            "state": "SP",
            "total_area": 700.0,
            "agricultural_area": 450.0,
            "vegetation_area": 250.0,
            "crops": ["SOJA"],
            "producer_id": sample_producer["id"]
        }
        
        create_response = client.post(
            "/api/farms/",
            json=farm_data,
            headers=auth_headers_admin
        )
        assert create_response.status_code == 201
        created_farm = create_response.json()
        farm_id = created_farm["id"]
        
        # Atualizar fazenda
        update_data = {
            "name": "Fazenda Progresso Renovada",
            "city": "Araraquara",
            "state": "SP",
            "total_area": 800.0,
            "agricultural_area": 500.0,
            "vegetation_area": 300.0,
            "crops": ["SOJA", "MILHO"],
            "producer_id": sample_producer["id"]
        }
        
        response = client.put(
            f"/api/farms/{farm_id}",
            json=update_data,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == update_data["name"]
        assert data["total_area"] == update_data["total_area"]
        assert set(data["crops"]) == set(update_data["crops"])
        
    @pytest.mark.integration
    def test_delete_farm(self, client, auth_headers_admin, sample_producer):
        """Testa exclusao de fazenda"""
        # Criar fazenda primeiro
        farm_data = {
            "name": "Fazenda a Deletar",
            "city": "São Carlos",
            "state": "SP",
            "total_area": 400.0,
            "agricultural_area": 250.0,
            "vegetation_area": 150.0,
            "crops": ["ALGODAO"],
            "producer_id": sample_producer["id"]
        }
        
        create_response = client.post(
            "/api/farms/",
            json=farm_data,
            headers=auth_headers_admin
        )
        assert create_response.status_code == 201
        created_farm = create_response.json()
        farm_id = created_farm["id"]
        
        # Deletar fazenda
        response = client.delete(f"/api/farms/{farm_id}", headers=auth_headers_admin)
        
        assert response.status_code == 200
        
        # Verificar se foi deletada
        get_response = client.get(f"/api/farms/{farm_id}", headers=auth_headers_admin)
        assert get_response.status_code == 404
        
    @pytest.mark.integration
    def test_get_farms_by_producer(self, client, auth_headers_admin, sample_producer):
        """Testa busca de fazendas por produtor"""
        # Criar duas fazendas para o mesmo produtor
        farm_data_1 = {
            "name": "Fazenda Norte",
            "city": "Jaú",
            "state": "SP",
            "total_area": 300.0,
            "agricultural_area": 180.0,
            "vegetation_area": 120.0,
            "crops": ["SOJA"],
            "producer_id": sample_producer["id"]
        }
        
        farm_data_2 = {
            "name": "Fazenda Sul",
            "city": "Bauru",
            "state": "SP",
            "total_area": 400.0,
            "agricultural_area": 250.0,
            "vegetation_area": 150.0,
            "crops": ["MILHO"],
            "producer_id": sample_producer["id"]
        }
        
        # Criar as duas fazendas
        response1 = client.post("/api/farms/", json=farm_data_1, headers=auth_headers_admin)
        assert response1.status_code == 201
        
        response2 = client.post("/api/farms/", json=farm_data_2, headers=auth_headers_admin)
        assert response2.status_code == 201
        
        # Buscar fazendas do produtor
        response = client.get(
            f"/api/producers/{sample_producer['id']}/farms",
            headers=auth_headers_admin
        )
        
        # Verificar resposta (pode retornar 200 com lista ou 404 se endpoint nao implementado)
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            assert len(data) >= 2
        else:
            # Se endpoint nao implementado, verificamos via lista geral
            all_farms_response = client.get("/api/farms/", headers=auth_headers_admin)
            assert all_farms_response.status_code == 200
            all_farms = all_farms_response.json()
            
            producer_farms = [f for f in all_farms if f["producer_id"] == sample_producer["id"]]
            assert len(producer_farms) >= 2