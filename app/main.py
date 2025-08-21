from fastapi import FastAPI
from app.database import engine, Base
from starlette.middleware.sessions import SessionMiddleware
from app.routes import usuarios, auth
from app.models import Usuario
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar app primero
app = FastAPI()

# Middleware de sesión requerido por Authlib
app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SESSION_SECRET_KEY", "super-secret-key")
)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(usuarios.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "API Tuanis Roleplay funcionando 🚀"}