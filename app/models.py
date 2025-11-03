from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)  # 👈 Adicionado campo de senha

    # Relacionamento com agendamentos
    agendamentos = relationship("Agendamento", back_populates="usuario")


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # Relacionamento reverso com o usuário
    usuario = relationship("Usuario", back_populates="agendamentos")
