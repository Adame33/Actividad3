from sqlmodel import Session
from sqlalchemy import text
from typing import Optional, List, Dict, Any
from models.MaterialModel import MaterialCreate, MaterialUpdate, MaterialOut, MaterialSalida

def _row_to_material_out(row) -> MaterialOut:
    return MaterialOut(
        idMaterial=str(row.get("idMaterial")),
        idVideo=str(row.get("idVideo")),
        nombre=str(row.get("nombre")),
        url=str(row.get("url")),
        descargas=int(row.get("descargas")),
        free=bool(row.get("free")),
    )

class MaterialesDAO:
    def __init__(self, session: Session):
        self.session = session

    def CrearMaterialSP(self, payload: MaterialCreate) -> MaterialSalida:
        salida = MaterialSalida(message="Error al crear material", estatus=False, data=None)
        try:
            stmt = text("CALL sp_create_material(:idVideo,:nombre,:url,:free)") \
                .bindparams(idVideo=payload.idVideo, nombre=payload.nombre, url=payload.url, free=payload.free)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row: salida.message = "SP no devolvió registro"; return salida
            salida.message, salida.estatus, salida.data = "Material creado", True, _row_to_material_out(row)
        except Exception as e:
            self.session.rollback(); salida.message = f"Error: {str(e)}"
        return salida

    def ActualizarMaterialSP(self, id_material: str, payload: MaterialUpdate) -> MaterialSalida:
        salida = MaterialSalida(message="Error al actualizar material", estatus=False, data=None)
        try:
            stmt = text("CALL sp_update_material(:id,:nombre,:url,:free)") \
                .bindparams(id=id_material, nombre=payload.nombre, url=payload.url, free=payload.free)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row: salida.message = "Material no encontrado"; return salida
            salida.message, salida.estatus, salida.data = "Material actualizado", True, _row_to_material_out(row)
        except Exception as e:
            self.session.rollback(); salida.message = f"Error: {str(e)}"
        return salida

    def ObtenerMaterialPorIdSP(self, id_material: str) -> MaterialSalida:
        salida = MaterialSalida(message="Error al obtener material", estatus=False, data=None)
        try:
            stmt = text("CALL sp_get_material_by_id(:id)").bindparams(id=id_material)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            if not row: salida.message = "Material no encontrado"; return salida
            salida.message, salida.estatus, salida.data = "OK", True, _row_to_material_out(row)
        except Exception as e:
            salida.message = f"Error: {str(e)}"
        return salida

    def ListarMaterialesSP(self, q: Optional[str], idVideo: Optional[str],
                           free: Optional[bool], offset: int = 0, limit: int = 50) -> List[MaterialOut]:
        stmt = text("CALL sp_list_materiales(:q,:idVideo,:free,:offset,:limit)") \
            .bindparams(q=q, idVideo=idVideo, free=free, offset=offset, limit=limit)
        result = self.session.exec(stmt)
        rows = result.mappings().all()
        return [_row_to_material_out(r) for r in rows]

    def EliminarMaterialSP(self, id_material: str) -> bool:
        stmt = text("CALL sp_delete_material(:id)").bindparams(id=id_material)
        result = self.session.exec(stmt)
        row = result.mappings().first()
        self.session.commit()
        return bool(row and row.get("deleted") == 1)

    def IncrementarDescargaSP(self, id_material: str) -> MaterialSalida:
        salida = MaterialSalida(message="Error al incrementar descarga", estatus=False, data=None)
        try:
            stmt = text("CALL sp_increment_descarga_material(:id)").bindparams(id=id_material)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row: salida.message = "Material no encontrado"; return salida
            salida.message, salida.estatus, salida.data = "Descarga contabilizada", True, _row_to_material_out(row)
        except Exception as e:
            self.session.rollback(); salida.message = f"Error: {str(e)}"
        return salida

    
    def MaterialesConOrigenView(self, q: Optional[str] = None, webinarId: Optional[str] = None,
                                videoId: Optional[str] = None, offset: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        where, params = ["1=1"], {"offset": offset, "limit": limit}
        if q:
            where.append("(material LIKE :q OR webinar LIKE :q OR video LIKE :q)")
            params["q"] = f"%{q}%"
        if webinarId:
            where.append("idWebinar = :webinarId")
            params["webinarId"] = webinarId
        if videoId:
            where.append("idVideo = :videoId")
            params["videoId"] = videoId

        sql = f"""
          SELECT * FROM vw_materiales_con_origen
          WHERE {' AND '.join(where)}
          ORDER BY webinar, video, material
          LIMIT :offset, :limit
        """
        res = self.session.exec(text(sql).bindparams(**params))
        return res.mappings().all()
