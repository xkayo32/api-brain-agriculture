from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class CropType(enum.Enum):
    SOJA = "SOJA"
    MILHO = "MILHO"
    ALGODAO = "ALGODAO"
    CAFE = "CAFE"
    CANA_DE_ACUCAR = "CANA_DE_ACUCAR"

class Crop(Base):
    __tablename__ = "crops"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    harvest_id = Column(Integer, ForeignKey("harvests.id"), nullable=False)
    crop_type = Column(Enum(CropType), nullable=False)
    planted_area = Column(Float, nullable=False)  # em hectares
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    harvest = relationship("Harvest", back_populates="crops")