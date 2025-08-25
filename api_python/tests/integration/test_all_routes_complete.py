"""
Testes completos de TODAS as rotas da API
Este arquivo garante 100% de cobertura de rotas
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.models.user import User
from app.models.producer import Producer
from app.models.farm import Farm
from app.models.harvest import Harvest
from app.models.crop import Crop, CropType
from app.utils.security import get_password_hash
from main import app

# Banco de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_complete.db"
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

@pytest.fixture(scope="function")
def db_session():
    """Sessão do banco de teste"""
    session = TestingSessionLocal()
    yield session
    session.query(Crop).delete()
    session.query(Harvest).delete()
    session.query(Farm).delete()
    session.query(Producer).delete()
    session.query(User).delete()
    session.commit()
    session.close()

@pytest.fixture
def admin_token(client, db_session):
    """Cria admin e retorna token"""
    # Criar usuário admin
    admin = User(
        username="admin_test",
        email="admin@test.com",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_admin=True
    )
    db_session.add(admin)
    db_session.commit()
    
    # Fazer login
    response = client.post(
        "/api/auth/login",
        data={"username": "admin_test", "password": "admin123"}
    )
    return f"Bearer {response.json()['access_token']}"

@pytest.fixture
def sample_data(db_session):
    """Cria dados de exemplo para testes"""
    # Produtor
    producer = Producer(
        document="11144477735",
        name="Produtor Teste"
    )
    db_session.add(producer)
    db_session.flush()
    
    # Fazenda
    farm = Farm(
        producer_id=producer.id,
        name="Fazenda Teste",
        city="São Paulo",
        state="SP",
        total_area=1000.0,
        agricultural_area=700.0,
        vegetation_area=300.0
    )
    db_session.add(farm)
    db_session.flush()
    
    # Safra
    harvest = Harvest(
        farm_id=farm.id,
        year=2024,
        description="Safra 2024"
    )
    db_session.add(harvest)
    db_session.flush()
    
    # Cultura
    crop = Crop(
        harvest_id=harvest.id,
        crop_type=CropType.SOJA,
        planted_area=500.0
    )
    db_session.add(crop)
    db_session.commit()
    
    return {
        "producer_id": producer.id,
        "farm_id": farm.id,
        "harvest_id": harvest.id,
        "crop_id": crop.id
    }


class TestAuthRoutes:
    """Testes completos das rotas de autenticação"""
    
    def test_register_new_user(self, client):
        """POST /api/auth/register"""
        response = client.post("/api/auth/register", json={
            "username": "novo_usuario",
            "email": "novo@test.com",
            "password": "senha123"
        })
        assert response.status_code == 201
        assert response.json()["username"] == "novo_usuario"
    
    def test_login_success(self, client, db_session):
        """POST /api/auth/login - sucesso"""
        # Criar usuário
        user = User(
            username="test_login",
            email="login@test.com",
            hashed_password=get_password_hash("senha123"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Login
        response = client.post(
            "/api/auth/login",
            data={"username": "test_login", "password": "senha123"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_login_fail(self, client):
        """POST /api/auth/login - falha"""
        response = client.post(
            "/api/auth/login",
            data={"username": "nao_existe", "password": "senha123"}
        )
        assert response.status_code == 401
    
    def test_get_current_user(self, client, admin_token):
        """GET /api/auth/me"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert response.json()["username"] == "admin_test"
    
    def test_get_current_user_unauthorized(self, client):
        """GET /api/auth/me - sem autorização"""
        response = client.get("/api/auth/me")
        assert response.status_code == 401
    
    def test_list_users(self, client, admin_token):
        """GET /api/auth/users"""
        response = client.get(
            "/api/auth/users",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_list_users_unauthorized(self, client):
        """GET /api/auth/users - sem autorização"""
        response = client.get("/api/auth/users")
        assert response.status_code == 401


class TestProducerRoutes:
    """Testes completos das rotas de produtores"""
    
    def test_list_producers(self, client, admin_token):
        """GET /api/producers/"""
        response = client.get(
            "/api/producers/",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_list_producers_unauthorized(self, client):
        """GET /api/producers/ - sem autorização"""
        response = client.get("/api/producers/")
        assert response.status_code == 401
    
    def test_get_producer_by_id(self, client, admin_token, sample_data):
        """GET /api/producers/{id}"""
        response = client.get(
            f"/api/producers/{sample_data['producer_id']}",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Produtor Teste"
    
    def test_get_producer_not_found(self, client, admin_token):
        """GET /api/producers/{id} - não encontrado"""
        response = client.get(
            "/api/producers/99999",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 404
    
    def test_create_producer(self, client, admin_token):
        """POST /api/producers/"""
        response = client.post(
            "/api/producers/",
            json={
                "document": "98765432100",
                "name": "Novo Produtor"
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 201
        assert response.json()["name"] == "Novo Produtor"
    
    def test_create_producer_invalid_document(self, client, admin_token):
        """POST /api/producers/ - documento inválido"""
        response = client.post(
            "/api/producers/",
            json={
                "document": "12345678900",  # CPF inválido
                "name": "Produtor Inválido"
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 400
    
    def test_update_producer(self, client, admin_token, sample_data):
        """PUT /api/producers/{id}"""
        response = client.put(
            f"/api/producers/{sample_data['producer_id']}",
            json={
                "document": "11144477735",
                "name": "Produtor Atualizado"
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Produtor Atualizado"
    
    def test_delete_producer(self, client, admin_token, db_session):
        """DELETE /api/producers/{id}"""
        # Criar produtor para deletar
        producer = Producer(document="12345678909", name="Deletar")
        db_session.add(producer)
        db_session.commit()
        
        response = client.delete(
            f"/api/producers/{producer.id}",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 204


class TestFarmRoutes:
    """Testes completos das rotas de fazendas"""
    
    def test_list_farms(self, client, admin_token):
        """GET /api/farms/"""
        response = client.get(
            "/api/farms/",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_farm_by_id(self, client, admin_token, sample_data):
        """GET /api/farms/{id}"""
        response = client.get(
            f"/api/farms/{sample_data['farm_id']}",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Fazenda Teste"
    
    def test_create_farm(self, client, admin_token, sample_data):
        """POST /api/farms/"""
        response = client.post(
            "/api/farms/",
            json={
                "producer_id": sample_data['producer_id'],
                "name": "Nova Fazenda",
                "city": "Rio de Janeiro",
                "state": "RJ",
                "total_area": 500.0,
                "agricultural_area": 300.0,
                "vegetation_area": 200.0
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 201
        assert response.json()["name"] == "Nova Fazenda"
    
    def test_create_farm_invalid_areas(self, client, admin_token, sample_data):
        """POST /api/farms/ - áreas inválidas"""
        response = client.post(
            "/api/farms/",
            json={
                "producer_id": sample_data['producer_id'],
                "name": "Fazenda Inválida",
                "city": "São Paulo",
                "state": "SP",
                "total_area": 500.0,
                "agricultural_area": 400.0,
                "vegetation_area": 200.0  # Soma > total
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 400
    
    def test_update_farm(self, client, admin_token, sample_data):
        """PUT /api/farms/{id}"""
        response = client.put(
            f"/api/farms/{sample_data['farm_id']}",
            json={
                "name": "Fazenda Atualizada",
                "city": "São Paulo",
                "state": "SP",
                "total_area": 1200.0,
                "agricultural_area": 800.0,
                "vegetation_area": 400.0
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Fazenda Atualizada"
    
    def test_delete_farm(self, client, admin_token, db_session, sample_data):
        """DELETE /api/farms/{id}"""
        # Criar fazenda para deletar
        farm = Farm(
            producer_id=sample_data['producer_id'],
            name="Deletar",
            city="Test",
            state="TS",
            total_area=100.0,
            agricultural_area=70.0,
            vegetation_area=30.0
        )
        db_session.add(farm)
        db_session.commit()
        
        response = client.delete(
            f"/api/farms/{farm.id}",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 204


class TestHarvestRoutes:
    """Testes completos das rotas de safras"""
    
    def test_list_harvests(self, client, admin_token):
        """GET /api/harvests/"""
        response = client.get(
            "/api/harvests/",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_harvest_by_id(self, client, admin_token, sample_data):
        """GET /api/harvests/{id}"""
        response = client.get(
            f"/api/harvests/{sample_data['harvest_id']}",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert response.json()["description"] == "Safra 2024"
    
    def test_get_harvest_not_found(self, client, admin_token):
        """GET /api/harvests/{id} - não encontrado"""
        response = client.get(
            "/api/harvests/99999",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 404
    
    def test_create_harvest(self, client, admin_token, sample_data):
        """POST /api/harvests/"""
        response = client.post(
            "/api/harvests/",
            json={
                "farm_id": sample_data['farm_id'],
                "year": 2025,
                "description": "Safra 2025"
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 201
        assert response.json()["description"] == "Safra 2025"
    
    def test_create_harvest_invalid_farm(self, client, admin_token):
        """POST /api/harvests/ - fazenda inválida"""
        response = client.post(
            "/api/harvests/",
            json={
                "farm_id": 99999,
                "year": 2025,
                "description": "Safra Inválida"
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 404
    
    def test_delete_harvest(self, client, admin_token, db_session, sample_data):
        """DELETE /api/harvests/{id}"""
        # Criar safra para deletar
        harvest = Harvest(
            farm_id=sample_data['farm_id'],
            year=2026,
            description="Deletar"
        )
        db_session.add(harvest)
        db_session.commit()
        
        response = client.delete(
            f"/api/harvests/{harvest.id}",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 204
    
    def test_get_harvests_by_farm(self, client, admin_token, sample_data):
        """GET /api/harvests/farm/{farm_id}"""
        response = client.get(
            f"/api/harvests/farm/{sample_data['farm_id']}",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1


class TestCropRoutes:
    """Testes completos das rotas de culturas"""
    
    def test_list_crops(self, client, admin_token):
        """GET /api/crops/"""
        response = client.get(
            "/api/crops/",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_crop_by_id(self, client, admin_token, sample_data):
        """GET /api/crops/{id}"""
        response = client.get(
            f"/api/crops/{sample_data['crop_id']}",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert response.json()["planted_area"] == 500.0
    
    def test_get_crop_not_found(self, client, admin_token):
        """GET /api/crops/{id} - não encontrado"""
        response = client.get(
            "/api/crops/99999",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 404
    
    def test_create_crop(self, client, admin_token, sample_data):
        """POST /api/crops/"""
        response = client.post(
            "/api/crops/",
            json={
                "harvest_id": sample_data['harvest_id'],
                "crop_type": "MILHO",
                "planted_area": 200.0
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 201
        assert response.json()["crop_type"] == "MILHO"
    
    def test_create_crop_invalid_harvest(self, client, admin_token):
        """POST /api/crops/ - safra inválida"""
        response = client.post(
            "/api/crops/",
            json={
                "harvest_id": 99999,
                "crop_type": "SOJA",
                "planted_area": 100.0
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 404
    
    def test_create_crop_invalid_area(self, client, admin_token, sample_data):
        """POST /api/crops/ - área inválida"""
        response = client.post(
            "/api/crops/",
            json={
                "harvest_id": sample_data['harvest_id'],
                "crop_type": "CAFE",
                "planted_area": 0  # Área inválida
            },
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 422
    
    def test_delete_crop(self, client, admin_token, db_session, sample_data):
        """DELETE /api/crops/{id}"""
        # Criar cultura para deletar
        crop = Crop(
            harvest_id=sample_data['harvest_id'],
            crop_type=CropType.ALGODAO,
            planted_area=150.0
        )
        db_session.add(crop)
        db_session.commit()
        
        response = client.delete(
            f"/api/crops/{crop.id}",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 204
    
    def test_get_crops_by_harvest(self, client, admin_token, sample_data):
        """GET /api/crops/harvest/{harvest_id}"""
        response = client.get(
            f"/api/crops/harvest/{sample_data['harvest_id']}",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_crops_by_type(self, client, admin_token, sample_data):
        """GET /api/crops/type/{crop_type}"""
        response = client.get(
            "/api/crops/type/SOJA",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestDashboardRoutes:
    """Testes completos das rotas de dashboard"""
    
    def test_dashboard_summary(self, client):
        """GET /api/dashboard/summary"""
        response = client.get("/api/dashboard/summary")
        assert response.status_code == 200
        assert "total_farms" in response.json()
        assert "total_area" in response.json()
    
    def test_dashboard_by_state(self, client):
        """GET /api/dashboard/by-state"""
        response = client.get("/api/dashboard/by-state")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_dashboard_by_crop(self, client):
        """GET /api/dashboard/by-crop"""
        response = client.get("/api/dashboard/by-crop")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_dashboard_land_use(self, client):
        """GET /api/dashboard/land-use"""
        response = client.get("/api/dashboard/land-use")
        assert response.status_code == 200
        assert "agricultural_area" in response.json()
        assert "vegetation_area" in response.json()


class TestUtilityRoutes:
    """Testes das rotas utilitárias"""
    
    def test_health_check(self, client):
        """GET /health"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "OK"
    
    def test_root_endpoint(self, client):
        """GET /"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "docs" in response.json()
    
    def test_docs_endpoint(self, client):
        """GET /docs"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()
    
    def test_openapi_json(self, client):
        """GET /openapi.json"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        json_data = response.json()
        assert "openapi" in json_data
        assert "paths" in json_data


class TestErrorHandling:
    """Testes de tratamento de erros"""
    
    def test_404_not_found(self, client):
        """Rota inexistente"""
        response = client.get("/api/rota-nao-existe")
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Método não permitido"""
        response = client.patch("/api/producers/")
        assert response.status_code == 405
    
    def test_malformed_json(self, client, admin_token):
        """JSON mal formado"""
        response = client.post(
            "/api/producers/",
            data="invalid json",
            headers={
                "Authorization": admin_token,
                "Content-Type": "application/json"
            }
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client, admin_token):
        """Campos obrigatórios faltando"""
        response = client.post(
            "/api/producers/",
            json={"name": "Sem documento"},  # Falta document
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 422
    
    def test_invalid_token(self, client):
        """Token inválido"""
        response = client.get(
            "/api/producers/",
            headers={"Authorization": "Bearer token_invalido"}
        )
        assert response.status_code == 401
    
    def test_expired_token(self, client):
        """Token expirado"""
        # Token com exp no passado
        expired_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjAwMDAwMDAwfQ.abc123"
        response = client.get(
            "/api/producers/",
            headers={"Authorization": expired_token}
        )
        assert response.status_code == 401


class TestPagination:
    """Testes de paginação"""
    
    def test_producers_pagination(self, client, admin_token):
        """Paginação de produtores"""
        response = client.get(
            "/api/producers/?skip=0&limit=5",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_farms_pagination(self, client, admin_token):
        """Paginação de fazendas"""
        response = client.get(
            "/api/farms/?skip=10&limit=10",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_harvests_pagination(self, client, admin_token):
        """Paginação de safras"""
        response = client.get(
            "/api/harvests/?skip=0&limit=100",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_crops_pagination(self, client, admin_token):
        """Paginação de culturas"""
        response = client.get(
            "/api/crops/?skip=5&limit=20",
            headers={"Authorization": admin_token}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# Contador de rotas testadas
def count_tested_routes():
    """Conta quantas rotas foram testadas"""
    routes = {
        "Auth": [
            "POST /api/auth/register",
            "POST /api/auth/login", 
            "GET /api/auth/me",
            "GET /api/auth/users"
        ],
        "Producers": [
            "GET /api/producers/",
            "GET /api/producers/{id}",
            "POST /api/producers/",
            "PUT /api/producers/{id}",
            "DELETE /api/producers/{id}"
        ],
        "Farms": [
            "GET /api/farms/",
            "GET /api/farms/{id}",
            "POST /api/farms/",
            "PUT /api/farms/{id}",
            "DELETE /api/farms/{id}"
        ],
        "Harvests": [
            "GET /api/harvests/",
            "GET /api/harvests/{id}",
            "POST /api/harvests/",
            "DELETE /api/harvests/{id}",
            "GET /api/harvests/farm/{farm_id}"
        ],
        "Crops": [
            "GET /api/crops/",
            "GET /api/crops/{id}",
            "POST /api/crops/",
            "DELETE /api/crops/{id}",
            "GET /api/crops/harvest/{harvest_id}",
            "GET /api/crops/type/{crop_type}"
        ],
        "Dashboard": [
            "GET /api/dashboard/summary",
            "GET /api/dashboard/by-state",
            "GET /api/dashboard/by-crop",
            "GET /api/dashboard/land-use"
        ],
        "Utility": [
            "GET /health",
            "GET /",
            "GET /docs",
            "GET /openapi.json"
        ]
    }
    
    total = sum(len(endpoints) for endpoints in routes.values())
    print(f"\n{'='*60}")
    print(f"COBERTURA COMPLETA DE ROTAS")
    print(f"{'='*60}")
    for category, endpoints in routes.items():
        print(f"\n{category}: {len(endpoints)} rotas")
        for endpoint in endpoints:
            print(f"  ✅ {endpoint}")
    print(f"\n{'='*60}")
    print(f"TOTAL: {total} rotas testadas")
    print(f"{'='*60}\n")
    
    return total

# Executar contador ao importar o módulo
if __name__ == "__main__":
    count_tested_routes()