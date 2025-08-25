from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Harvest(Base):
    __tablename__ = "harvests"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String, nullable=False)  # Ex: "Safra 2024"
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    farm = relationship("Farm", back_populates="harvests")
    crops = relationship("Crop", back_populates="harvest", cascade="all, delete-orphan")