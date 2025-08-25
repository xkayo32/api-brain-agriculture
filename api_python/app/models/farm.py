from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Farm(Base):
    __tablename__ = "farms"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    total_area = Column(Float, nullable=False)  # em hectares
    agricultural_area = Column(Float, nullable=False)
    vegetation_area = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    producer = relationship("Producer", back_populates="farms")
    harvests = relationship("Harvest", back_populates="farm", cascade="all, delete-orphan")