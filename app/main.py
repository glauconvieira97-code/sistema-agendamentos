from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.routes import router
from app.database import engine
from app import models

# Criação das tabelas no banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Sessões via cookie (autenticação simples)
app.add_middleware(SessionMiddleware, secret_key="chave-supersecreta")

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir rotas
app.include_router(router)
