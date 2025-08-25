from sqlalchemy.orm import Session
from app.models import Producer
from app.schemas import ProducerCreate, ProducerUpdate
from app.utils import validate_document
from typing import List, Optional

class ProducerService:
    
    @staticmethod
    def get_all(db: Session) -> List[Producer]:
        """Busca todos os produtores"""
        return db.query(Producer).all()
    
    @staticmethod
    def get_by_id(db: Session, producer_id: int) -> Optional[Producer]:
        """Busca produtor por ID"""
        return db.query(Producer).filter(Producer.id == producer_id).first()
    
    @staticmethod
    def get_by_document(db: Session, document: str) -> Optional[Producer]:
        """Busca produtor por documento"""
        return db.query(Producer).filter(Producer.document == document).first()
    
    @staticmethod
    def create(db: Session, producer_data: ProducerCreate) -> Producer:
        """Cria um novo produtor"""
        # Valida o documento
        if not validate_document(producer_data.document):
            raise ValueError("Documento inválido (CPF ou CNPJ)")
        
        # Verifica se ja existe
        existing = ProducerService.get_by_document(db, producer_data.document)
        if existing:
            raise ValueError("Já existe um produtor com esse documento")
        
        # Cria o produtor
        producer = Producer(**producer_data.dict())
        db.add(producer)
        db.commit()
        db.refresh(producer)
        return producer
    
    @staticmethod
    def update(db: Session, producer_id: int, producer_data: ProducerUpdate) -> Optional[Producer]:
        """Atualiza um produtor"""
        producer = ProducerService.get_by_id(db, producer_id)
        if not producer:
            return None
        
        # Valida documento se foi enviado
        if producer_data.document and not validate_document(producer_data.document):
            raise ValueError("Documento inválido (CPF ou CNPJ)")
        
        # Atualiza os campos
        for field, value in producer_data.dict(exclude_unset=True).items():
            setattr(producer, field, value)
        
        db.commit()
        db.refresh(producer)
        return producer
    
    @staticmethod
    def delete(db: Session, producer_id: int) -> bool:
        """Deleta um produtor"""
        producer = ProducerService.get_by_id(db, producer_id)
        if not producer:
            return False
        
        db.delete(producer)
        db.commit()
        return True