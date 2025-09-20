from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import Optional, List
from dao.materialesdao import MaterialesDAO
from models.MaterialModel import MaterialCreate, MaterialUpdate, MaterialSalida, MaterialOut
from routes.usuarios import validar_usuario

def get_session(request: Request):
    sess = getattr(request.app.state, "db_session", None)
    if not sess: raise HTTPException(status_code=500, detail="Sesión de BD no inicializada")
    return sess

router = APIRouter(prefix="/materiales/v1", tags=["Materiales"])

@router.post("/materiales", response_model=MaterialSalida)
def crear_material(payload: MaterialCreate, request: Request, _: bool = Depends(validar_usuario)):
    dao = MaterialesDAO(get_session(request))
    res = dao.CrearMaterialSP(payload)
    if not res.estatus: raise HTTPException(status_code=400, detail=res.message)
    return res

@router.patch("/materiales/{material_id}", response_model=MaterialSalida)
def actualizar_material(material_id: str, payload: MaterialUpdate, request: Request, _: bool = Depends(validar_usuario)):
    dao = MaterialesDAO(get_session(request))
    res = dao.ActualizarMaterialSP(material_id, payload)
    if not res.estatus: raise HTTPException(status_code=400, detail=res.message)
    return res

@router.get("/materiales/{material_id}", response_model=MaterialSalida)
def obtener_material(material_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = MaterialesDAO(get_session(request))
    return dao.ObtenerMaterialPorIdSP(material_id)

@router.get("/materiales", response_model=List[MaterialOut])
def listar_materiales(
    request: Request,
    q: Optional[str] = Query(default=None),
    idVideo: Optional[str] = Query(default=None),
    free: Optional[bool] = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = MaterialesDAO(get_session(request))
    return dao.ListarMaterialesSP(q=q, idVideo=idVideo, free=free, offset=offset, limit=limit)

@router.delete("/materiales/{material_id}")
def eliminar_material(material_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = MaterialesDAO(get_session(request))
    ok = dao.EliminarMaterialSP(material_id)
    if not ok: raise HTTPException(status_code=404, detail="Material no encontrado")
    return {"message": "Material eliminado", "estatus": True}

@router.post("/materiales/{material_id}/descargar", response_model=MaterialSalida)
def contabilizar_descarga(material_id: str, request: Request, _: bool = Depends(validar_usuario)):
    dao = MaterialesDAO(get_session(request))
    return dao.IncrementarDescargaSP(material_id)


@router.get("/materiales-con-origen")
def materiales_con_origen(
    request: Request,
    q: Optional[str] = Query(default=None),
    webinarId: Optional[str] = Query(default=None),
    videoId: Optional[str] = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    _: bool = Depends(validar_usuario)
):
    dao = MaterialesDAO(get_session(request))
    return dao.MaterialesConOrigenView(q=q, webinarId=webinarId, videoId=videoId, offset=offset, limit=limit)
