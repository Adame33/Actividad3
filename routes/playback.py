from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import Optional
from dao.playbackdao import PlaybackDAO
from models.PlaybackModel import PlayStart, PlayUpdate, PlaybackSalida
from routes.usuarios import validar_usuario

def get_session(request: Request):
    sess = getattr(request.app.state, "db_session", None)
    if not sess: raise HTTPException(status_code=500, detail="Sesión de BD no inicializada")
    return sess

router = APIRouter(prefix="/playback/v1", tags=["Playback"])

# ---- SPs ----
@router.post("/start", response_model=PlaybackSalida)
def play_iniciar(payload: PlayStart, request: Request, _: bool = Depends(validar_usuario)):
    dao = PlaybackDAO(get_session(request))
    return dao.StartSP(payload)

@router.patch("/views/{vista_id}/update", response_model=PlaybackSalida)
def play_actualizar(vista_id: str, payload: PlayUpdate, request: Request, _: bool = Depends(validar_usuario)):
    dao = PlaybackDAO(get_session(request))
    return dao.UpdateSP(vista_id, payload)

@router.post("/views/{vista_id}/complete", response_model=PlaybackSalida)
def play_completar(vista_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = PlaybackDAO(get_session(request))
    return dao.CompleteSP(vista_id)

@router.post("/views/{vista_id}/stop", response_model=PlaybackSalida)
def play_detener(vista_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = PlaybackDAO(get_session(request))
    return dao.StopSP(vista_id)

@router.post("/views/{vista_id}/switch/{video_id}", response_model=PlaybackSalida)
def play_cambiar_video(vista_id: str, video_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = PlaybackDAO(get_session(request))
    return dao.SwitchVideoSP(vista_id, video_id)

@router.get("/users/{user_id}/views")
def play_lista_del_usuario(user_id: str, request: Request,
                      offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200),
                      _: bool = Depends(validar_usuario)):
    dao = PlaybackDAO(get_session(request))
    return dao.ListByUserSP(user_id, offset, limit)

@router.get("/views/{vista_id}")
def play_obtener_por_id(vista_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = PlaybackDAO(get_session(request))
    row = dao.GetByIdSP(vista_id)
    if not row: raise HTTPException(status_code=404, detail="Vista no encontrada")
    return row


@router.get("/vistas-detalle")
def vistas_detalle(
    request: Request,
    q: Optional[str] = Query(default=None),
    userId: Optional[str] = Query(default=None),
    webinarId: Optional[str] = Query(default=None),
    videoId: Optional[str] = Query(default=None),
    activo: Optional[bool] = Query(default=None),
    completado: Optional[bool] = Query(default=None),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = PlaybackDAO(get_session(request))
    return dao.VistasDetalleView(q, userId, webinarId, videoId, activo, completado, offset, limit)

@router.get("/vista-activa/{user_id}")
def vista_activa(user_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = PlaybackDAO(get_session(request))
    row = dao.VistaActivaPorUsuarioView(user_id)
    if not row: raise HTTPException(status_code=404, detail="Sin vista activa")
    return row

@router.get("/metricas-webinar")
def metricas_webinar(
    request: Request,
    q: Optional[str] = Query(default=None),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = PlaybackDAO(get_session(request))
    return dao.MetricasWebinarView(q=q, offset=offset, limit=limit)
