# Funciones relacionadas con el RF-3 (Degustaciones)
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict, Any
from app.objetos.degustacion import DegustacionDB, ComentarioDegustacion
from app.objetos.cerveza import Cerveza
from app.objetos.cerveceria import Cerveceria
from app.servicios import galardon_servicio

# --- CRUD para Degustaciones ---

def crear_degustacion(db: Session, degustacion_data: dict) -> DegustacionDB:
    """
    Crea una nueva degustación (RF-3.1, RF-3.3, RF-3.5)
    """
    # Validar campos obligatorios
    required_fields = ['usuario_id', 'cerveza_id']
    for field in required_fields:
        if field not in degustacion_data:
            raise ValueError(f"El campo '{field}' es obligatorio")
    
    # Validar que la puntuación esté entre 0 y 5 si se proporciona (RF-3.3)
    puntuacion = degustacion_data.get('puntuacion')
    if puntuacion is not None and (puntuacion < 0 or puntuacion > 5):
        raise ValueError("La puntuación debe estar entre 0 y 5")
    
    # Verificar que la cerveza existe
    cerveza = db.query(Cerveza).filter(Cerveza.id == degustacion_data['cerveza_id']).first()
    if not cerveza:
        raise ValueError("La cerveza especificada no existe")
    
    # Verificar que la cervecería existe si se proporciona
    cerveceria_id = degustacion_data.get('cerveceria_id')
    if cerveceria_id:
        cerveceria = db.query(Cerveceria).filter(Cerveceria.id == cerveceria_id).first()
        if not cerveceria:
            raise ValueError("La cervecería especificada no existe")
    
    # Crear la degustación
    db_degustacion = DegustacionDB(**degustacion_data)
    db.add(db_degustacion)
    db.commit()
    db.refresh(db_degustacion)
    
    # Actualizar la valoración promedio de la cerveza (RF-3.4)
    actualizar_valoracion_promedio_cerveza(db, degustacion_data['cerveza_id'])
    
    return db_degustacion

def obtener_degustacion(db: Session, degustacion_id: int) -> Optional[DegustacionDB]:
    """
    Obtiene una degustación por ID
    """
    return db.query(DegustacionDB).filter(DegustacionDB.id == degustacion_id).first()

def obtener_degustaciones_por_usuario(db: Session, usuario_id: int, skip: int = 0, limit: int = 100) -> List[DegustacionDB]:
    """
    Obtiene todas las degustaciones de un usuario
    """
    return db.query(DegustacionDB).filter(
        DegustacionDB.usuario_id == usuario_id
    ).order_by(desc(DegustacionDB.fecha_creacion)).offset(skip).limit(limit).all()

def obtener_degustaciones_por_cerveza(db: Session, cerveza_id: int, skip: int = 0, limit: int = 100) -> List[DegustacionDB]:
    """
    Obtiene todas las degustaciones de una cerveza
    """
    return db.query(DegustacionDB).filter(
        DegustacionDB.cerveza_id == cerveza_id
    ).order_by(desc(DegustacionDB.fecha_creacion)).offset(skip).limit(limit).all()

def actualizar_degustacion(db: Session, degustacion_id: int, degustacion_data: dict) -> Optional[DegustacionDB]:
    """
    Actualiza una degustación existente
    """
    db_degustacion = obtener_degustacion(db, degustacion_id)
    if not db_degustacion:
        return None
    
    # Validar puntuación si se actualiza
    if 'puntuacion' in degustacion_data and degustacion_data['puntuacion'] is not None:
        if degustacion_data['puntuacion'] < 0 or degustacion_data['puntuacion'] > 5:
            raise ValueError("La puntuación debe estar entre 0 y 5")
    
    # Actualizar campos
    for key, value in degustacion_data.items():
        if hasattr(db_degustacion, key):
            setattr(db_degustacion, key, value)
    
    db.add(db_degustacion)
    db.commit()
    db.refresh(db_degustacion)
    
    # Actualizar valoración promedio si cambió la puntuación
    if 'puntuacion' in degustacion_data:
        actualizar_valoracion_promedio_cerveza(db, db_degustacion.cerveza_id)
    
    return db_degustacion

def eliminar_degustacion(db: Session, degustacion_id: int) -> bool:
    """
    Elimina una degustación
    """
    db_degustacion = obtener_degustacion(db, degustacion_id)
    if db_degustacion:
        cerveza_id = db_degustacion.cerveza_id
        db.delete(db_degustacion)
        db.commit()
        # Actualizar valoración promedio después de eliminar
        actualizar_valoracion_promedio_cerveza(db, cerveza_id)
        return True
    return False

# --- Funcionalidades específicas de negocio ---

def actualizar_valoracion_promedio_cerveza(db: Session, cerveza_id: int):
    """
    Calcula y actualiza la valoración promedio de una cerveza (RF-3.4)
    """
    # Calcular promedio de puntuaciones no nulas
    result = db.query(
        func.count(DegustacionDB.id).label('total'),
        func.avg(DegustacionDB.puntuacion).label('promedio')
    ).filter(
        DegustacionDB.cerveza_id == cerveza_id,
        DegustacionDB.puntuacion.isnot(None)
    ).first()
    
    promedio = result.promedio if result and result.total > 0 else None
    
    # Actualizar la cerveza
    cerveza = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if cerveza:
        cerveza.valoracion_promedio = promedio
        cerveza.total_valoraciones = result.total if result else 0
        db.add(cerveza)
        db.commit()

def obtener_degustaciones_mas_valoradas(db: Session, estilo: str = None, pais: str = None, skip: int = 0, limit: int = 20) -> List[DegustacionDB]:
    """
    Obtiene las degustaciones más valoradas con filtros (RF-5.6, RF-5.7)
    """
    query = db.query(DegustacionDB).join(Cerveza).filter(
        DegustacionDB.puntuacion.isnot(None)
    )
    
    # Aplicar filtros
    if estilo:
        query = query.filter(Cerveza.estilo == estilo)
    if pais:
        query = query.filter(Cerveza.pais_procedencia == pais)
    
    return query.order_by(desc(DegustacionDB.puntuacion)).offset(skip).limit(limit).all()

def obtener_actividad_amigos(db: Session, usuario_id: int, skip: int = 0, limit: int = 50) -> List[DegustacionDB]:
    """
    Obtiene la actividad reciente de degustaciones de amigos (RF-3.8, RF-5.3)
    """
    # Esta función asume que existe una relación de amistad en el modelo de usuario
    # Necesitarías implementar la lógica específica según tu modelo de amistades
    from app.objetos.usuario import UsuarioDB
    
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    if not usuario or not hasattr(usuario, 'amigos'):
        return []
    
    # Obtener IDs de amigos
    amigos_ids = [amigo.id for amigo in usuario.amigos]
    
    if not amigos_ids:
        return []
    
    return db.query(DegustacionDB).filter(
        DegustacionDB.usuario_id.in_(amigos_ids)
    ).order_by(desc(DegustacionDB.fecha_creacion)).offset(skip).limit(limit).all()

# --- Gestión de comentarios en degustaciones ---

def agregar_comentario_degustacion(db: Session, comentario_data: dict) -> ComentarioDegustacion:
    """
    Agrega un comentario a una degustación (RF-2.7)
    """
    required_fields = ['degustacion_id', 'usuario_id', 'comentario']
    for field in required_fields:
        if field not in comentario_data:
            raise ValueError(f"El campo '{field}' es obligatorio")
    
    # Verificar que la degustación existe
    degustacion = obtener_degustacion(db, comentario_data['degustacion_id'])
    if not degustacion:
        raise ValueError("La degustación especificada no existe")
    
    db_comentario = ComentarioDegustacion(**comentario_data)
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    
    # Verificar galardones por interacción social
    try:
        galardon_servicio.verificar_y_otorgar_galardones_por_comentario(
            db=db,
            usuario_id=comentario_data['usuario_id']
        )
    except Exception as e:
        print(f"Error verificando galardones por comentario: {e}")
    
    return db_comentario

def obtener_comentarios_degustacion(db: Session, degustacion_id: int, skip: int = 0, limit: int = 100) -> List[ComentarioDegustacion]:
    """
    Obtiene todos los comentarios de una degustación
    """
    return db.query(ComentarioDegustacion).filter(
        ComentarioDegustacion.degustacion_id == degustacion_id
    ).order_by(ComentarioDegustacion.fecha_creacion).offset(skip).limit(limit).all()