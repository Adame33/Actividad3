from pydantic import BaseModel

class Salida(BaseModel):
    message: str
    estatus: bool