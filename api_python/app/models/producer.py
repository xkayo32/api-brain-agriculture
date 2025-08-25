from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Producer(Base):
    __tablename__ = "producers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document = Column(String, nullable=False, unique=True)  # CPF ou CNPJ
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamento com fazendas
    farms = relationship("Farm", back_populates="producer", cascade="all, delete-orphan")