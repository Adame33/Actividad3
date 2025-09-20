from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import Optional, List, Dict, Any
from dao.tutoresdao import TutoresDAO
from models.tutoresModel import TutorCreate, TutorUpdate, TutorSalida, TutorOut
from routes.usuarios import validar_usuario  
# helper sesión
def get_session(request: Request):
    sess = getattr(request.app.state, "db_session", None)
    if not sess: raise HTTPException(status_code=500, detail="Sesión de BD no inicializada")
    return sess

router = APIRouter(prefix="/tutores/v1", tags=["Tutores"])

@router.post("/tutores", response_model=TutorSalida)
def crear_tutor(payload: TutorCreate, request: Request, _: bool = Depends(validar_usuario)):
    dao = TutoresDAO(get_session(request))
    res = dao.CrearTutorSP(payload)
    if not res.estatus: raise HTTPException(status_code=400, detail=res.message)
    return res

@router.patch("/tutores/{tutor_id}", response_model=TutorSalida)
def actualizar_tutor(tutor_id: str, payload: TutorUpdate, request: Request, _: bool = Depends(validar_usuario)):
    dao = TutoresDAO(get_session(request))
    res = dao.ActualizarTutorSP(tutor_id, payload)
    if not res.estatus: raise HTTPException(status_code=400, detail=res.message)
    return res

@router.get("/tutores/{tutor_id}", response_model=TutorSalida)
def obtener_tutor(tutor_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = TutoresDAO(get_session(request))
    return dao.ObtenerTutorPorIdSP(tutor_id)

@router.get("/tutores", response_model=List[TutorOut])
def listar_tutores(
    request: Request,
    q: Optional[str] = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = TutoresDAO(get_session(request))
    return dao.ListarTutoresSP(q=q, offset=offset, limit=limit)

@router.get("/tutores/{tutor_id}/webinars")
def listar_webinars_tutor(
    tutor_id: str,
    request: Request,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = TutoresDAO(get_session(request))
    return dao.ListarWebinarsPorTutorSP(tutor_id, offset=offset, limit=limit)

@router.get("/catalogo")
def catalogo_tutores(request: Request, _: bool = Depends(validar_usuario)):
    dao = TutoresDAO(get_session(request))
    return dao.CatalogoTutoresView()
