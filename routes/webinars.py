from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import Optional, List, Dict, Any

from uuid import UUID

from dao.webinarsdao import WebinarsDAO
from models.WebinarModel import WebinarCreate, WebinarUpdate, WebinarSalida, WebinarOut
from routes.usuarios import validar_usuario


def get_session(request: Request):
    sess = getattr(request.app.state, "db_session", None)
    if not sess: raise HTTPException(status_code=500, detail="Sesión de BD no inicializada")
    return sess

router = APIRouter(prefix="/webinars/v1", tags=["Webinars"])

@router.post("/webinars", response_model=WebinarSalida)
def crear_webinar(payload: WebinarCreate, request: Request, _: bool = Depends(validar_usuario)):
    dao = WebinarsDAO(get_session(request))
    res = dao.CrearWebinarSP(payload)
    if not res.estatus: raise HTTPException(status_code=400, detail=res.message)
    return res
@router.get("/webinars/resumen")
def obtener_Resumen_Webinar(request: Request, _: bool = Depends(validar_usuario)):
    dao = WebinarsDAO(get_session(request))
    return dao.ListarResumenView()

@router.patch("/webinars/{webinar_id}", response_model=WebinarSalida)
def actualizar_webinar(webinar_id: str, payload: WebinarUpdate, request: Request, _: bool = Depends(validar_usuario)):
    dao = WebinarsDAO(get_session(request))
    res = dao.ActualizarWebinarSP(webinar_id, payload)
    if not res.estatus: raise HTTPException(status_code=400, detail=res.message)
    return res

@router.get("/webinars/{webinar_id}", response_model=WebinarSalida)
def obtener_webinar(webinar_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = WebinarsDAO(get_session(request))
    return dao.ObtenerWebinarPorIdSP(webinar_id)

@router.get("/webinars", response_model=List[WebinarOut])
def listar_webinars(
    request: Request,
    q: Optional[str] = Query(default=None),
    categoria: Optional[str] = Query(default=None),
    contenidoLibre: Optional[bool] = Query(default=None),
    tutorId: Optional[str] = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = WebinarsDAO(get_session(request))
    return dao.ListarWebinarsSP(q, categoria, contenidoLibre, tutorId, offset, limit)


@router.get("/webinars/{webinar_id}/videos")
def listar_videos_de_webinar(
    webinar_id: UUID,
    request: Request,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = WebinarsDAO(get_session(request))
    return dao.ListarVideosDeWebinarSP(str(webinar_id), offset, limit)

@router.get("/videos")
def obtener_videos_con_webinar(
    request: Request,
    webinarId: str | None = Query(default=None),
    _: bool = Depends(validar_usuario)
):
    dao = WebinarsDAO(get_session(request))
    return dao.ListarVideosConWebinarView(webinarId)