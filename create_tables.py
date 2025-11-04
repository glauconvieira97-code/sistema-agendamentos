from app.database import Base, engine
from app import models

# Cria as tabelas no banco com base nos modelos definidos
Base.metadata.create_all(bind=engine)

print("✅ Tabelas criadas com sucesso no banco PostgreSQL!")
