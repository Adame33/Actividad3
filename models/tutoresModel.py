from sqlmodel import SQLModel, Field
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from models.salida import Salida

class Tutores(SQLModel, table=True):
    idTutor: str = Field(primary_key=True, max_length=36)
    nombre: str = Field(max_length=150, nullable=False)
    mail: str = Field(max_length=150, nullable=False)
    foto: Optional[str] = Field(default=None, max_length=250)
    puesto: Optional[str] = Field(default=None, max_length=150)
    urlLinkedin: Optional[str] = Field(default=None, max_length=250)

class TutorCreate(BaseModel):
    nombre: str
    mail: EmailStr
    foto: Optional[str] = None
    puesto: Optional[str] = None
    urlLinkedin: Optional[str] = None

class TutorUpdate(BaseModel):
    nombre: Optional[str] = None
    mail: Optional[EmailStr] = None
    foto: Optional[str] = None
    puesto: Optional[str] = None
    urlLinkedin: Optional[str] = None

class TutorOut(BaseModel):
    idTutor: str
    nombre: str
    mail: str
    foto: Optional[str] = None
    puesto: Optional[str] = None
    urlLinkedin: Optional[str] = None

class TutorSalida(Salida):
    data: Optional[TutorOut] = None
