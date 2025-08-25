from sqlalchemy.orm import Session
from app.models import Farm, Producer
from app.schemas import FarmCreate, FarmUpdate
from typing import List, Optional

class FarmService:
    
    @staticmethod
    def get_all(db: Session) -> List[Farm]:
        """Busca todas as fazendas"""
        return db.query(Farm).all()
    
    @staticmethod
    def get_by_id(db: Session, farm_id: int) -> Optional[Farm]:
        """Busca fazenda por ID"""
        return db.query(Farm).filter(Farm.id == farm_id).first()
    
    @staticmethod
    def get_by_producer(db: Session, producer_id: int) -> List[Farm]:
        """Busca fazendas de um produtor"""
        return db.query(Farm).filter(Farm.producer_id == producer_id).all()
    
    @staticmethod
    def create(db: Session, farm_data: FarmCreate) -> Farm:
        """Cria uma nova fazenda"""
        # Valida as areas
        if farm_data.agricultural_area + farm_data.vegetation_area > farm_data.total_area:
            raise ValueError("A soma das áreas agricultável e vegetação não pode ser maior que a área total")
        
        # Verifica se o produtor existe
        producer = db.query(Producer).filter(Producer.id == farm_data.producer_id).first()
        if not producer:
            raise ValueError("Produtor não encontrado")
        
        # Cria a fazenda
        farm = Farm(**farm_data.dict())
        db.add(farm)
        db.commit()
        db.refresh(farm)
        return farm
    
    @staticmethod
    def update(db: Session, farm_id: int, farm_data: FarmUpdate) -> Optional[Farm]:
        """Atualiza uma fazenda"""
        farm = FarmService.get_by_id(db, farm_id)
        if not farm:
            return None
        
        # Pega os valores atuais ou novos
        total_area = farm_data.total_area if farm_data.total_area is not None else farm.total_area
        agricultural_area = farm_data.agricultural_area if farm_data.agricultural_area is not None else farm.agricultural_area
        vegetation_area = farm_data.vegetation_area if farm_data.vegetation_area is not None else farm.vegetation_area
        
        # Valida as areas
        if agricultural_area + vegetation_area > total_area:
            raise ValueError("A soma das áreas agricultável e vegetação não pode ser maior que a área total")
        
        # Atualiza os campos
        for field, value in farm_data.dict(exclude_unset=True).items():
            setattr(farm, field, value)
        
        db.commit()
        db.refresh(farm)
        return farm
    
    @staticmethod
    def delete(db: Session, farm_id: int) -> bool:
        """Deleta uma fazenda"""
        farm = FarmService.get_by_id(db, farm_id)
        if not farm:
            return False
        
        db.delete(farm)
        db.commit()
        return True