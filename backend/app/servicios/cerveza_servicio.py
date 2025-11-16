from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, distinct
from app.objetos.cerveza import Cerveza
from app.objetos.degustacion import DegustacionDB
import pdb

class CervezaService:

    @staticmethod
    def crear_cerveza(db: Session, cerveza_data: dict) -> Cerveza:
        """
        Crea una nueva cerveza (RF-3.2).
        """
        # Verificamos si ya existe, no es case sensitive. 
        db_cerveza_existente = db.query(Cerveza).filter(
            func.lower(Cerveza.nombre) == func.lower(cerveza_data['nombre'])
        ).first()
        
        if db_cerveza_existente:
            raise ValueError(f"La cerveza '{cerveza_data['nombre']}' ya existe.")

        # Filtramos data_cerveza para incluir solo columnas del modelo
        atributos_modelo = Cerveza.__table__.columns.keys()
        data_limpia = {k: v for k, v in cerveza_data.items() if k in atributos_modelo}
        
        db_cerveza = Cerveza(**data_limpia)
        
        db.add(db_cerveza)
        db.commit()
        db.refresh(db_cerveza)
        return db_cerveza

    @staticmethod
    def buscar_cervezas(db: Session, q: str = None, estilo: str = None, pais: str = None) -> list[tuple[Cerveza, float | None]]:
        """
        Busca y filtra cervezas (RF-3.1, RF-5.7).
        AHORA INCLUYE LA VALORACIÓN PROMEDIO EN 1 SOLA CONSULTA.
        """
        # pdb.set_trace()

        # El query ahora pide la Cerveza y el promedio de Degustacion.rating
        query = db.query(
            Cerveza,
            func.avg(DegustacionDB.puntuacion).label("valoracion_promedio")
        )
        
        # Usamos un LEFT JOIN (isouter=True)
        # Si una cerveza no tiene degustaciones, el join no la descarta.
        query = query.join(DegustacionDB, DegustacionDB.cerveza_id == Cerveza.id, isouter=True)
        
        if q:
            query = query.filter(Cerveza.nombre.ilike(f"%{q}%"))
        if estilo:
            query = query.filter(Cerveza.estilo == estilo)
        if pais:
            query = query.filter(Cerveza.pais_procedencia == pais)
            
        # Agrupamos por Cerveza para que func.avg() funcione por cada cerveza
        query = query.group_by(Cerveza.id)
            
        return query.order_by(Cerveza.nombre).all()

    @staticmethod
    def get_cerveza_por_id(db: Session, cerveza_id: int) -> Cerveza | None:
        """ Obtiene una cerveza por su ID. """
        return db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    
    @staticmethod
    def actualizar_cerveza(db: Session, cerveza_id: int, 
        cerveza_data: dict) -> Optional[Cerveza]:
        """
        Actualiza una cerveza existente
        """
        db_cerveza = CervezaService.get_cerveza_por_id(db, cerveza_id)
        if not db_cerveza:
            return None
        # Actualizar campos
        for key, value in cerveza_data.items():
            if hasattr(db_cerveza, key):
                setattr(db_cerveza, key, value)
        # Actualiza en base de datos
        db.add(db_cerveza)
        db.commit()
        db.refresh(db_cerveza)
        return db_cerveza

    @staticmethod
    def eliminar_cerveza(db: Session, cerveza_id: int) -> bool:
        """
        Elimina una cerveza
        """
        db_cerveza = CervezaService.get_cerveza_por_id(db, cerveza_id)
        if not db_cerveza:
            return None
        if db_cerveza:
            db.delete(db_cerveza)
            db.commit()
            return True
        return False

    @staticmethod
    def get_valoracion_promedio(db: Session, cerveza_id: int) -> float:
        """
        Calcula la valoración promedio (RF-3.4).
        """
        resultado = db.query(func.avg(DegustacionDB.puntuacion))\
            .filter(DegustacionDB.cerveza_id == cerveza_id)\
            .scalar()
        
        return round(resultado, 2) if resultado is not None else 0.0

    @staticmethod
    def get_favoritas_usuario(db: Session, usuario_id: int) -> list[dict]:
        """
        Obtiene las 3 favoritas de un usuario (RF-5.4).
        """
        favoritas = db.query(
                Cerveza,
                DegustacionDB.puntuacion,
            ).join(
                DegustacionDB, Cerveza.id == DegustacionDB.cerveza_id
            ).filter(
                DegustacionDB.usuario_id == usuario_id,
                DegustacionDB.puntuacion.isnot(None)  # Solo degustaciones con puntuación
            ).order_by(
                desc(DegustacionDB.puntuacion),  # Ordenar por puntuación descendente
            ).limit(3).all()
                
        # # 'favoritas' es una lista de tuplas: [(Cerveza, 5.0), (Cerveza, 4.5)]
        # # La convertimos al formato diccionario que pedía el placeholder:
        pdb.set_trace()
        res = [
            {
                "id": cerveza.id,
                "nombre": cerveza.nombre,
                "estilo": cerveza.estilo,
                "valoracion_usuario": round(valoracion, 2)
            }
            for cerveza, valoracion in favoritas # Desempaquetamos la tupla
        ]
        return res

    @staticmethod
    def get_estilos_unicos(db: Session) -> list[str]:
        """ Obtiene estilos únicos ordenados alfabéticamente (RNF-4). """
        query = db.query(distinct(Cerveza.estilo)).order_by(Cerveza.estilo)
        # Filtramos None si los hubiera
        return [estilo[0] for estilo in query.all() if estilo[0]]

    @staticmethod
    def get_paises_unicos(db: Session) -> list[str]:
        """ Obtiene países únicos ordenados alfabéticamente (RNF-4). """
        query = db.query(distinct(Cerveza.pais_procedencia)).order_by(Cerveza.pais_procedencia)
        # Filtramos None si los hubiera
        return [pais[0] for pais in query.all() if pais[0]]