from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Farm, Crop
from app.schemas import DashboardSummary, StateDistribution, LandUseDistribution, CropDistribution
from typing import List

class DashboardService:
    
    @staticmethod
    def get_summary(db: Session) -> DashboardSummary:
        """Retorna o resumo do dashboard"""
        total_farms = db.query(Farm).count()
        total_area = db.query(func.sum(Farm.total_area)).scalar() or 0.0
        
        return DashboardSummary(
            total_farms=total_farms,
            total_area=total_area
        )
    
    @staticmethod
    def get_state_distribution(db: Session) -> List[StateDistribution]:
        """Retorna a distribuicao por estado"""
        # Busca quantidade por estado
        states = db.query(
            Farm.state,
            func.count(Farm.id).label('count')
        ).group_by(Farm.state).all()
        
        total = sum(s.count for s in states)
        
        result = []
        for state in states:
            percentage = (state.count / total * 100) if total > 0 else 0
            result.append(StateDistribution(
                state=state.state,
                count=state.count,
                percentage=percentage
            ))
        
        return result
    
    @staticmethod
    def get_land_use_distribution(db: Session) -> LandUseDistribution:
        """Retorna a distribuicao de uso do solo"""
        agricultural_area = db.query(func.sum(Farm.agricultural_area)).scalar() or 0.0
        vegetation_area = db.query(func.sum(Farm.vegetation_area)).scalar() or 0.0
        
        total = agricultural_area + vegetation_area
        
        return LandUseDistribution(
            agricultural_area=agricultural_area,
            vegetation_area=vegetation_area,
            agricultural_percentage=(agricultural_area / total * 100) if total > 0 else 0,
            vegetation_percentage=(vegetation_area / total * 100) if total > 0 else 0
        )
    
    @staticmethod
    def get_crop_distribution(db: Session) -> List[CropDistribution]:
        """Retorna a distribuicao por cultura"""
        # Busca area total por tipo de cultura
        crops = db.query(
            Crop.crop_type,
            func.sum(Crop.planted_area).label('total_area')
        ).group_by(Crop.crop_type).all()
        
        total = sum(c.total_area for c in crops) if crops else 0
        
        result = []
        for crop in crops:
            percentage = (crop.total_area / total * 100) if total > 0 else 0
            result.append(CropDistribution(
                crop_type=crop.crop_type.value,
                total_area=crop.total_area,
                percentage=percentage
            ))
        
        return result