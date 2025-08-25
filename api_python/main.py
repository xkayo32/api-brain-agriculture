from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import uvicorn

from app.database import engine, Base
from app.controllers import producer_router, farm_router, dashboard_router
from app.controllers.auth_controller import router as auth_router
from app.controllers.harvest_controller import router as harvest_router
from app.controllers.crop_controller import router as crop_router
from app.config import config
from app.init_db import init_database

# Inicializar banco e criar usuario admin
init_database()

# Criar aplicacao
app = FastAPI(
    title="API de Produtores Rurais",
    description="Sistema para gerenciar produtores rurais e suas fazendas com autenticação JWT",
    version="2.0.0",
    swagger_ui_parameters={"persistAuthorization": True}
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar rotas
app.include_router(auth_router)
app.include_router(producer_router)
app.include_router(farm_router)
app.include_router(harvest_router)
app.include_router(crop_router)
app.include_router(dashboard_router)

# Rota de health check
@app.get("/health")
def health_check():
    return {"status": "OK"}

# Rota principal
@app.get("/")
def root():
    return {
        "message": "API de Produtores Rurais",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=True
    )