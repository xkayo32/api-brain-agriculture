from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import ProducerCreate, ProducerUpdate, ProducerResponse
from app.services import ProducerService
from app.models.user import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/producers", tags=["Produtores"])

@router.get("/", response_model=List[ProducerResponse])
def list_producers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todos os produtores"""
    return ProducerService.get_all(db)

@router.get("/{producer_id}", response_model=ProducerResponse)
def get_producer(
    producer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca um produtor por ID"""
    producer = ProducerService.get_by_id(db, producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return producer

@router.post("/", response_model=ProducerResponse, status_code=201)
def create_producer(
    producer_data: ProducerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria um novo produtor"""
    try:
        return ProducerService.create(db, producer_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{producer_id}", response_model=ProducerResponse)
def update_producer(
    producer_id: int,
    producer_data: ProducerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza um produtor"""
    try:
        producer = ProducerService.update(db, producer_id, producer_data)
        if not producer:
            raise HTTPException(status_code=404, detail="Produtor não encontrado")
        return producer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{producer_id}", status_code=204)
def delete_producer(
    producer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deleta um produtor"""
    if not ProducerService.delete(db, producer_id):
        raise HTTPException(status_code=404, detail="Produtor não encontrado")