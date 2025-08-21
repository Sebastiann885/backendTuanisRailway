from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

from app.database import get_db
from app.models import AuthUser
from app.schemas import AuthUserCreate, AuthUserOut

router = APIRouter(prefix="/auth", tags=["Auth"])

# --- Configuración JWT ---
SECRET_KEY = os.getenv("SECRET_KEY", "supersecreto123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Utilidades ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Endpoints ---
@router.post("/register", response_model=AuthUserOut)
def register(user_in: AuthUserCreate, db: Session = Depends(get_db)):
    # ¿Usuario ya existe?
    if db.query(AuthUser).filter(AuthUser.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    if db.query(AuthUser).filter(AuthUser.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email ya en uso")

    hashed_password = get_password_hash(user_in.password)
    new_user = AuthUser(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(AuthUser).filter(AuthUser.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=AuthUserOut)
def profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = db.query(AuthUser).filter(AuthUser.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")