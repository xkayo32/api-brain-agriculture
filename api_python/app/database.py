from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import config

# Criar engine do banco
engine = create_engine(config.DATABASE_URL)

# Criar sessao
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Funcao para pegar a sessao do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()