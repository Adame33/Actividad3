from sqlmodel import Session
from sqlalchemy import text
from typing import Optional, List, Dict, Any
from models.PlaybackModel import PlayStart, PlayUpdate, PlaybackSalida

class PlaybackDAO:
    def __init__(self, session: Session):
        self.session = session

    def StartSP(self, payload: PlayStart) -> PlaybackSalida:
        out = PlaybackSalida(message="Error al iniciar vista", estatus=False, data=None)
        try:
            stmt = text("CALL sp_play_start(:userId,:webinarId,:videoId)") \
                .bindparams(userId=payload.userId, webinarId=payload.webinarId, videoId=payload.videoId)
            res = self.session.exec(stmt)
            row = res.mappings().first()
            self.session.commit()
            if not row: out.message="SP no devolvió registro"; return out
            out.message, out.estatus, out.data = "Vista iniciada", True, dict(row)
        except Exception as e:
            self.session.rollback(); out.message=f"Error: {str(e)}"
        return out

    def UpdateSP(self, id_vista: str, payload: PlayUpdate) -> PlaybackSalida:
        out = PlaybackSalida(message="Error al actualizar vista", estatus=False, data=None)
        try:
            stmt = text("CALL sp_play_update(:idVista,:videoId,:posSeg)") \
                .bindparams(idVista=id_vista, videoId=payload.videoId, posSeg=payload.posSeg)
            res = self.session.exec(stmt)
            row = res.mappings().first()
            self.session.commit()
            if not row: out.message="Vista no encontrada"; return out
            out.message, out.estatus, out.data = "Vista actualizada", True, dict(row)
        except Exception as e:
            self.session.rollback(); out.message=f"Error: {str(e)}"
        return out

    def CompleteSP(self, id_vista: str) -> PlaybackSalida:
        out = PlaybackSalida(message="Error al completar vista", estatus=False, data=None)
        try:
            stmt = text("CALL sp_play_complete(:idVista)").bindparams(idVista=id_vista)
            res = self.session.exec(stmt)
            row = res.mappings().first()
            self.session.commit()
            if not row: out.message="Vista no encontrada"; return out
            out.message, out.estatus, out.data = "Vista completada", True, dict(row)
        except Exception as e:
            self.session.rollback(); out.message=f"Error: {str(e)}"
        return out

    def StopSP(self, id_vista: str) -> PlaybackSalida:
        out = PlaybackSalida(message="Error al detener vista", estatus=False, data=None)
        try:
            stmt = text("CALL sp_play_stop(:idVista)").bindparams(idVista=id_vista)
            res = self.session.exec(stmt)
            row = res.mappings().first()
            self.session.commit()
            if not row: out.message="Vista no encontrada"; return out
            out.message, out.estatus, out.data = "Vista detenida", True, dict(row)
        except Exception as e:
            self.session.rollback(); out.message=f"Error: {str(e)}"
        return out

    def SwitchVideoSP(self, id_vista: str, new_video_id: str) -> PlaybackSalida:
        out = PlaybackSalida(message="Error al cambiar video", estatus=False, data=None)
        try:
            stmt = text("CALL sp_play_switch_video(:idVista,:videoId)") \
                .bindparams(idVista=id_vista, videoId=new_video_id)
            res = self.session.exec(stmt)
            row = res.mappings().first()
            self.session.commit()
            if not row: out.message="Vista no encontrada"; return out
            out.message, out.estatus, out.data = "Video cambiado", True, dict(row)
        except Exception as e:
            self.session.rollback(); out.message=f"Error: {str(e)}"
        return out

    def ListByUserSP(self, user_id: str, offset: int = 0, limit: int = 50):
        stmt = text("CALL sp_play_list_by_user(:uid,:offset,:limit)") \
            .bindparams(uid=user_id, offset=offset, limit=limit)
        res = self.session.exec(stmt)
        return res.mappings().all()

    def GetByIdSP(self, id_vista: str):
        stmt = text("CALL sp_play_get_by_id(:id)").bindparams(id=id_vista)
        res = self.session.exec(stmt)
        return res.mappings().first()

    # ---------- VISTAS ----------
    def VistasDetalleView(self, q: Optional[str] = None, userId: Optional[str] = None,
                          webinarId: Optional[str] = None, videoId: Optional[str] = None,
                          activo: Optional[bool] = None, completado: Optional[bool] = None,
                          offset: int = 0, limit: int = 50):
        where, params = ["1=1"], {"offset": offset, "limit": limit}
        if q: where.append("(username LIKE :q OR webinar LIKE :q OR video LIKE :q)"); params["q"]=f"%{q}%"
        if userId: where.append("userId = :userId"); params["userId"]=userId
        if webinarId: where.append("webinarId = :webinarId"); params["webinarId"]=webinarId
        if videoId: where.append("videoId = :videoId"); params["videoId"]=videoId
        if activo is not None: where.append("activo = :activo"); params["activo"]=int(activo)
        if completado is not None: where.append("completado = :completado"); params["completado"]=int(completado)

        sql = f"""
          SELECT * FROM vw_vistas_detalle
          WHERE {' AND '.join(where)}
          ORDER BY startedAt DESC
          LIMIT :offset, :limit
        """
        res = self.session.exec(text(sql).bindparams(**params))
        return res.mappings().all()

    def VistaActivaPorUsuarioView(self, user_id: str):
        stmt = text("SELECT * FROM vw_vista_activa_por_usuario WHERE userId = :uid LIMIT 1") \
            .bindparams(uid=user_id)
        res = self.session.exec(stmt)
        return res.mappings().first()

    def MetricasWebinarView(self, q: Optional[str] = None, offset: int = 0, limit: int = 50):
        where, params = ["1=1"], {"offset": offset, "limit": limit}
        if q: where.append("webinar LIKE :q"); params["q"]=f"%{q}%"
        sql = f"""
          SELECT * FROM vw_metricas_webinar
          WHERE {' AND '.join(where)}
          ORDER BY watchTime_aprox_seg DESC
          LIMIT :offset, :limit
        """
        res = self.session.exec(text(sql).bindparams(**params))
        return res.mappings().all()
