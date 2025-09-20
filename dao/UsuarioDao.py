# dao/UsuarioDao.py
from sqlmodel import Session
from sqlalchemy import text
from typing import Optional ,List
from models.UsuarioModel import Usuarios, UsuarioCreate, UsuarioOut, UsuarioSalida ,UsuarioUpdate

def _row_to_out(row) -> UsuarioOut:
    return UsuarioOut(
        idUsuario=str(row.get("idUsuario")),
        username=str(row.get("username")),
        mail=row.get("mail"),
        isActive=bool(row.get("isActive")),
        createdAt=str(row.get("createdAt")) if row.get("createdAt") is not None else None,
    )

class UsuariosDAO:
    def __init__(self, session: Session):
        self.session = session

    def CrearUsuarioSP(self, payload: UsuarioCreate) -> UsuarioSalida:
        salida = UsuarioSalida(message="Error al crear el usuario (SP)", estatus=False, data=None)
        try:
            stmt = text("CALL sp_create_usuario(:username, :passwordHash, :mail)") \
                .bindparams(username=payload.username,
                            passwordHash=payload.passwordHash,
                            mail=payload.mail)

            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()

            if not row:
                salida.message = "SP no devolvió registro"
                return salida

            salida.message = "Usuario creado exitosamente (SP)"
            salida.estatus = True
            salida.data = _row_to_out(row)  # <- sin passwordHash
        except Exception as e:
            self.session.rollback()
            salida.message = f"Error al crear el usuario (SP): {str(e)}"
        return salida

    def autenticar(self, username: str, passwordHash: str) -> UsuarioSalida:
        salida = UsuarioSalida(message="Error en la autenticación", estatus=False, data=None)
        try:
            stmt = text("""
                SELECT idUsuario, username, passwordHash, mail, isActive, createdAt
                FROM Usuarios
                WHERE username = :username
                  AND passwordHash = :passwordHash
                  AND isActive = 1
                LIMIT 1
            """).bindparams(username=username, passwordHash=passwordHash)

            result = self.session.exec(stmt)
            row = result.mappings().first()

            if row:
                salida.message = "Autenticación exitosa"
                salida.estatus = True
                salida.data = _row_to_out(row)  # <- salida segura
            else:
                salida.message = "Credenciales inválidas"
        except Exception as e:
            salida.message = f"Error en la autenticación: {str(e)}"
        return salida
    


    def CambiarPasswordSP(self, user_id: str, new_password_hash: str) -> UsuarioSalida:
        salida = UsuarioSalida(message="Error al cambiar contraseña", estatus=False, data=None)
        try:
            stmt = text("CALL sp_change_password(:userId, :newPasswordHash)") \
                .bindparams(userId=user_id, newPasswordHash=new_password_hash)

            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()

            if not row:
                salida.message = "Usuario no encontrado"
                return salida

            salida.message = "Contraseña actualizada"
            salida.estatus = True
            salida.data = _row_to_out(row)
        except Exception as e:
            self.session.rollback()
            salida.message = f"Error al cambiar contraseña: {str(e)}"
        return salida
    
    
    def DesactivarUsuarioSP(self, user_id: str) -> UsuarioSalida:
        salida = UsuarioSalida(message="Error al desactivar usuario", estatus=False, data=None)
        try:
            stmt = text("CALL sp_deactivate_usuario(:userId)") \
                .bindparams(userId=user_id)

            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()

            if not row:
                salida.message = "Usuario no encontrado"
                return salida

            salida.message = "Usuario desactivado"
            salida.estatus = True
            salida.data = _row_to_out(row)
        except Exception as e:
            self.session.rollback()
            salida.message = f"Error al desactivar usuario: {str(e)}"
        return salida


    def ListarUsuariosSP(self, q: Optional[str], active: Optional[bool], offset: int = 0, limit: int = 50) -> List[UsuarioOut]:
        stmt = text("CALL sp_list_usuarios(:q, :active, :offset, :limit)") \
            .bindparams(q=q, active=active, offset=offset, limit=limit)
        result = self.session.exec(stmt)
        rows = result.mappings().all()
        
        return [_row_to_out(r) for r in rows]


    def ObtenerUsuarioPorIdSP(self, user_id: str) -> UsuarioSalida:
        salida = UsuarioSalida(message="Error al obtener usuario", estatus=False, data=None)
        try:
            stmt = text("CALL sp_get_usuario_by_id(:userId)").bindparams(userId=user_id)
            result = self.session.exec(stmt)
            row = result.mappings().first()
            if not row:
                salida.message = "Usuario no encontrado"
                return salida
            salida.message, salida.estatus, salida.data = "OK", True, _row_to_out(row)
        except Exception as e:
            salida.message = f"Error: {str(e)}"
        return salida


    def ActualizarUsuarioSP(self, user_id: str, payload: UsuarioUpdate) -> UsuarioSalida:
        salida = UsuarioSalida(message="Error al actualizar usuario", estatus=False, data=None)
        try:
            stmt = text("""
                CALL sp_update_usuario(:userId, :username, :mail, :isActive)
            """).bindparams(
                userId=user_id,
                username=payload.username,
                mail=payload.mail,
                isActive=payload.isActive
            )
            result = self.session.exec(stmt)
            row = result.mappings().first()
            self.session.commit()
            if not row:
                salida.message = "Usuario no encontrado"
                return salida
            salida.message, salida.estatus, salida.data = "Usuario actualizado", True, _row_to_out(row)
        except Exception as e:
            self.session.rollback()
            salida.message = f"Error al actualizar usuario: {str(e)}"
        return salida