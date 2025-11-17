from flask import g
from sqlalchemy.orm import Session
from app.objetos.galardon import Galardon, UsuarioGalardon
from app.objetos.usuario import UsuarioDB
import pdb

# --- CRUD para la entidad Galardon (RF-4.5 Admin) ---

def crear_galardon(db: Session, galardon: dict):
    """Crea un nuevo tipo de galardón (para Admin)"""
    # Filtramos la entrada para incluir solo columnas del modelo
    atributos_modelo = Galardon.__table__.columns.keys()
    data_limpia = {k: v for k, v in galardon.items() if k in atributos_modelo}    
    db_galardon = Galardon(**data_limpia)
    if obtener_galardon_por_nombre(db, db_galardon.nombre):
        raise ValueError("Ya existe un galardón con ese nombre")
    # Añade a la base de datos
    db.add(db_galardon)
    db.commit()
    db.refresh(db_galardon)
    return db_galardon

def obtener_galardon(db: Session, galardon_id: int):
    """Obtiene un tipo de galardón por ID"""
    return db.query(Galardon).filter(Galardon.id == galardon_id).first()

def obtener_galardon_por_nombre(db: Session, nombre: str):
    """Obtiene un tipo de galardón por nombre"""
    return db.query(Galardon).filter(Galardon.nombre == nombre).first()

def obtener_galardones(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todos los tipos de galardones"""
    return db.query(Galardon).offset(skip).limit(limit).all()

def actualizar_galardon(db: Session, galardon_id: int, galardon: dict):
    """Actualiza un tipo de galardón (para Admin)"""
    db_galardon = obtener_galardon(db, galardon_id)
    if not db_galardon:
        return None
    # Actualiza los campos
    for key, value in galardon.items():
        # Solo actualizar si el atributo existe en el modelo
        if hasattr(db_galardon, key):
            if key=="nombre" and obtener_galardon_por_nombre(db, value):
                raise ValueError("No puedes cambiar el nombre al de un galardón que ya exista")
            setattr(db_galardon, key, value)
    # Añade a la base de datos
    db.add(db_galardon)
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
    return db.query(UsuarioGalardon).filter(UsuarioGalardon.usuario_id == usuario_id).all()

def obtener_galardon_de_usuario(db: Session, usuario_id: int, galardon_id: int):
    """Obtiene un galardon que haya obtenido el usuario en base a su ID"""
    # Usamos la relación para cargar los detalles del galardón automáticamente
    return db.query(UsuarioGalardon).filter((UsuarioGalardon.usuario_id == usuario_id) 
        & (UsuarioGalardon.galardon_id == galardon_id)).first()

def asignar_galardon_a_usuario(db: Session, usuario_id: int, galardon_id: int, 
    nivel_actual: int = 1, progreso_actual: int = 0) -> UsuarioGalardon:
    """
    Asigna un galardón a un usuario 
    """
    # pdb.set_trace()
    # Check if user exists
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    if not usuario:
        raise ValueError(f"Usuario con ID {usuario_id} no encontrado")
    
    # Comprueba si el galardon existe
    galardon = obtener_galardon(db, galardon_id)
    if not galardon:
        raise ValueError(f"Galardón con ID {galardon_id} no encontrado")
    
    # Comprueba si el usuario ya tiene el galardon
    existing = obtener_galardon_de_usuario(db, usuario_id, galardon_id)
    if existing:
        raise ValueError(f"El usuario ya tiene este galardón asignado")
    
    # Valida el nivel_actual
    if nivel_actual < 1:
        raise ValueError("El nivel actual debe ser al menos 1")
    
    # Valida el progreso_actual
    if progreso_actual < 0:
        raise ValueError("El progreso actual no puede ser negativo")
    
    # Crea una nueva relación
    usuario_galardon = UsuarioGalardon(
        usuario_id=usuario_id,
        galardon_id=galardon_id,
        nivel_actual=nivel_actual,
        progreso_actual=progreso_actual
    )
    
    db.add(usuario_galardon)
    try:
        db.commit()
        db.refresh(usuario_galardon)
        return usuario_galardon
    except Exception as e:
        db.rollback()
        raise e
    
def eliminar_galardon_usuario(db: Session, user_id: int, galardon_id: int) -> bool:
    """
    Elimina un galardón de un usuario
    """
    try:
        galardon_usuario = obtener_galardon_de_usuario(db, user_id, galardon_id)
        if galardon_usuario:
            db.delete(galardon_usuario)
            db.commit()
            return True
        return False
            
    except Exception as e:
        db.rollback()
        print(f"Error eliminando galardón de usuario: {e}")
        return False

# --- Lógica de Negocio ---
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

