from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.harvest import Harvest
from app.models.farm import Farm
from app.schemas import HarvestCreate, HarvestResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/harvests", tags=["Safras"])

@router.get("/", response_model=List[HarvestResponse])
async def list_harvests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lista todas as safras"""
    harvests = db.query(Harvest).offset(skip).limit(limit).all()
    return harvests

@router.get("/{harvest_id}", response_model=HarvestResponse)
async def get_harvest(
    harvest_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtém uma safra específica"""
    harvest = db.query(Harvest).filter(Harvest.id == harvest_id).first()
    if not harvest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Safra não encontrada"
        )
    return harvest

@router.post("/", response_model=HarvestResponse, status_code=201)
async def create_harvest(
    harvest_data: HarvestCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cria uma nova safra"""
    # Verificar se a fazenda existe
    farm = db.query(Farm).filter(Farm.id == harvest_data.farm_id).first()
    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fazenda não encontrada"
        )
    
    harvest = Harvest(**harvest_data.dict())
    db.add(harvest)
    db.commit()
    db.refresh(harvest)
    return harvest

@router.delete("/{harvest_id}", status_code=204)
async def delete_harvest(
    harvest_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Deleta uma safra"""
    harvest = db.query(Harvest).filter(Harvest.id == harvest_id).first()
    if not harvest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Safra não encontrada"
        )
    
    db.delete(harvest)
    db.commit()
    return None

@router.get("/farm/{farm_id}", response_model=List[HarvestResponse])
async def get_harvests_by_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lista todas as safras de uma fazenda específica"""
    harvests = db.query(Harvest).filter(Harvest.farm_id == farm_id).all()
    return harvests