from sqlmodel import Session
from sqlalchemy import text
from typing import List, Optional
from models.tutoresModel import TutorCreate, TutorUpdate, TutorOut, TutorSalida

def _row_to_tutor_out(row) -> TutorOut:
    return TutorOut(
        idTutor=str(row.get("idTutor")),
        nombre=str(row.get("nombre")),
        mail=str(row.get("mail")),
        foto=row.get("foto"),
        puesto=row.get("puesto"),
        urlLinkedin=row.get("urlLinkedin"),
    )

class TutoresDAO:
    def __init__(self, session: Session):
        self.session = session

    def CrearTutorSP(self, payload: TutorCreate) -> TutorSalida:
        salida = TutorSalida(message="Error al crear tutor", estatus=False, data=None)
        try:
            stmt = text("CALL sp_create_tutor(:nombre, :mail, :foto, :puesto, :url)") \
                .bindparams(nombre=payload.nombre, mail=payload.mail,
                            foto=payload.foto, puesto=payload.puesto, url=payload.urlLinkedin)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row: salida.message = "SP no devolvió registro"; return salida
            salida.message, salida.estatus, salida.data = "Tutor creado", True, _row_to_tutor_out(row)
        except Exception as e:
            self.session.rollback(); salida.message = f"Error: {str(e)}"
        return salida

    def ActualizarTutorSP(self, id_tutor: str, payload: TutorUpdate) -> TutorSalida:
        salida = TutorSalida(message="Error al actualizar tutor", estatus=False, data=None)
        try:
            stmt = text("""
                CALL sp_update_tutor(:id, :nombre, :mail, :foto, :puesto, :url)
            """).bindparams(id=id_tutor, nombre=payload.nombre, mail=payload.mail,
                            foto=payload.foto, puesto=payload.puesto, url=payload.urlLinkedin)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row: salida.message = "Tutor no encontrado"; return salida
            salida.message, salida.estatus, salida.data = "Tutor actualizado", True, _row_to_tutor_out(row)
        except Exception as e:
            self.session.rollback(); salida.message = f"Error: {str(e)}"
        return salida

    def ObtenerTutorPorIdSP(self, id_tutor: str) -> TutorSalida:
        salida = TutorSalida(message="Error al obtener tutor", estatus=False, data=None)
        try:
            stmt = text("CALL sp_get_tutor_by_id(:id)").bindparams(id=id_tutor)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            if not row: salida.message = "Tutor no encontrado"; return salida
            salida.message, salida.estatus, salida.data = "OK", True, _row_to_tutor_out(row)
        except Exception as e:
            salida.message = f"Error: {str(e)}"
        return salida

    def ListarTutoresSP(self, q: Optional[str], offset: int = 0, limit: int = 50) -> List[TutorOut]:
        stmt = text("CALL sp_list_tutores(:q, :offset, :limit)") \
            .bindparams(q=q, offset=offset, limit=limit)
        result = self.session.exec(stmt)
        rows = result.mappings().all()
        return [_row_to_tutor_out(r) for r in rows]

    def ListarWebinarsPorTutorSP(self, id_tutor: str, offset: int = 0, limit: int = 50):
        stmt = text("CALL sp_list_webinars_by_tutor(:id, :offset, :limit)") \
            .bindparams(id=id_tutor, offset=offset, limit=limit)
        result = self.session.exec(stmt)
        return result.mappings().all()
    
    def CatalogoTutoresView(self):
        result = self.session.exec(text("SELECT * FROM vw_catalogo_tutores "))
        return result.mappings().all()

