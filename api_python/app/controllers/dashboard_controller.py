from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import DashboardSummary, StateDistribution, LandUseDistribution, CropDistribution
from app.services import DashboardService

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Retorna o resumo do dashboard"""
    return DashboardService.get_summary(db)

@router.get("/by-state", response_model=List[StateDistribution])
def get_state_distribution(db: Session = Depends(get_db)):
    """Retorna a distribuicao de fazendas por estado"""
    return DashboardService.get_state_distribution(db)

@router.get("/land-use", response_model=LandUseDistribution)
def get_land_use_distribution(db: Session = Depends(get_db)):
    """Retorna a distribuicao de uso do solo"""
    return DashboardService.get_land_use_distribution(db)

@router.get("/by-crop", response_model=List[CropDistribution])
def get_crop_distribution(db: Session = Depends(get_db)):
    """Retorna a distribuicao por tipo de cultura"""
    return DashboardService.get_crop_distribution(db)