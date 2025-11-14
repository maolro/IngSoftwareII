from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.objetos.cerveza import Cerveza
from app.objetos.degustacion import DegustacionDB

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
        # El query ahora pide la Cerveza y el promedio de Degustacion.rating
        query = db.query(
            Cerveza,
            func.avg(DegustacionDB.rating).label("valoracion_promedio")
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
    def get_valoracion_promedio(db: Session, cerveza_id: int) -> float:
        """
        Calcula la valoración promedio (RF-3.4).
        ¡¡¡PLACEHOLDER!!! Requiere el modelo 'Degustacion'.
        """

        #### --- IMPLEMENTACIÓN (requiere Degustacion) ---
        # 
        # resultado = db.query(func.avg(Degustacion.rating))\
        #               .filter(Degustacion.cerveza_id == cerveza_id)\
        #               .scalar()
        # return round(resultado, 2) if resultado is not None else 0.0
        # 
        # --- FIN IMPLEMENTACIÓN FUTURA ---
        
        #### Devolvemos un valor de ejemplo mientras no exista Degustacion
        return 0.0 

    @staticmethod
    def get_favoritas_usuario(db: Session, usuario_id: int) -> list[dict]:
        """
        Obtiene las 3 favoritas de un usuario (RF-5.4).
        ¡¡¡PLACEHOLDER!!! Requiere 'Degustacion' y 'Usuario'.
        """
        # favoritas = db.query(
        #             Cerveza,
        #             func.avg(Degustacion.rating).label("valoracion_usuario")
        #         ).join(
        #             Degustacion, Cerveza.id == Degustacion.cerveza_id
        #         ).filter(
        #             Degustacion.usuario_id == usuario_id
        #         ).group_by(
        #             Cerveza.id
        #         ).order_by(
        #             func.desc("valoracion_usuario") # Ordena por el alias
        #         ).limit(3).all()
                
        # # 'favoritas' es una lista de tuplas: [(Cerveza, 5.0), (Cerveza, 4.5)]
        # # La convertimos al formato diccionario que pedía el placeholder:
        
        # return [
        #     {
        #         "id": cerveza.id,
        #         "nombre": cerveza.nombre,
        #         "estilo": cerveza.estilo,
        #         "valoracion_usuario": round(valoracion, 2)
        #     }
        #     for cerveza, valoracion in favoritas # Desempaquetamos la tupla
        # ]
                
        # Devolvemos un valor de ejemplo
        return [
            {"id": 1, "nombre": "Cerveza Favorita 1 (Ejemplo)", "estilo": "IPA", "valoracion_usuario": 5.0},
            {"id": 2, "nombre": "Cerveza Favorita 2 (Ejemplo)", "estilo": "Stout", "valoracion_usuario": 4.5},
        ]

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