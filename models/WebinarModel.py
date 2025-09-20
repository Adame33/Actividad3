from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel
from models.salida import Salida

class Webinars(SQLModel, table=True):
    idWebinar: str = Field(primary_key=True, max_length=36)
    nombre: str = Field(max_length=200, nullable=False)
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    categoria: Optional[str] = Field(default="default", max_length=100)
    dificultad: Optional[str] = Field(default=None, max_length=50)
    imagen: Optional[str] = Field(default=None, max_length=250)
    contenidoLibre: bool = Field(default=True, nullable=False)
    totalVideos: int = Field(default=0, nullable=False)
    tutorId: Optional[str] = Field(default=None, max_length=36)

class WebinarCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = "default"
    dificultad: Optional[str] = None
    imagen: Optional[str] = None
    contenidoLibre: Optional[bool] = True
    tutorId: Optional[str] = None

class WebinarUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    dificultad: Optional[str] = None
    imagen: Optional[str] = None
    contenidoLibre: Optional[bool] = None

class WebinarOut(BaseModel):
    idWebinar: str
    nombre: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    dificultad: Optional[str] = None
    imagen: Optional[str] = None
    contenidoLibre: bool
    totalVideos: int
    tutorId: Optional[str] = None

class WebinarQuery(BaseModel):
    q: Optional[str] = None
    categoria: Optional[str] = None
    contenidoLibre: Optional[bool] = None
    tutorId: Optional[str] = None
    offset: int = 0
    limit: int = 50

class WebinarSalida(Salida):
    data: Optional[WebinarOut] = None
