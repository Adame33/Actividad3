from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel
from models.salida import Salida

class Videos(SQLModel, table=True):
    idVideo: str = Field(primary_key=True, max_length=36)
    idWebinar: str = Field(max_length=36, nullable=False)
    titulo: str = Field(max_length=200, nullable=False)
    duracionSeg: int = Field(default=0, nullable=False)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    url: Optional[str] = Field(default=None, max_length=250)
    libre: bool = Field(default=True, nullable=False)
    miniatura: Optional[str] = Field(default=None, max_length=250)

class VideoCreate(BaseModel):
    idWebinar: str
    titulo: str
    duracionSeg: Optional[int] = 0
    descripcion: Optional[str] = None
    url: Optional[str] = None
    libre: Optional[bool] = True
    miniatura: Optional[str] = None

class VideoUpdate(BaseModel):
    titulo: Optional[str] = None
    duracionSeg: Optional[int] = None
    descripcion: Optional[str] = None
    url: Optional[str] = None
    libre: Optional[bool] = None
    miniatura: Optional[str] = None

class VideoOut(BaseModel):
    idVideo: str
    idWebinar: str
    titulo: str
    duracionSeg: int
    descripcion: Optional[str] = None
    url: Optional[str] = None
    libre: bool
    miniatura: Optional[str] = None

class VideoQuery(BaseModel):
    q: Optional[str] = None
    idWebinar: Optional[str] = None
    libre: Optional[bool] = None
    offset: int = 0
    limit: int = 50

class VideoSalida(Salida):
    data: Optional[VideoOut] = None
