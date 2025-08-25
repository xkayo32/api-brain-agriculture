from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.crop import Crop
from app.models.harvest import Harvest
from app.schemas import CropCreate, CropResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/crops", tags=["Culturas"])

@router.get("/", response_model=List[CropResponse])
async def list_crops(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lista todas as culturas"""
    crops = db.query(Crop).offset(skip).limit(limit).all()
    return crops

@router.get("/{crop_id}", response_model=CropResponse)
async def get_crop(
    crop_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtém uma cultura específica"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultura não encontrada"
        )
    return crop

@router.post("/", response_model=CropResponse, status_code=201)
async def create_crop(
    crop_data: CropCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cria uma nova cultura"""
    # Verificar se a safra existe
    harvest = db.query(Harvest).filter(Harvest.id == crop_data.harvest_id).first()
    if not harvest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Safra não encontrada"
        )
    
    # Validar área plantada
    if crop_data.planted_area <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Área plantada deve ser maior que zero"
        )
    
    crop = Crop(**crop_data.dict())
    db.add(crop)
    db.commit()
    db.refresh(crop)
    return crop

@router.delete("/{crop_id}", status_code=204)
async def delete_crop(
    crop_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Deleta uma cultura"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultura não encontrada"
        )
    
    db.delete(crop)
    db.commit()
    return None

@router.get("/harvest/{harvest_id}", response_model=List[CropResponse])
async def get_crops_by_harvest(
    harvest_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lista todas as culturas de uma safra específica"""
    crops = db.query(Crop).filter(Crop.harvest_id == harvest_id).all()
    return crops

@router.get("/type/{crop_type}", response_model=List[CropResponse])
async def get_crops_by_type(
    crop_type: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lista todas as culturas de um tipo específico"""
    crops = db.query(Crop).filter(Crop.crop_type == crop_type).all()
    return crops