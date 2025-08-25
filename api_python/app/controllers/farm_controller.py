from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas import FarmCreate, FarmUpdate, FarmResponse
from app.services import FarmService
from app.models.user import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/farms", tags=["Fazendas"])

@router.get("/", response_model=List[FarmResponse])
def list_farms(
    producer_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todas as fazendas ou de um produtor especifico"""
    if producer_id:
        return FarmService.get_by_producer(db, producer_id)
    return FarmService.get_all(db)

@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca uma fazenda por ID"""
    farm = FarmService.get_by_id(db, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Fazenda não encontrada")
    return farm

@router.post("/", response_model=FarmResponse, status_code=201)
def create_farm(
    farm_data: FarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova fazenda"""
    try:
        return FarmService.create(db, farm_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{farm_id}", response_model=FarmResponse)
def update_farm(
    farm_id: int,
    farm_data: FarmUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza uma fazenda"""
    try:
        farm = FarmService.update(db, farm_id, farm_data)
        if not farm:
            raise HTTPException(status_code=404, detail="Fazenda não encontrada")
        return farm
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{farm_id}", status_code=204)
def delete_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deleta uma fazenda"""
    if not FarmService.delete(db, farm_id):
        raise HTTPException(status_code=404, detail="Fazenda não encontrada")