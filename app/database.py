from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import settings  # ✅ Usamos la clase Settings centralizada
from urllib.parse import quote_plus

# Escapamos caracteres especiales de la contraseña
password_encoded = quote_plus(settings.DB_PASSWORD)

DATABASE_URL = (
    f"mysql+mysqlconnector://{settings.DB_USER}:{password_encoded}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Configuración del engine con pool para mejor rendimiento
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # ✅ Evita conexiones muertas
    pool_size=10,         # ✅ Número de conexiones activas
    max_overflow=20       # ✅ Conexiones extra si hay carga alta
)

# Session local para usar en dependencias
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para inyección en endpoints
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

