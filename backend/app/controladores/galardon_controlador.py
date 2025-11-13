from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.servicios import galardon_servicio
from app.esquemas import galardon_esquema
from app.database import get_db # Importa el dependency de FastAPI

galardon_router = APIRouter(
    prefix="/galardones",
    tags=["Galardones"]
)

# --- Endpoints para ADMIN (RF-4.5) ---

@galardon_router.post("/", response_model=galardon_esquema.GalardonCreate, status_code=201)
def crear_nuevo_galardon(galardon: galardon_esquema.GalardonCreate, db: Session = Depends(get_db)):
    # NOTA: Aquí faltaría la lógica de autenticación para rol "Administrador"
    # Pero para la práctica, crear el endpoint es suficiente (RF-4.5)
    return galardon_servicio.crear_galardon(db=db, galardon=galardon)

@galardon_router.get("/", response_model=List[galardon_esquema.Galardon])
def leer_galardones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene una lista de todos los tipos de galardones"""
    galardones = galardon_servicio.obtener_galardones(db, skip=skip, limit=limit)
    return galardones

@galardon_router.get("/{galardon_id}", response_model=galardon_esquema.Galardon)
def leer_galardon_por_id(galardon_id: int, db: Session = Depends(get_db)):
    """Obtiene un tipo de galardón por su ID"""
    db_galardon = galardon_servicio.obtener_galardon(db, galardon_id=galardon_id)
    if db_galardon is None:
        raise HTTPException(status_code=404, detail="Galardon no encontrado")
    return db_galardon

@galardon_router.put("/{galardon_id}", response_model=galardon_esquema.Galardon)
def actualizar_galardon_por_id(galardon_id: int, galardon: galardon_esquema.GalardonCreate, db: Session = Depends(get_db)):
    # Lógica de admin
    db_galardon = galardon_servicio.actualizar_galardon(db, galardon_id=galardon_id, galardon=galardon)
    if db_galardon is None:
        raise HTTPException(status_code=404, detail="Galardon no encontrado")
    return db_galardon

@galardon_router.delete("/{galardon_id}", status_code=200)
def eliminar_galardon_por_id(galardon_id: int, db: Session = Depends(get_db)):
    # Lógica de admin
    if not galardon_servicio.eliminar_galardon(db, galardon_id=galardon_id):
        raise HTTPException(status_code=404, detail="Galardon no encontrado")
    return {"message": "Galardon eliminado exitosamente"}

# --- Endpoint para Usuarios (Ver sus propios galardones) ---
# Este endpoint cumple con RF-5.5 (resumen de galardones en dashboard)
# El frontend lo llamará para saber qué galardones mostrar.

@galardon_router.get("/usuario/{usuario_id}", response_model=List[galardon_esquema.UsuarioGalardonDetalle])
def leer_galardones_de_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtiene la lista de galardones que ha ganado un usuario específico"""
    # Aquí faltaría validar que el usuario exista
    galardones = galardon_servicio.obtener_galardones_de_usuario(db, usuario_id=usuario_id)
    if not galardones:
        # No es un error, el usuario puede no tener galardones
        return []
    return galardones
