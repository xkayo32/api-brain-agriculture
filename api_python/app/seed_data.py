"""
Script para popular o banco com dados de exemplo completos
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Producer, Farm, Harvest, Crop
from app.models.crop import CropType
from app.utils.validators import validate_document
from datetime import datetime

def reset_database():
    """Reseta o banco de dados"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Banco de dados resetado")

def reset_data_tables():
    """Limpa apenas as tabelas de dados (preserva usuarios)"""
    db = SessionLocal()
    try:
        # Deletar na ordem correta por causa das foreign keys
        db.query(Crop).delete()
        db.query(Harvest).delete()
        db.query(Farm).delete()
        db.query(Producer).delete()
        db.commit()
        print("Tabelas de dados limpas")
    finally:
        db.close()

def seed_sample_data():
    """Popula o banco com dados de exemplo completos"""
    db = SessionLocal()
    
    try:
        # Limpar apenas tabelas de dados (preserva usuarios)
        reset_data_tables()
        
        print("Populando banco com dados de exemplo completos...")
        
        # Criar produtores de exemplo
        producers_data = [
            {
                "document": "11144477735",  # CPF valido
                "name": "João Silva Santos"
            },
            {
                "document": "98765432100",  # CPF valido
                "name": "Maria Oliveira Costa"
            },
            {
                "document": "11222333000181",  # CNPJ valido
                "name": "Fazendas Reunidas Ltda"
            },
            {
                "document": "12345678909",  # CPF valido
                "name": "Pedro Almeida Ferreira"
            },
            {
                "document": "11444777000161",  # CNPJ valido
                "name": "Agropecuária Brasil S/A"
            },
            {
                "document": "11144477777",  # CPF valido 
                "name": "Ana Paula Rodrigues"
            },
            {
                "document": "22333444000181",  # CNPJ valido
                "name": "Cooperativa Agrícola Central"
            }
        ]
        
        producers = []
        for prod_data in producers_data:
            if validate_document(prod_data["document"]):
                producer = Producer(**prod_data)
                db.add(producer)
                producers.append(producer)
                print(f"Produtor criado: {prod_data['name']}")
            else:
                print(f"Documento invalido para {prod_data['name']}: {prod_data['document']}")
                # Ainda adiciona None para manter indices
                producers.append(None)
        
        db.flush()
        
        # Criar fazendas de exemplo
        farms_data = [
            {
                "producer_id": 0,
                "name": "Fazenda Santa Rita",
                "city": "Ribeirão Preto",
                "state": "SP",
                "total_area": 1200.0,
                "agricultural_area": 900.0,
                "vegetation_area": 300.0
            },
            {
                "producer_id": 0,
                "name": "Sítio Boa Vista",
                "city": "Franca",
                "state": "SP", 
                "total_area": 450.0,
                "agricultural_area": 350.0,
                "vegetation_area": 100.0
            },
            {
                "producer_id": 1,
                "name": "Fazenda Esperança",
                "city": "Uberaba",
                "state": "MG",
                "total_area": 2500.0,
                "agricultural_area": 2000.0,
                "vegetation_area": 500.0
            },
            {
                "producer_id": 2,
                "name": "Complexo Agropecuário Vale Verde",
                "city": "Campo Grande",
                "state": "MS",
                "total_area": 5000.0,
                "agricultural_area": 4200.0,
                "vegetation_area": 800.0
            },
            {
                "producer_id": 2,
                "name": "Fazenda União",
                "city": "Dourados",
                "state": "MS",
                "total_area": 3200.0,
                "agricultural_area": 2800.0,
                "vegetation_area": 400.0
            },
            {
                "producer_id": 3,
                "name": "Rancho Dois Irmãos",
                "city": "Barretos",
                "state": "SP",
                "total_area": 800.0,
                "agricultural_area": 600.0,
                "vegetation_area": 200.0
            },
            {
                "producer_id": 4,
                "name": "Fazenda Continental",
                "city": "Sorriso",
                "state": "MT",
                "total_area": 8500.0,
                "agricultural_area": 7500.0,
                "vegetation_area": 1000.0
            },
            {
                "producer_id": 4,
                "name": "Fazenda Primavera",
                "city": "Lucas do Rio Verde",
                "state": "MT",
                "total_area": 6200.0,
                "agricultural_area": 5500.0,
                "vegetation_area": 700.0
            },
            {
                "producer_id": 5,
                "name": "Chácara Felicidade",
                "city": "Campinas",
                "state": "SP",
                "total_area": 120.0,
                "agricultural_area": 80.0,
                "vegetation_area": 40.0
            },
            {
                "producer_id": 6,
                "name": "Fazenda Cooperada Norte",
                "city": "Cristalina",
                "state": "GO",
                "total_area": 4800.0,
                "agricultural_area": 4000.0,
                "vegetation_area": 800.0
            },
            {
                "producer_id": 6,
                "name": "Fazenda Cooperada Sul",
                "city": "Rio Verde",
                "state": "GO",
                "total_area": 3600.0,
                "agricultural_area": 3000.0,
                "vegetation_area": 600.0
            },
            {
                "producer_id": 0,
                "name": "Fazenda Nova Era",
                "city": "Araraquara",
                "state": "SP",
                "total_area": 650.0,
                "agricultural_area": 500.0,
                "vegetation_area": 150.0
            }
        ]
        
        farms = []
        for i, farm_data in enumerate(farms_data):
            # Map producer_id to actual producer
            producer_idx = farm_data['producer_id']
            if producers[producer_idx] is None:
                print(f"Pulando fazenda {farm_data['name']} - produtor invalido")
                farms.append(None)
                continue
            farm_data['producer_id'] = producers[producer_idx].id
            farm = Farm(**farm_data)
            db.add(farm)
            farms.append(farm)
        
        db.flush()
        
        # Criar safras de exemplo
        harvests_data = [
            {"farm_idx": 0, "year": 2024, "description": "Safra 2024 - Principal"},
            {"farm_idx": 0, "year": 2024, "description": "Safrinha 2024"},
            {"farm_idx": 1, "year": 2024, "description": "Safra 2024"},
            {"farm_idx": 2, "year": 2024, "description": "Safra 2024 - Principal"},
            {"farm_idx": 3, "year": 2024, "description": "Safra 2024 - Verão"},
            {"farm_idx": 3, "year": 2024, "description": "Safra 2024 - Inverno"},
            {"farm_idx": 4, "year": 2024, "description": "Safra 2024"},
            {"farm_idx": 5, "year": 2024, "description": "Safra 2024"},
            {"farm_idx": 6, "year": 2024, "description": "Safra 2024 - Principal"},
            {"farm_idx": 7, "year": 2024, "description": "Safra 2024 - Principal"},
            {"farm_idx": 8, "year": 2024, "description": "Safra 2024"},
            {"farm_idx": 9, "year": 2024, "description": "Safra 2024 - Verão"},
            {"farm_idx": 10, "year": 2024, "description": "Safra 2024 - Verão"},
            {"farm_idx": 11, "year": 2024, "description": "Safra 2024"},
        ]
        
        harvests = []
        for harvest_data in harvests_data:
            farm_idx = harvest_data.pop('farm_idx')
            if farms[farm_idx] is None:
                print(f"Pulando safra - fazenda invalida")
                harvests.append(None)
                continue
            harvest_data['farm_id'] = farms[farm_idx].id
            harvest = Harvest(**harvest_data)
            db.add(harvest)
            harvests.append(harvest)
        
        db.flush()
        
        # Criar culturas de exemplo
        crops_data = [
            # Fazenda 1 - Safra principal
            {"harvest_idx": 0, "crop_type": CropType.SOJA, "planted_area": 700.0},
            {"harvest_idx": 0, "crop_type": CropType.MILHO, "planted_area": 200.0},
            # Fazenda 1 - Safrinha
            {"harvest_idx": 1, "crop_type": CropType.MILHO, "planted_area": 500.0},
            {"harvest_idx": 1, "crop_type": CropType.ALGODAO, "planted_area": 400.0},
            
            # Fazenda 2
            {"harvest_idx": 2, "crop_type": CropType.CAFE, "planted_area": 250.0},
            {"harvest_idx": 2, "crop_type": CropType.SOJA, "planted_area": 100.0},
            
            # Fazenda 3
            {"harvest_idx": 3, "crop_type": CropType.SOJA, "planted_area": 1500.0},
            {"harvest_idx": 3, "crop_type": CropType.MILHO, "planted_area": 500.0},
            
            # Fazenda 4 - Safra Verão
            {"harvest_idx": 4, "crop_type": CropType.SOJA, "planted_area": 3000.0},
            {"harvest_idx": 4, "crop_type": CropType.MILHO, "planted_area": 1200.0},
            # Fazenda 4 - Safra Inverno
            {"harvest_idx": 5, "crop_type": CropType.ALGODAO, "planted_area": 2500.0},
            {"harvest_idx": 5, "crop_type": CropType.MILHO, "planted_area": 1700.0},
            
            # Fazenda 5
            {"harvest_idx": 6, "crop_type": CropType.SOJA, "planted_area": 2000.0},
            {"harvest_idx": 6, "crop_type": CropType.CANA_DE_ACUCAR, "planted_area": 800.0},
            
            # Fazenda 6
            {"harvest_idx": 7, "crop_type": CropType.CAFE, "planted_area": 400.0},
            {"harvest_idx": 7, "crop_type": CropType.MILHO, "planted_area": 200.0},
            
            # Fazenda 7
            {"harvest_idx": 8, "crop_type": CropType.SOJA, "planted_area": 5500.0},
            {"harvest_idx": 8, "crop_type": CropType.MILHO, "planted_area": 2000.0},
            
            # Fazenda 8
            {"harvest_idx": 9, "crop_type": CropType.SOJA, "planted_area": 4000.0},
            {"harvest_idx": 9, "crop_type": CropType.ALGODAO, "planted_area": 1500.0},
            
            # Fazenda 9
            {"harvest_idx": 10, "crop_type": CropType.CAFE, "planted_area": 50.0},
            {"harvest_idx": 10, "crop_type": CropType.MILHO, "planted_area": 30.0},
            
            # Fazenda 10
            {"harvest_idx": 11, "crop_type": CropType.SOJA, "planted_area": 3000.0},
            {"harvest_idx": 11, "crop_type": CropType.MILHO, "planted_area": 1000.0},
            
            # Fazenda 11
            {"harvest_idx": 12, "crop_type": CropType.SOJA, "planted_area": 2200.0},
            {"harvest_idx": 12, "crop_type": CropType.ALGODAO, "planted_area": 800.0},
            
            # Fazenda 12
            {"harvest_idx": 13, "crop_type": CropType.CANA_DE_ACUCAR, "planted_area": 350.0},
            {"harvest_idx": 13, "crop_type": CropType.SOJA, "planted_area": 150.0},
        ]
        
        for crop_data in crops_data:
            harvest_idx = crop_data.pop('harvest_idx')
            if harvests[harvest_idx] is None:
                print(f"Pulando cultura - safra invalida")
                continue
            crop_data['harvest_id'] = harvests[harvest_idx].id
            crop = Crop(**crop_data)
            db.add(crop)
        
        db.commit()
        
        # Estatísticas finais
        total_producers = db.query(Producer).count()
        total_farms = db.query(Farm).count()
        total_harvests = db.query(Harvest).count()
        total_crops = db.query(Crop).count()
        
        print(f"\n=== DADOS CRIADOS COM SUCESSO ===")
        print(f"Produtores: {total_producers}")
        print(f"Fazendas: {total_farms}")
        print(f"Safras: {total_harvests}")
        print(f"Culturas: {total_crops}")
        print(f"================================")
        
        # Calcular totais por estado
        from sqlalchemy import func
        states = db.query(Farm.state, func.count(Farm.id), func.sum(Farm.total_area)).\
            group_by(Farm.state).all()
        
        print(f"\n=== DISTRIBUIÇÃO POR ESTADO ===")
        for state, count, area in states:
            print(f"{state}: {count} fazendas, {area:.0f} hectares")
        
        # Calcular totais por cultura
        crops_summary = db.query(Crop.crop_type, func.sum(Crop.planted_area)).\
            group_by(Crop.crop_type).all()
        
        print(f"\n=== DISTRIBUIÇÃO POR CULTURA ===")
        for crop_type, area in crops_summary:
            print(f"{crop_type.value}: {area:.0f} hectares")
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar dados de exemplo: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_sample_data()