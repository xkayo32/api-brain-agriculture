"""
Testes de integracao dos endpoints de produtores
"""
import pytest


class TestProducerEndpoints:
    """Testes dos endpoints de produtores rurais"""
    
    @pytest.mark.integration
    def test_create_producer_success(self, client, auth_headers_admin):
        """Testa criacao bem sucedida de produtor"""
        producer_data = {
            "name": "João Silva",
            "cpf_cnpj": "12345678909",
            "total_area": 1000.0,
            "agricultural_area": 600.0,
            "vegetation_area": 400.0,
            "city": "São Paulo",
            "state": "SP"
        }
        
        response = client.post(
            "/api/producers/",
            json=producer_data,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["name"] == producer_data["name"]
        assert data["cpf_cnpj"] == producer_data["cpf_cnpj"]
        assert data["total_area"] == producer_data["total_area"]
        assert data["city"] == producer_data["city"]
        assert "id" in data
        
    @pytest.mark.integration
    def test_create_producer_invalid_cpf(self, client, auth_headers_admin):
        """Testa criacao de produtor com CPF invalido"""
        producer_data = {
            "name": "João Silva",
            "cpf_cnpj": "12345678901",  # CPF invalido
            "total_area": 1000.0,
            "agricultural_area": 600.0,
            "vegetation_area": 400.0,
            "city": "São Paulo",
            "state": "SP"
        }
        
        response = client.post(
            "/api/producers/",
            json=producer_data,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    def test_create_producer_invalid_areas(self, client, auth_headers_admin):
        """Testa criacao de produtor com areas invalidas"""
        producer_data = {
            "name": "João Silva",
            "cpf_cnpj": "12345678909",
            "total_area": 1000.0,
            "agricultural_area": 700.0,
            "vegetation_area": 400.0,  # Soma das areas maior que total
            "city": "São Paulo",
            "state": "SP"
        }
        
        response = client.post(
            "/api/producers/",
            json=producer_data,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    def test_list_producers_empty(self, client, auth_headers_admin):
        """Testa listagem de produtores vazia"""
        response = client.get("/api/producers/", headers=auth_headers_admin)
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        
    @pytest.mark.integration
    def test_list_producers_with_data(self, client, auth_headers_admin):
        """Testa listagem de produtores com dados"""
        # Primeiro criar um produtor
        producer_data = {
            "name": "Maria Santos",
            "cpf_cnpj": "98765432100",
            "total_area": 500.0,
            "agricultural_area": 300.0,
            "vegetation_area": 200.0,
            "city": "Rio de Janeiro",
            "state": "RJ"
        }
        
        create_response = client.post(
            "/api/producers/",
            json=producer_data,
            headers=auth_headers_admin
        )
        assert create_response.status_code == 201
        
        # Listar produtores
        response = client.get("/api/producers/", headers=auth_headers_admin)
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Verificar se o produtor criado esta na lista
        producer_found = False
        for producer in data:
            if producer["name"] == "Maria Santos":
                producer_found = True
                break
        assert producer_found
        
    @pytest.mark.integration
    def test_get_producer_by_id(self, client, auth_headers_admin):
        """Testa obtencao de produtor por ID"""
        # Criar produtor primeiro
        producer_data = {
            "name": "Carlos Oliveira",
            "cpf_cnpj": "11144477735",
            "total_area": 800.0,
            "agricultural_area": 500.0,
            "vegetation_area": 300.0,
            "city": "Belo Horizonte",
            "state": "MG"
        }
        
        create_response = client.post(
            "/api/producers/",
            json=producer_data,
            headers=auth_headers_admin
        )
        assert create_response.status_code == 201
        created_producer = create_response.json()
        producer_id = created_producer["id"]
        
        # Obter produtor por ID
        response = client.get(f"/api/producers/{producer_id}", headers=auth_headers_admin)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == producer_id
        assert data["name"] == producer_data["name"]
        assert data["cpf_cnpj"] == producer_data["cpf_cnpj"]
        
    @pytest.mark.integration
    def test_get_producer_not_found(self, client, auth_headers_admin):
        """Testa obtencao de produtor inexistente"""
        response = client.get("/api/producers/9999", headers=auth_headers_admin)
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        
    @pytest.mark.integration
    def test_update_producer(self, client, auth_headers_admin):
        """Testa atualizacao de produtor"""
        # Criar produtor primeiro
        producer_data = {
            "name": "Ana Costa",
            "cpf_cnpj": "12345678909",
            "total_area": 600.0,
            "agricultural_area": 400.0,
            "vegetation_area": 200.0,
            "city": "Salvador",
            "state": "BA"
        }
        
        create_response = client.post(
            "/api/producers/",
            json=producer_data,
            headers=auth_headers_admin
        )
        assert create_response.status_code == 201
        created_producer = create_response.json()
        producer_id = created_producer["id"]
        
        # Atualizar produtor
        update_data = {
            "name": "Ana Costa Silva",
            "cpf_cnpj": "12345678909",
            "total_area": 700.0,
            "agricultural_area": 450.0,
            "vegetation_area": 250.0,
            "city": "Salvador",
            "state": "BA"
        }
        
        response = client.put(
            f"/api/producers/{producer_id}",
            json=update_data,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == update_data["name"]
        assert data["total_area"] == update_data["total_area"]
        assert data["agricultural_area"] == update_data["agricultural_area"]
        
    @pytest.mark.integration
    def test_delete_producer(self, client, auth_headers_admin):
        """Testa exclusao de produtor"""
        # Criar produtor primeiro
        producer_data = {
            "name": "Pedro Alves",
            "cpf_cnpj": "98765432100",
            "total_area": 400.0,
            "agricultural_area": 250.0,
            "vegetation_area": 150.0,
            "city": "Fortaleza",
            "state": "CE"
        }
        
        create_response = client.post(
            "/api/producers/",
            json=producer_data,
            headers=auth_headers_admin
        )
        assert create_response.status_code == 201
        created_producer = create_response.json()
        producer_id = created_producer["id"]
        
        # Deletar produtor
        response = client.delete(f"/api/producers/{producer_id}", headers=auth_headers_admin)
        
        assert response.status_code == 200
        
        # Verificar se foi deletado
        get_response = client.get(f"/api/producers/{producer_id}", headers=auth_headers_admin)
        assert get_response.status_code == 404
        
    @pytest.mark.integration
    def test_create_producer_duplicate_cpf(self, client, auth_headers_admin):
        """Testa criacao de produtor com CPF duplicado"""
        producer_data_1 = {
            "name": "Primeiro Produtor",
            "cpf_cnpj": "12345678909",
            "total_area": 500.0,
            "agricultural_area": 300.0,
            "vegetation_area": 200.0,
            "city": "São Paulo",
            "state": "SP"
        }
        
        # Criar primeiro produtor
        response1 = client.post(
            "/api/producers/",
            json=producer_data_1,
            headers=auth_headers_admin
        )
        assert response1.status_code == 201
        
        # Tentar criar segundo produtor com mesmo CPF
        producer_data_2 = {
            "name": "Segundo Produtor",
            "cpf_cnpj": "12345678909",  # CPF duplicado
            "total_area": 600.0,
            "agricultural_area": 400.0,
            "vegetation_area": 200.0,
            "city": "Rio de Janeiro",
            "state": "RJ"
        }
        
        response2 = client.post(
            "/api/producers/",
            json=producer_data_2,
            headers=auth_headers_admin
        )
        
        assert response2.status_code == 400
        data = response2.json()
        assert "detail" in data