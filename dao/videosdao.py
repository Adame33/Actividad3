from sqlmodel import Session
from sqlalchemy import text
from typing import List, Optional, Dict, Any
from models.VideoModel import VideoCreate, VideoUpdate, VideoOut, VideoSalida

def _row_to_video_out(row) -> VideoOut:
    return VideoOut(
        idVideo=str(row.get("idVideo")),
        idWebinar=str(row.get("idWebinar")),
        titulo=str(row.get("titulo")),
        duracionSeg=int(row.get("duracionSeg")),
        descripcion=row.get("descripcion"),
        url=row.get("url"),
        libre=bool(row.get("libre")),
        miniatura=row.get("miniatura"),
    )

class VideosDAO:
    def __init__(self, session: Session):
        self.session = session

    def CrearVideoSP(self, payload: VideoCreate) -> VideoSalida:
        salida = VideoSalida(message="Error al crear video", estatus=False, data=None)
        try:
            stmt = text("""
                CALL sp_create_video(:idWebinar,:titulo,:duracionSeg,:descripcion,:url,:libre,:miniatura)
            """).bindparams(
                idWebinar=payload.idWebinar, titulo=payload.titulo,
                duracionSeg=payload.duracionSeg, descripcion=payload.descripcion,
                url=payload.url, libre=payload.libre, miniatura=payload.miniatura
            )
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row: salida.message="SP no devolvió registro"; return salida
            salida.message, salida.estatus, salida.data = "Video creado", True, _row_to_video_out(row)
        except Exception as e:
            self.session.rollback(); salida.message=f"Error: {str(e)}"
        return salida

    def ActualizarVideoSP(self, id_video: str, payload: VideoUpdate) -> VideoSalida:
        salida = VideoSalida(message="Error al actualizar video", estatus=False, data=None)
        try:
            stmt = text("""
                CALL sp_update_video(:id,:titulo,:duracionSeg,:descripcion,:url,:libre,:miniatura)
            """).bindparams(
                id=id_video, titulo=payload.titulo, duracionSeg=payload.duracionSeg,
                descripcion=payload.descripcion, url=payload.url,
                libre=payload.libre, miniatura=payload.miniatura
            )
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row: salida.message="Video no encontrado"; return salida
            salida.message, salida.estatus, salida.data = "Video actualizado", True, _row_to_video_out(row)
        except Exception as e:
            self.session.rollback(); salida.message=f"Error: {str(e)}"
        return salida

    def ObtenerVideoPorIdSP(self, id_video: str) -> VideoSalida:
        salida = VideoSalida(message="Error al obtener video", estatus=False, data=None)
        try:
            stmt = text("CALL sp_get_video_by_id(:id)").bindparams(id=id_video)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            if not row: salida.message="Video no encontrado"; return salida
            salida.message, salida.estatus, salida.data = "OK", True, _row_to_video_out(row)
        except Exception as e:
            salida.message=f"Error: {str(e)}"
        return salida

    def ListarVideosSP(self, q: Optional[str], idWebinar: Optional[str],
                       libre: Optional[bool], offset: int=0, limit: int=50) -> List[VideoOut]:
        stmt = text("""
            CALL sp_list_videos(:q,:idWebinar,:libre,:offset,:limit)
        """).bindparams(q=q, idWebinar=idWebinar, libre=libre, offset=offset, limit=limit)
        result = self.session.exec(stmt)
        rows = result.mappings().all()
        return [_row_to_video_out(r) for r in rows]

    def ReasignarVideoSP(self, id_video: str, id_webinar: str) -> VideoSalida:
        salida = VideoSalida(message="Error al reasignar video", estatus=False, data=None)
        try:
            stmt = text("CALL sp_attach_video_to_webinar(:idVideo,:idWebinar)") \
                .bindparams(idVideo=id_video, idWebinar=id_webinar)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row: salida.message="Video no encontrado"; return salida
            salida.message, salida.estatus, salida.data = "Video reasignado", True, _row_to_video_out(row)
        except Exception as e:
            self.session.rollback(); salida.message=f"Error: {str(e)}"
        return salida

    
    def ListarVideosConWebinarView(self, id_webinar: str | None = None):
        if id_webinar:
            stmt = text("SELECT * FROM vw_videos_con_webinar WHERE idWebinar=:id ORDER BY video").bindparams(id=id_webinar)
        else:
            stmt = text("SELECT * FROM vw_videos_con_webinar ORDER BY webinar, video")
        result = self.session.exec(stmt)
        return result.mappings().all()


    
    def CatalogoVideosView(self):
        result = self.session.exec(text("SELECT * FROM vw_catalogo_videos "))
        return result.mappings().all()

    
    def MetricasVideoView(self, q: str | None = None, webinarId: str | None = None,
                        offset: int = 0, limit: int = 50):
        where, params = ["1=1"], {"offset": offset, "limit": limit}
        if q:
            where.append("(video LIKE :q OR webinar LIKE :q)")
            params["q"] = f"%{q}%"
        if webinarId:
            where.append("webinarId = :webinarId")
            params["webinarId"] = webinarId
        sql = f"""
        SELECT * FROM vw_metricas_video
        WHERE {' AND '.join(where)}
        LIMIT :offset, :limit
        """
        result = self.session.exec(text(sql).bindparams(**params))
        return result.mappings().all()
