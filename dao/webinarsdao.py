from sqlmodel import Session
from sqlalchemy import text
from typing import List, Optional
from models.WebinarModel import WebinarCreate, WebinarUpdate, WebinarOut, WebinarSalida

def _row_to_webinar_out(row) -> WebinarOut:
    return WebinarOut(
        idWebinar=str(row.get("idWebinar")),
        nombre=str(row.get("nombre")),
        descripcion=row.get("descripcion"),
        categoria=row.get("categoria"),
        dificultad=row.get("dificultad"),
        imagen=row.get("imagen"),
        contenidoLibre=bool(row.get("contenidoLibre")),
        totalVideos=int(row.get("totalVideos")),
        tutorId=row.get("tutorId"),
    )

class WebinarsDAO:
    def __init__(self, session: Session):
        self.session = session

    def CrearWebinarSP(self, payload: WebinarCreate) -> WebinarSalida:
        salida = WebinarSalida(message="Error al crear webinar", estatus=False, data=None)
        try:
            stmt = text("""
                CALL sp_create_webinar(:nombre,:descripcion,:categoria,:dificultad,:imagen,:contenidoLibre,:tutorId)
            """).bindparams(
                nombre=payload.nombre,
                descripcion=payload.descripcion,
                categoria=payload.categoria,
                dificultad=payload.dificultad,
                imagen=payload.imagen,
                contenidoLibre=payload.contenidoLibre,
                tutorId=payload.tutorId
            )
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row: salida.message = "SP no devolvió registro"; return salida
            salida.message, salida.estatus, salida.data = "Webinar creado", True, _row_to_webinar_out(row)
        except Exception as e:
            self.session.rollback(); salida.message = f"Error: {str(e)}"
        return salida

    def ActualizarWebinarSP(self, id_webinar: str, payload: WebinarUpdate) -> WebinarSalida:
        salida = WebinarSalida(message="Error al actualizar webinar", estatus=False, data=None)
        try:
            stmt = text("""
                CALL sp_update_webinar(:id,:nombre,:descripcion,:categoria,:dificultad,:imagen,:contenidoLibre)
            """).bindparams(
                id=id_webinar,
                nombre=payload.nombre,
                descripcion=payload.descripcion,
                categoria=payload.categoria,
                dificultad=payload.dificultad,
                imagen=payload.imagen,
                contenidoLibre=payload.contenidoLibre
            )
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row: salida.message = "Webinar no encontrado"; return salida
            salida.message, salida.estatus, salida.data = "Webinar actualizado", True, _row_to_webinar_out(row)
        except Exception as e:
            self.session.rollback(); salida.message = f"Error: {str(e)}"
        return salida

    def ObtenerWebinarPorIdSP(self, id_webinar: str) -> WebinarSalida:
        salida = WebinarSalida(message="Error al obtener webinar", estatus=False, data=None)
        try:
            stmt = text("CALL sp_get_webinar_by_id(:id)").bindparams(id=id_webinar)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            if not row: salida.message = "Webinar no encontrado"; return salida
            salida.message, salida.estatus, salida.data = "OK", True, _row_to_webinar_out(row)
        except Exception as e:
            salida.message = f"Error: {str(e)}"
        return salida

    def ListarWebinarsSP(self, q: Optional[str], categoria: Optional[str], contenidoLibre: Optional[bool],
                         tutorId: Optional[str], offset: int = 0, limit: int = 50) -> List[WebinarOut]:
        stmt = text("""
            CALL sp_list_webinars(:q,:categoria,:contenidoLibre,:tutorId,:offset,:limit)
        """).bindparams(
            q=q, categoria=categoria, contenidoLibre=contenidoLibre,
            tutorId=tutorId, offset=offset, limit=limit
        )
        result = self.session.exec(stmt)
        rows = result.mappings().all()
        return [_row_to_webinar_out(r) for r in rows]

    def ListarVideosDeWebinarSP(self, id_webinar: str, offset: int = 0, limit: int = 50):
        stmt = text("CALL sp_list_videos_by_webinar(:id,:offset,:limit)") \
            .bindparams(id=id_webinar, offset=offset, limit=limit)
        result = self.session.exec(stmt)
        return result.mappings().all()

    def ListarResumenView(self):
        result = self.session.exec(text("SELECT * FROM vw_webinars_resumen"))
        print(result)
        return result.mappings().all()
    
    def ListarVideosConWebinarView(self, id_webinar: str | None = None):
        if id_webinar:
            stmt = text("SELECT * FROM vw_videos_con_webinar WHERE idWebinar = :id ORDER BY video").bindparams(id=id_webinar)
        else:
            stmt = text("SELECT * FROM vw_videos_con_webinar ORDER BY webinar, video")
        result = self.session.exec(stmt)
        return result.mappings().all()
