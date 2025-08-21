from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated
from datetime import date

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    nacionalidad: str
    estatura: str
    fecha_nacimiento: date
    edad: int
    cedula: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
        
class AuthUserBase(BaseModel):
    username: str
    email: EmailStr

class AuthUserCreate(AuthUserBase):
    password: Annotated[str, StringConstraints(min_length=8)] 

class AuthUserOut(AuthUserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
