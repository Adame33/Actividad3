from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel
from models.salida import Salida

class VistasWebinar(SQLModel, table=True):
    idVista: str = Field(primary_key=True, max_length=36)
    userId: str = Field(max_length=36, nullable=False)
    webinarId: str = Field(max_length=36, nullable=False)
    videoId: Optional[str] = Field(default=None, max_length=36)
    startedAt: Optional[str] = Field(default=None)
    lastSeenAt: Optional[str] = Field(default=None)
    posSeg: int = Field(default=0, nullable=False)
    completado: bool = Field(default=False, nullable=False)
    activo: bool = Field(default=True, nullable=False)

# DTOs
class PlayStart(BaseModel):
    userId: str
    webinarId: str
    videoId: str | None = None

class PlayUpdate(BaseModel):
    videoId: str | None = None
    posSeg: int | None = None

class PlaybackSalida(Salida):
    data: dict | None = None
