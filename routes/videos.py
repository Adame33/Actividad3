from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import Optional, List
from dao.videosdao import VideosDAO
from models.VideoModel import VideoCreate, VideoUpdate, VideoSalida, VideoOut
from routes.usuarios import validar_usuario

def get_session(request: Request):
    sess = getattr(request.app.state, "db_session", None)
    if not sess: raise HTTPException(status_code=500, detail="Sesión de BD no inicializada")
    return sess

router = APIRouter(prefix="/videos/v1", tags=["Videos"])

@router.post("/videos", response_model=VideoSalida)
def crear_video(payload: VideoCreate, request: Request, _: bool = Depends(validar_usuario)):
    dao = VideosDAO(get_session(request))
    res = dao.CrearVideoSP(payload)
    if not res.estatus: raise HTTPException(status_code=400, detail=res.message)
    return res

@router.patch("/videos/{video_id}", response_model=VideoSalida)
def actualizar_video(video_id: str, payload: VideoUpdate, request: Request, _: bool = Depends(validar_usuario)):
    dao = VideosDAO(get_session(request))
    res = dao.ActualizarVideoSP(video_id, payload)
    if not res.estatus: raise HTTPException(status_code=400, detail=res.message)
    return res

@router.get("/videos/{video_id}", response_model=VideoSalida)
def obtener_video(video_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = VideosDAO(get_session(request))
    return dao.ObtenerVideoPorIdSP(video_id)

@router.get("/videos", response_model=List[VideoOut])
def listar_videos(
    request: Request,
    q: Optional[str] = Query(default=None),
    idWebinar: Optional[str] = Query(default=None),
    libre: Optional[bool] = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = VideosDAO(get_session(request))
    return dao.ListarVideosSP(q, idWebinar, libre, offset, limit)

@router.post("/videos/{video_id}/attach/{webinar_id}", response_model=VideoSalida)
def reasignar_video(video_id: str, webinar_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = VideosDAO(get_session(request))
    res = dao.ReasignarVideoSP(video_id, webinar_id)
    if not res.estatus: raise HTTPException(status_code=400, detail=res.message)
    return res

# vista: videos + webinar/tutor
@router.get("/videos-con-webinar")
def videos_con_webinar(request: Request, webinarId: Optional[str] = Query(default=None), _: bool = Depends(validar_usuario)):
    dao = VideosDAO(get_session(request))
    return dao.ListarVideosConWebinarView(webinarId)

@router.get("/catalogo")
def catalogo_videos(request: Request, _: bool = Depends(validar_usuario)):
    dao = VideosDAO(get_session(request))
    return dao.CatalogoVideosView()

@router.get("/metricas")
def metricas_video(
    request: Request,
    q: str | None = Query(default=None),
    webinarId: str | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = VideosDAO(get_session(request))
    return dao.MetricasVideoView(q=q, webinarId=webinarId, offset=offset, limit=limit)
