from .producer_controller import router as producer_router
from .farm_controller import router as farm_router
from .dashboard_controller import router as dashboard_router

__all__ = ["producer_router", "farm_router", "dashboard_router"]