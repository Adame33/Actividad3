# routes/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, Request , Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dao.UsuarioDao import UsuariosDAO
from models.UsuarioModel import UsuarioCreate, UsuarioSalida , UsuarioChangePassword, UsuarioQuery , UsuarioUpdate, UsuarioOut
from typing import List, Optional

router = APIRouter(prefix="/usuarios")
security = HTTPBasic()

def get_session(request: Request):
    sess = getattr(request.app.state, "db_session", None)
    if not sess:
        raise HTTPException(status_code=500, detail="Sesión de BD no inicializada")
    return sess

def validar_usuario(request: Request, credentials: HTTPBasicCredentials = Depends(security)) -> bool:
    dao = UsuariosDAO(get_session(request))
    auth = dao.autenticar(credentials.username, credentials.password)  # aquí usas hash en Basic
    if not auth.estatus:
        raise HTTPException(status_code=401, detail="No autorizado")
    return True

@router.post("/register", response_model=UsuarioSalida)
def register(payload: UsuarioCreate, request: Request):
    dao = UsuariosDAO(get_session(request))
    res = dao.CrearUsuarioSP(payload)
    if not res.estatus:
        raise HTTPException(status_code=400, detail=res.message)
    return res

@router.post("/login", response_model=UsuarioSalida)
def login(username: str, passwordHash: str, request: Request):
    dao = UsuariosDAO(get_session(request))
    res = dao.autenticar(username, passwordHash)
    if not res.estatus:
        raise HTTPException(status_code=401, detail=res.message)
    return res


@router.patch("/usuarios/{user_id}/password", response_model=UsuarioSalida)
def cambiar_password(user_id: str, payload: UsuarioChangePassword, request: Request, _: bool = Depends(validar_usuario)):
    dao = UsuariosDAO(get_session(request))
    res = dao.CambiarPasswordSP(user_id, payload.newPasswordHash)
    if not res.estatus:
        raise HTTPException(status_code=400, detail=res.message)
    return res

@router.patch("/usuarios/{user_id}/deactivate", response_model=UsuarioSalida)
def desactivar_usuario(user_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = UsuariosDAO(get_session(request))
    res = dao.DesactivarUsuarioSP(user_id)
    if not res.estatus:
        raise HTTPException(status_code=400, detail=res.message)
    return res

@router.get("/usuarios", response_model=List[UsuarioOut])
def listar_usuarios(
    request: Request,
    q: Optional[str] = Query(default=None),
    active: Optional[bool] = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = UsuariosDAO(get_session(request))
    return dao.ListarUsuariosSP(q=q, active=active, offset=offset, limit=limit)


@router.get("/usuarios/{user_id}", response_model=UsuarioSalida)
def obtener_usuario_por_id(user_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = UsuariosDAO(get_session(request))
    return dao.ObtenerUsuarioPorIdSP(user_id)


@router.patch("/usuarios/{user_id}", response_model=UsuarioSalida)
def Actualizar_Usuario(user_id: str, payload: UsuarioUpdate, request: Request, _: bool = Depends(validar_usuario)):
    dao = UsuariosDAO(get_session(request))
    res = dao.ActualizarUsuarioSP(user_id, payload)
    if not res.estatus:
        raise HTTPException(status_code=400, detail=res.message)
    return res