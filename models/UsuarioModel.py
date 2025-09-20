# models/UsuarioModel.py
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr
from typing import Optional
from models.salida import Salida

# Modelo de tabla (BD)
class Usuarios(SQLModel, table=True):
    idUsuario: str = Field(primary_key=True, max_length=36)
    username: str = Field(max_length=100, nullable=False, unique=True)
    passwordHash: str = Field(max_length=255, nullable=False)
    mail: Optional[str] = Field(default=None, max_length=150, nullable=True)
    isActive: bool = Field(default=True, nullable=False)
    createdAt: Optional[str] = Field(default=None, nullable=True)

# ===== DTOs =====
# Entrada para crear
class UsuarioCreate(BaseModel):
    username: str
    passwordHash: str
    mail: Optional[EmailStr] = None

# Salida segura (sin passwordHash)
class UsuarioOut(BaseModel):
    idUsuario: str
    username: str
    mail: Optional[str] = None
    isActive: bool
    createdAt: Optional[str] = None

class UsuarioQuery(BaseModel):
    q: Optional[str] = None
    active: Optional[bool] = None
    offset: int = 0
    limit: int = 50

class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    mail: Optional[EmailStr] = None
    isActive: Optional[bool] = None


class UsuarioChangePassword(BaseModel):
    newPasswordHash: str

class UsuarioSalida(Salida):
    data: Optional[UsuarioOut] = None


