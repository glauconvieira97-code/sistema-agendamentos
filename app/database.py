from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./app.db"

# Cria a conexão com o banco SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Cria sessões do banco para uso nas rotas
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base usada pelos modelos
Base = declarative_base()
