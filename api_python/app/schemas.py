from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enum para tipos de cultura
class CropTypeEnum(str, Enum):
    SOJA = "SOJA"
    MILHO = "MILHO"
    ALGODAO = "ALGODAO"
    CAFE = "CAFE"
    CANA_DE_ACUCAR = "CANA_DE_ACUCAR"

# Schemas do Produtor
class ProducerBase(BaseModel):
    document: str
    name: str

class ProducerCreate(ProducerBase):
    pass

class ProducerUpdate(BaseModel):
    document: Optional[str] = None
    name: Optional[str] = None

class ProducerResponse(ProducerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Schemas da Fazenda
class FarmBase(BaseModel):
    name: str
    city: str
    state: str
    total_area: float = Field(gt=0)
    agricultural_area: float = Field(ge=0)
    vegetation_area: float = Field(ge=0)

class FarmCreate(FarmBase):
    producer_id: int

class FarmUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    total_area: Optional[float] = Field(None, gt=0)
    agricultural_area: Optional[float] = Field(None, ge=0)
    vegetation_area: Optional[float] = Field(None, ge=0)

class FarmResponse(FarmBase):
    id: int
    producer_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Schemas da Safra
class HarvestBase(BaseModel):
    year: int
    description: str

class HarvestCreate(HarvestBase):
    farm_id: int

class HarvestResponse(HarvestBase):
    id: int
    farm_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas da Cultura
class CropBase(BaseModel):
    crop_type: CropTypeEnum
    planted_area: float = Field(gt=0)

class CropCreate(CropBase):
    harvest_id: int

class CropResponse(CropBase):
    id: int
    harvest_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas do Dashboard
class DashboardSummary(BaseModel):
    total_farms: int
    total_area: float

class StateDistribution(BaseModel):
    state: str
    count: int
    percentage: float

class CropDistribution(BaseModel):
    crop_type: str
    total_area: float
    percentage: float

class LandUseDistribution(BaseModel):
    agricultural_area: float
    vegetation_area: float
    agricultural_percentage: float
    vegetation_percentage: float

# Schemas de Autenticação e Usuário
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None