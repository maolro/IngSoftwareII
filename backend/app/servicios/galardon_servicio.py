from sqlalchemy.orm import Session
from app.objetos import galardon as galardon_modelo
from app.esquemas import galardon_esquema
from typing import List, Optional

# --- CRUD para la entidad Galardon (RF-4.5 Admin) ---

def crear_galardon(db: Session, galardon: galardon_esquema.GalardonCreate):
    """Crea un nuevo tipo de galardón (para Admin)"""
    db_galardon = galardon_modelo.Galardon(**galardon.dict())
    db.add(db_galardon)
    db.commit()
    db.refresh(db_galardon)
    return db_galardon

def obtener_galardon(db: Session, galardon_id: int):
    """Obtiene un tipo de galardón por ID"""
    return db.query(galardon_modelo.Galardon).filter(galardon_modelo.Galardon.id == galardon_id).first()

def obtener_galardones(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todos los tipos de galardones"""
    return db.query(galardon_modelo.Galardon).offset(skip).limit(limit).all()

def actualizar_galardon(db: Session, galardon_id: int, galardon: galardon_esquema.GalardonCreate):
    """Actualiza un tipo de galardón (para Admin)"""
    db_galardon = obtener_galardon(db, galardon_id)
    if db_galardon:
        update_data = galardon.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_galardon, key, value)
        db.commit()
        db.refresh(db_galardon)
    return db_galardon

def eliminar_galardon(db: Session, galardon_id: int):
    """Elimina un tipo de galardón (para Admin)"""
    db_galardon = obtener_galardon(db, galardon_id)
    if db_galardon:
        db.delete(db_galardon)
        db.commit()
        return True
    return False

# --- Lógica de Galardones de Usuario ---

def obtener_galardones_de_usuario(db: Session, usuario_id: int):
    """Obtiene los galardones que un usuario ha ganado (RF-5.5)"""
    # Usamos la relación para cargar los detalles del galardón automáticamente
    return db.query(galardon_modelo.UsuarioGalardon).filter(galardon_modelo.UsuarioGalardon.usuario_id == usuario_id).all()

# --- Lógica de Negocio (El núcleo de tu tarea) ---
# Esta función la llamarán tus compañeros desde sus servicios

def verificar_y_otorgar_galardones_por_degustacion(db: Session, usuario_id: int, degustacion_nueva):
    """
    Servicio que llamará Diego (Degustación) cada vez que se cree una.
    Aquí va la lógica para RF-4.1, RF-4.2, RF-4.3
    """
    
    # 1. Obtener todos los galardones de tipo 'cantidad_cervezas', 'pais', 'estilo'
    # 2. Obtener el progreso actual del usuario para esos galardones
    # 3. Lógica de ejemplo para "Maestro de IPA"
    #    (Necesitarás info de la degustacion_nueva)
    #    if degustacion_nueva.cerveza.estilo == "IPA":
    #       ... incrementar progreso para galardón "Maestro de IPA"
    
    # (Implementar lógica de incremento y subida de nivel aquí)
    print(f"Verificando galardones para usuario {usuario_id} por nueva degustación...")
    pass

def verificar_y_otorgar_galardones_por_comentario(db: Session, usuario_id: int):
    """
    Servicio que llamará Matías (Social) cada vez que se cree un comentario.
    Lógica para RF-4.3 (interacciones sociales).
    """
    print(f"Verificando galardones para usuario {usuario_id} por nuevo comentario...")
    pass
