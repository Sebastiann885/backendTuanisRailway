from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app import models, schemas, database
from app.database import get_db
from app.cache import init_redis  # 🔹 Nuevo: Redis
import os, json

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# --- Configuración JWT ---
SECRET_KEY = os.getenv("SECRET_KEY", "supersecreto123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# --- Dependencia de seguridad ---
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )


# --- ENDPOINTS PROTEGIDOS ---
@router.post("/", response_model=schemas.UsuarioOut)
def crear_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    if db.query(models.Usuario).filter_by(cedula=usuario.cedula).first():
        raise HTTPException(status_code=400, detail="La cédula ya existe")
    
    nuevo_usuario = models.Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # 🔹 Limpiar cache porque la lista de usuarios cambió
    # (mejor hacerlo con un patrón en Redis, ej: usuarios:*)
    # Aquí simplificamos borrando el listado completo
    import asyncio
    asyncio.create_task(invalidate_cache("usuarios:*"))

    return nuevo_usuario


@router.get("/", response_model=list[schemas.UsuarioOut])
async def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    redis = await init_redis()
    cache_key = "usuarios:all"

    # Buscar en cache
    if data := await redis.get(cache_key):
        return json.loads(data)

    # Consultar BD
    usuarios = db.query(models.Usuario).all()
    usuarios_dict = [schemas.UsuarioOut.from_orm(u).dict() for u in usuarios]

    # Guardar en cache por 60 segundos
    await redis.set(cache_key, json.dumps(usuarios_dict), ex=60)

    return usuarios_dict


@router.get("/{cedula}", response_model=schemas.UsuarioOut)
async def obtener_usuario(
    cedula: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    redis = await init_redis()
    cache_key = f"usuario:{cedula}"

    # Buscar en cache
    if data := await redis.get(cache_key):
        return json.loads(data)

    # Consultar BD
    usuario = db.query(models.Usuario).filter_by(cedula=cedula).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario_dict = schemas.UsuarioOut.from_orm(usuario).dict()

    # Guardar en cache por 60 segundos
    await redis.set(cache_key, json.dumps(usuario_dict), ex=60)

    return usuario_dict


@router.put("/{cedula}", response_model=schemas.UsuarioOut)
def actualizar_usuario(
    cedula: str,
    datos: schemas.UsuarioBase,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    usuario = db.query(models.Usuario).filter_by(cedula=cedula).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in datos.dict().items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)

    # 🔹 Invalida cache del usuario y lista
    import asyncio
    asyncio.create_task(invalidate_cache(f"usuario:{cedula}"))
    asyncio.create_task(invalidate_cache("usuarios:all"))

    return usuario


@router.delete("/{cedula}")
def eliminar_usuario(
    cedula: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    usuario = db.query(models.Usuario).filter_by(cedula=cedula).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    # 🔹 Invalida cache
    import asyncio
    asyncio.create_task(invalidate_cache(f"usuario:{cedula}"))
    asyncio.create_task(invalidate_cache("usuarios:all"))

    return {"mensaje": "Usuario eliminado correctamente"}


# --- Helper para limpiar cache ---
async def invalidate_cache(pattern: str):
    redis = await init_redis()
    keys = await redis.keys(pattern)
    if keys:
        await redis.delete(*keys)
