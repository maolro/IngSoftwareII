from sqlalchemy import Column, Integer, String, Float
from app.base_datos import Base
#Si vas a usar otro manejador de conexiones, cambiar la importación.

class Cerveza(Base):
    """
    Mapeo de la tabla 'cervezas' (basado en RF-3.2).
    """
    
    __tablename__ = "cervezas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String)
    foto = Column(String)
    estilo = Column(String, index=True)
    pais_procedencia = Column(String, index=True)
    tamano = Column(String)
    formato = Column(String)
    porcentaje_alcohol = Column(Float)
    ibu = Column(Integer) # Amargor (%IBU)
    color = Column(String)
    
    # Nota: 'valoracion_promedio' (RF-3.4) no es una columna
    # sino un valor calculado en el servicio.

    def to_dict(self):
        """
        Convierte el objeto Cerveza en un diccionario para la API.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "foto": self.foto,
            "estilo": self.estilo,
            "pais_procedencia": self.pais_procedencia,
            "tamano": self.tamano,
            "formato": self.formato,
            "porcentaje_alcohol": self.porcentaje_alcohol,
            "ibu": self.ibu,
            "color": self.color,
        }

