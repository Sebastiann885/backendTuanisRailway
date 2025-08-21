from sqlalchemy import Column, Integer, String, Date, Boolean
from app.database import Base

# Tabla de usuarios de rolplay
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    nacionalidad = Column(String(50), nullable=False)
    estatura = Column(String(10), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    edad = Column(Integer, nullable=False)
    cedula = Column(String(20), unique=True, index=True, nullable=False)

# Tabla de autenticación
class AuthUser(Base):
    __tablename__ = "usuarios_auth"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)