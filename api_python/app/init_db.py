"""
Script de inicializacao do banco de dados
Cria um usuario admin padrao se nao existir
"""
from sqlalchemy.orm import Session
from app.database import engine, Base
from app.models.user import User
from app.utils.security import get_password_hash
import time

def init_database():
    """Inicializa o banco e cria usuario admin padrao"""
    # Aguarda o banco estar pronto
    max_tries = 5
    for i in range(max_tries):
        try:
            # Criar todas as tabelas
            Base.metadata.create_all(bind=engine)
            
            # Criar sessao
            from app.database import SessionLocal
            db = SessionLocal()
            
            # Verificar se ja existe algum usuario
            existing_users = db.query(User).count()
            
            if existing_users == 0:
                # Criar usuario admin padrao
                admin_user = User(
                    username="admin",
                    email="admin@brazilagro.com",
                    hashed_password=get_password_hash("admin123"),
                    is_active=True,
                    is_admin=True
                )
                
                db.add(admin_user)
                db.commit()
                print("Usuario admin criado com sucesso!")
                print("Username: admin")
                print("Password: admin123")
            else:
                print(f"Banco ja inicializado com {existing_users} usuarios")
            
            db.close()
            
            # Carregar dados de exemplo
            from app.seed_data import seed_sample_data
            seed_sample_data()
            
            break
            
        except Exception as e:
            if i < max_tries - 1:
                print(f"Aguardando banco de dados... tentativa {i+1}/{max_tries}")
                time.sleep(5)
            else:
                print(f"Erro ao inicializar banco: {e}")
                raise

if __name__ == "__main__":
    init_database()