"""
Testes de fluxo CRUD real - Criar, Atualizar e Deletar registros reais
Os testes não usam fixtures pré-criadas, mas fazem o ciclo completo
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.models.user import User
from app.utils.security import get_password_hash
from main import app

# Banco de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_real_crud.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def setup_database():
    """Setup do banco de teste"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(setup_database):
    """Cliente de teste"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def admin_token(client):
    """Cria admin real e retorna token"""
    # Limpar usuários existentes
    db = TestingSessionLocal()
    db.query(User).delete()
    db.commit()
    
    # Criar usuário admin real
    admin = User(
        username="admin_real",
        email="admin@real.com",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_admin=True
    )
    db.add(admin)
    db.commit()
    db.close()
    
    # Fazer login real
    response = client.post(
        "/api/auth/login",
        data={"username": "admin_real", "password": "admin123"}
    )
    assert response.status_code == 200
    return f"Bearer {response.json()['access_token']}"


class TestRealProducerCRUD:
    """Testes de CRUD real de produtores - sem fixtures, ciclo completo"""
    
    def test_complete_producer_lifecycle(self, client, admin_token):
        """Teste do ciclo completo: CREATE → READ → UPDATE → DELETE"""
        headers = {"Authorization": admin_token}
        
        # 🟢 STEP 1: CREATE - Criar produtor real
        print("\n🟢 CRIANDO produtor...")
        create_data = {
            "document": "11144477735",  # CPF válido
            "name": "João Silva Santos - Teste Real"
        }
        
        create_response = client.post(
            "/api/producers/",
            json=create_data,
            headers=headers
        )
        
        assert create_response.status_code == 201
        producer = create_response.json()
        producer_id = producer["id"]
        
        print(f"✅ Produtor criado com ID: {producer_id}")
        assert producer["name"] == create_data["name"]
        assert producer["document"] == create_data["document"]
        assert "created_at" in producer
        assert "updated_at" in producer
        
        # 🔵 STEP 2: READ - Verificar se foi criado corretamente
        print(f"\n🔵 LENDO produtor {producer_id}...")
        read_response = client.get(f"/api/producers/{producer_id}", headers=headers)
        
        assert read_response.status_code == 200
        read_producer = read_response.json()
        
        print(f"✅ Produtor lido: {read_producer['name']}")
        assert read_producer["id"] == producer_id
        assert read_producer["name"] == create_data["name"]
        
        # 🟡 STEP 3: UPDATE - Atualizar dados do produtor
        print(f"\n🟡 ATUALIZANDO produtor {producer_id}...")
        update_data = {
            "document": "11144477735",  # Mesmo CPF
            "name": "João Silva Santos - ATUALIZADO"
        }
        
        update_response = client.put(
            f"/api/producers/{producer_id}",
            json=update_data,
            headers=headers
        )
        
        assert update_response.status_code == 200
        updated_producer = update_response.json()
        
        print(f"✅ Produtor atualizado: {updated_producer['name']}")
        assert updated_producer["id"] == producer_id
        assert updated_producer["name"] == update_data["name"]
        assert "ATUALIZADO" in updated_producer["name"]
        
        # 🔵 STEP 4: READ após UPDATE - Verificar se foi atualizado
        print(f"\n🔵 VERIFICANDO atualização do produtor {producer_id}...")
        verify_response = client.get(f"/api/producers/{producer_id}", headers=headers)
        
        assert verify_response.status_code == 200
        verify_producer = verify_response.json()
        
        print(f"✅ Atualização verificada: {verify_producer['name']}")
        assert "ATUALIZADO" in verify_producer["name"]
        
        # 🔴 STEP 5: DELETE - Deletar o produtor
        print(f"\n🔴 DELETANDO produtor {producer_id}...")
        delete_response = client.delete(f"/api/producers/{producer_id}", headers=headers)
        
        assert delete_response.status_code == 204
        print(f"✅ Produtor {producer_id} deletado")
        
        # 🔵 STEP 6: Verificar se foi deletado (deve dar 404)
        print(f"\n🔵 VERIFICANDO deleção do produtor {producer_id}...")
        check_delete_response = client.get(f"/api/producers/{producer_id}", headers=headers)
        
        assert check_delete_response.status_code == 404
        print(f"✅ Confirmado: Produtor {producer_id} não existe mais")
        
        print(f"\n🎉 CICLO COMPLETO REALIZADO COM SUCESSO!")
        print(f"   CREATE ✅ → READ ✅ → UPDATE ✅ → READ ✅ → DELETE ✅ → VERIFY ✅")


class TestRealFarmCRUD:
    """Testes de CRUD real de fazendas"""
    
    def test_complete_farm_lifecycle(self, client, admin_token):
        """Teste do ciclo completo de fazenda: CREATE → UPDATE → DELETE"""
        headers = {"Authorization": admin_token}
        
        # Primeiro criar um produtor para a fazenda
        producer_data = {
            "document": "98765432100",
            "name": "Maria Oliveira - Produtora de Teste"
        }
        producer_response = client.post("/api/producers/", json=producer_data, headers=headers)
        assert producer_response.status_code == 201
        producer_id = producer_response.json()["id"]
        
        # 🟢 CREATE Fazenda
        print("\n🟢 CRIANDO fazenda...")
        farm_data = {
            "producer_id": producer_id,
            "name": "Fazenda Teste Real",
            "city": "São Paulo",
            "state": "SP",
            "total_area": 1000.0,
            "agricultural_area": 700.0,
            "vegetation_area": 300.0
        }
        
        create_response = client.post("/api/farms/", json=farm_data, headers=headers)
        assert create_response.status_code == 201
        farm = create_response.json()
        farm_id = farm["id"]
        
        print(f"✅ Fazenda criada com ID: {farm_id}")
        
        # 🟡 UPDATE Fazenda
        print(f"\n🟡 ATUALIZANDO fazenda {farm_id}...")
        update_data = {
            "name": "Fazenda Teste Real - ATUALIZADA",
            "city": "São Paulo",
            "state": "SP",
            "total_area": 1200.0,
            "agricultural_area": 800.0,
            "vegetation_area": 400.0
        }
        
        update_response = client.put(f"/api/farms/{farm_id}", json=update_data, headers=headers)
        assert update_response.status_code == 200
        updated_farm = update_response.json()
        
        print(f"✅ Fazenda atualizada: {updated_farm['name']}")
        assert "ATUALIZADA" in updated_farm["name"]
        assert updated_farm["total_area"] == 1200.0
        
        # 🔴 DELETE Fazenda
        print(f"\n🔴 DELETANDO fazenda {farm_id}...")
        delete_response = client.delete(f"/api/farms/{farm_id}", headers=headers)
        assert delete_response.status_code == 204
        
        # Verificar se foi deletada
        check_response = client.get(f"/api/farms/{farm_id}", headers=headers)
        assert check_response.status_code == 404
        
        print(f"✅ Fazenda {farm_id} deletada com sucesso")
        
        # Limpar - deletar o produtor também
        client.delete(f"/api/producers/{producer_id}", headers=headers)
        
        print(f"\n🎉 CICLO COMPLETO DE FAZENDA REALIZADO!")


class TestRealHarvestCRUD:
    """Testes de CRUD real de safras"""
    
    def test_complete_harvest_lifecycle(self, client, admin_token):
        """Teste do ciclo completo de safra: CREATE → UPDATE → DELETE"""
        headers = {"Authorization": admin_token}
        
        # Criar produtor e fazenda para a safra
        producer_data = {"document": "12345678909", "name": "Pedro Almeida"}
        producer_response = client.post("/api/producers/", json=producer_data, headers=headers)
        producer_id = producer_response.json()["id"]
        
        farm_data = {
            "producer_id": producer_id,
            "name": "Fazenda Pedro",
            "city": "Ribeirão Preto",
            "state": "SP",
            "total_area": 500.0,
            "agricultural_area": 350.0,
            "vegetation_area": 150.0
        }
        farm_response = client.post("/api/farms/", json=farm_data, headers=headers)
        farm_id = farm_response.json()["id"]
        
        # 🟢 CREATE Safra
        print("\n🟢 CRIANDO safra...")
        harvest_data = {
            "farm_id": farm_id,
            "year": 2024,
            "description": "Safra 2024 - Teste Real"
        }
        
        create_response = client.post("/api/harvests/", json=harvest_data, headers=headers)
        assert create_response.status_code == 201
        harvest = create_response.json()
        harvest_id = harvest["id"]
        
        print(f"✅ Safra criada com ID: {harvest_id}")
        assert harvest["year"] == 2024
        assert "Teste Real" in harvest["description"]
        
        # 🔵 READ Safra
        read_response = client.get(f"/api/harvests/{harvest_id}", headers=headers)
        assert read_response.status_code == 200
        
        # 🔴 DELETE Safra
        print(f"\n🔴 DELETANDO safra {harvest_id}...")
        delete_response = client.delete(f"/api/harvests/{harvest_id}", headers=headers)
        assert delete_response.status_code == 204
        
        # Verificar deleção
        check_response = client.get(f"/api/harvests/{harvest_id}", headers=headers)
        assert check_response.status_code == 404
        
        print(f"✅ Safra {harvest_id} deletada com sucesso")
        
        # Limpar
        client.delete(f"/api/farms/{farm_id}", headers=headers)
        client.delete(f"/api/producers/{producer_id}", headers=headers)
        
        print(f"\n🎉 CICLO COMPLETO DE SAFRA REALIZADO!")


class TestRealCropCRUD:
    """Testes de CRUD real de culturas"""
    
    def test_complete_crop_lifecycle(self, client, admin_token):
        """Teste do ciclo completo de cultura: CREATE → READ → DELETE"""
        headers = {"Authorization": admin_token}
        
        # Criar estrutura completa: produtor → fazenda → safra
        producer_data = {"document": "52734865806", "name": "Ana Costa"}
        producer_response = client.post("/api/producers/", json=producer_data, headers=headers)
        producer_id = producer_response.json()["id"]
        
        farm_data = {
            "producer_id": producer_id,
            "name": "Fazenda Ana",
            "city": "Campinas",
            "state": "SP",
            "total_area": 300.0,
            "agricultural_area": 200.0,
            "vegetation_area": 100.0
        }
        farm_response = client.post("/api/farms/", json=farm_data, headers=headers)
        farm_id = farm_response.json()["id"]
        
        harvest_data = {
            "farm_id": farm_id,
            "year": 2024,
            "description": "Safra 2024"
        }
        harvest_response = client.post("/api/harvests/", json=harvest_data, headers=headers)
        harvest_id = harvest_response.json()["id"]
        
        # 🟢 CREATE Cultura
        print("\n🟢 CRIANDO cultura...")
        crop_data = {
            "harvest_id": harvest_id,
            "crop_type": "SOJA",
            "planted_area": 150.0
        }
        
        create_response = client.post("/api/crops/", json=crop_data, headers=headers)
        assert create_response.status_code == 201
        crop = create_response.json()
        crop_id = crop["id"]
        
        print(f"✅ Cultura criada com ID: {crop_id}")
        assert crop["crop_type"] == "SOJA"
        assert crop["planted_area"] == 150.0
        
        # 🔵 READ Cultura
        read_response = client.get(f"/api/crops/{crop_id}", headers=headers)
        assert read_response.status_code == 200
        
        # 🔴 DELETE Cultura
        print(f"\n🔴 DELETANDO cultura {crop_id}...")
        delete_response = client.delete(f"/api/crops/{crop_id}", headers=headers)
        assert delete_response.status_code == 204
        
        # Verificar deleção
        check_response = client.get(f"/api/crops/{crop_id}", headers=headers)
        assert check_response.status_code == 404
        
        print(f"✅ Cultura {crop_id} deletada com sucesso")
        
        # Limpar tudo
        client.delete(f"/api/harvests/{harvest_id}", headers=headers)
        client.delete(f"/api/farms/{farm_id}", headers=headers)
        client.delete(f"/api/producers/{producer_id}", headers=headers)
        
        print(f"\n🎉 CICLO COMPLETO DE CULTURA REALIZADO!")


class TestCompleteSystemFlow:
    """Teste do fluxo completo do sistema inteiro"""
    
    def test_complete_system_lifecycle(self, client, admin_token):
        """Teste mega completo: Produtor → Fazenda → Safra → Cultura → Limpar tudo"""
        headers = {"Authorization": admin_token}
        
        print("\n" + "="*60)
        print("🚀 INICIANDO TESTE DE FLUXO COMPLETO DO SISTEMA")
        print("="*60)
        
        # 1. Criar Produtor
        producer_data = {"document": "11144477777", "name": "Sistema Completo Ltda"}
        producer_response = client.post("/api/producers/", json=producer_data, headers=headers)
        assert producer_response.status_code == 201
        producer_id = producer_response.json()["id"]
        print(f"1️⃣ ✅ Produtor criado: ID {producer_id}")
        
        # 2. Criar Fazenda
        farm_data = {
            "producer_id": producer_id,
            "name": "Fazenda Sistema Completo",
            "city": "Teste City",
            "state": "TC",
            "total_area": 2000.0,
            "agricultural_area": 1500.0,
            "vegetation_area": 500.0
        }
        farm_response = client.post("/api/farms/", json=farm_data, headers=headers)
        assert farm_response.status_code == 201
        farm_id = farm_response.json()["id"]
        print(f"2️⃣ ✅ Fazenda criada: ID {farm_id}")
        
        # 3. Criar Safra
        harvest_data = {
            "farm_id": farm_id,
            "year": 2024,
            "description": "Safra Sistema Completo 2024"
        }
        harvest_response = client.post("/api/harvests/", json=harvest_data, headers=headers)
        assert harvest_response.status_code == 201
        harvest_id = harvest_response.json()["id"]
        print(f"3️⃣ ✅ Safra criada: ID {harvest_id}")
        
        # 4. Criar Culturas
        crops_data = [
            {"harvest_id": harvest_id, "crop_type": "SOJA", "planted_area": 800.0},
            {"harvest_id": harvest_id, "crop_type": "MILHO", "planted_area": 700.0}
        ]
        
        crop_ids = []
        for i, crop_data in enumerate(crops_data, 1):
            crop_response = client.post("/api/crops/", json=crop_data, headers=headers)
            assert crop_response.status_code == 201
            crop_id = crop_response.json()["id"]
            crop_ids.append(crop_id)
            print(f"4️⃣.{i} ✅ Cultura {crop_data['crop_type']} criada: ID {crop_id}")
        
        # 5. Verificar que tudo existe
        print(f"\n5️⃣ 🔍 VERIFICANDO se tudo foi criado...")
        
        # Verificar produtor
        prod_check = client.get(f"/api/producers/{producer_id}", headers=headers)
        assert prod_check.status_code == 200
        print(f"   ✅ Produtor {producer_id} existe")
        
        # Verificar fazenda  
        farm_check = client.get(f"/api/farms/{farm_id}", headers=headers)
        assert farm_check.status_code == 200
        print(f"   ✅ Fazenda {farm_id} existe")
        
        # Verificar safra
        harvest_check = client.get(f"/api/harvests/{harvest_id}", headers=headers)
        assert harvest_check.status_code == 200
        print(f"   ✅ Safra {harvest_id} existe")
        
        # Verificar culturas
        for crop_id in crop_ids:
            crop_check = client.get(f"/api/crops/{crop_id}", headers=headers)
            assert crop_check.status_code == 200
            print(f"   ✅ Cultura {crop_id} existe")
        
        # 6. Atualizar dados
        print(f"\n6️⃣ 🟡 ATUALIZANDO dados...")
        
        # Atualizar produtor
        update_producer = {"document": "11144477777", "name": "Sistema Completo ATUALIZADO"}
        prod_update = client.put(f"/api/producers/{producer_id}", json=update_producer, headers=headers)
        assert prod_update.status_code == 200
        assert "ATUALIZADO" in prod_update.json()["name"]
        print(f"   ✅ Produtor {producer_id} atualizado")
        
        # Atualizar fazenda
        update_farm = {
            "name": "Fazenda Sistema Completo ATUALIZADA",
            "city": "Teste City",
            "state": "TC",
            "total_area": 2500.0,
            "agricultural_area": 2000.0,
            "vegetation_area": 500.0
        }
        farm_update = client.put(f"/api/farms/{farm_id}", json=update_farm, headers=headers)
        assert farm_update.status_code == 200
        assert "ATUALIZADA" in farm_update.json()["name"]
        print(f"   ✅ Fazenda {farm_id} atualizada")
        
        # 7. Deletar tudo na ordem correta (filhos primeiro)
        print(f"\n7️⃣ 🔴 DELETANDO tudo na ordem correta...")
        
        # Deletar culturas
        for i, crop_id in enumerate(crop_ids, 1):
            crop_delete = client.delete(f"/api/crops/{crop_id}", headers=headers)
            assert crop_delete.status_code == 204
            print(f"   ✅ Cultura {crop_id} deletada")
        
        # Deletar safra
        harvest_delete = client.delete(f"/api/harvests/{harvest_id}", headers=headers)
        assert harvest_delete.status_code == 204
        print(f"   ✅ Safra {harvest_id} deletada")
        
        # Deletar fazenda
        farm_delete = client.delete(f"/api/farms/{farm_id}", headers=headers)
        assert farm_delete.status_code == 204
        print(f"   ✅ Fazenda {farm_id} deletada")
        
        # Deletar produtor
        prod_delete = client.delete(f"/api/producers/{producer_id}", headers=headers)
        assert prod_delete.status_code == 204
        print(f"   ✅ Produtor {producer_id} deletado")
        
        # 8. Verificar que tudo foi deletado
        print(f"\n8️⃣ 🔍 VERIFICANDO que tudo foi deletado...")
        
        for entity_type, entity_id in [
            ("producers", producer_id),
            ("farms", farm_id), 
            ("harvests", harvest_id),
            *[("crops", crop_id) for crop_id in crop_ids]
        ]:
            check = client.get(f"/api/{entity_type}/{entity_id}", headers=headers)
            assert check.status_code == 404
            print(f"   ✅ {entity_type}/{entity_id} confirmadamente deletado")
        
        print(f"\n" + "="*60)
        print("🎉 TESTE DE FLUXO COMPLETO REALIZADO COM SUCESSO!")
        print("   CREATE ✅ → READ ✅ → UPDATE ✅ → DELETE ✅ → VERIFY ✅")
        print("="*60 + "\n")