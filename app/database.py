from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados PostgreSQL na Render
SQLALCHEMY_DATABASE_URL = "postgresql://admin:gCyxmquugd2CQnyslHz0axYXCnhZXcna@dpg-d44kd2mmcj7s73aode70-a.oregon-postgres.render.com/agendamentos_guj7"

# Criação do engine e da sessão com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM
Base = declarative_base()
