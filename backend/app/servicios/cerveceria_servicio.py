from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.objetos.cerveceria import Cerveceria
import math

class CerveceriaService:

    @staticmethod
    def crear_cerveceria(db: Session, cerveceria_data: dict) -> Cerveceria:
        db_existente = db.query(Cerveceria).filter(
            func.lower(Cerveceria.nombre) == func.lower(cerveceria_data['nombre'])
        ).first()

        if db_existente:
            raise ValueError(f"La cervecería '{cerveceria_data['nombre']}' ya existe.")

        atributos_modelo = Cerveceria.__table__.columns.keys()
        data_limpia = {k: v for k, v in cerveceria_data.items() if k in atributos_modelo}

        db_cerveceria = Cerveceria(**data_limpia)
        db.add(db_cerveceria)
        db.commit()
        db.refresh(db_cerveceria)
        return db_cerveceria

    @staticmethod
    def buscar_cervecerias(db: Session, q: str = None, ciudad: str = None, pais: str = None) -> list[Cerveceria]:
        query = db.query(Cerveceria)
        if q:
            query = query.filter(Cerveceria.nombre.ilike(f"%{q}%"))
        if ciudad:
            query = query.filter(Cerveceria.ciudad == ciudad)
        if pais:
            query = query.filter(Cerveceria.pais == pais)
        return query.order_by(Cerveceria.nombre).all()

    @staticmethod
    def get_cerveceria_por_id(db: Session, cerveceria_id: int) -> Cerveceria | None:
        return db.query(Cerveceria).filter(Cerveceria.id == cerveceria_id).first()

    @staticmethod
    def get_cervecerias_cercanas(db: Session, lat: float, lon: float, radio: float = 5) -> list[Cerveceria]:
        """
        Devuelve cervecerías dentro de un radio en km usando coordenadas.
        Requiere que Cerveceria tenga columnas lat/lon.
        """
        # Placeholder: si no tienes lat/lon, devuelve todas
        if not hasattr(Cerveceria, 'lat') or not hasattr(Cerveceria, 'lon'):
            return db.query(Cerveceria).order_by(Cerveceria.nombre).all()

        def distancia_km(lat1, lon1, lat2, lon2):
            R = 6371  # radio de la tierra en km
            phi1, phi2 = math.radians(lat1), math.radians(lat2)
            d_phi = math.radians(lat2 - lat1)
            d_lambda = math.radians(lon2 - lon1)
            a = math.sin(d_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(d_lambda/2)**2
            c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c

        todas = db.query(Cerveceria).all()
        cercanas = [
            c for c in todas
            if c.lat is not None and c.lon is not None and distancia_km(lat, lon, c.lat, c.lon) <= radio
        ]
        return sorted(cercanas, key=lambda x: x.nombre)
