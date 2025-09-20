from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel
from models.salida import Salida

class MaterialApoyo(SQLModel, table=True):
    idMaterial: str = Field(primary_key=True, max_length=36)
    idVideo: str = Field(max_length=36, nullable=False)
    nombre: str = Field(max_length=200, nullable=False)
    url: str = Field(max_length=500, nullable=False)
    descargas: int = Field(default=0, nullable=False)
    free: bool = Field(default=False, nullable=False)

class MaterialCreate(BaseModel):
    idVideo: str
    nombre: str
    url: str
    free: Optional[bool] = False

class MaterialUpdate(BaseModel):
    nombre: Optional[str] = None
    url: Optional[str] = None
    free: Optional[bool] = None

class MaterialOut(BaseModel):
    idMaterial: str
    idVideo: str
    nombre: str
    url: str
    descargas: int
    free: bool

class MaterialSalida(Salida):
    data: Optional[MaterialOut] = None
