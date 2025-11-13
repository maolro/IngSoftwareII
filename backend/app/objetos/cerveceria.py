# Entidad de cervecería con sus campos
from sqlalchemy import Column, Integer, String, Float
from app.base_datos import Base
from sqlalchemy.orm import relationship

# Si vas a usar otro manejador de conexiones, cambiar la importación.

class Cerveceria(Base):
    """
    Mapeo de la tabla 'cervecerias' (basado en RF-3.6, RF-3.7 y RNF-8).
    """
    
    __tablename__ = "cervecerias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    direccion = Column(String, nullable=False)
    ciudad = Column(String, index=True)
    pais = Column(String, index=True)
    descripcion = Column(String)
    telefono = Column(String)
    horario = Column(String)
    foto = Column(String)

    # Relaciones
    degustaciones = relationship("DegustacionDB",  back_populates="cerveceria",
        cascade="all, delete-orphan"
    )
    
    # Nota: 'me_gusta_total' (RF-3.7) no es una columna persistente,
    # sino un valor calculado en el servicio.

    def to_dict(self):
        """
        Convierte el objeto Cerveceria en un diccionario para la API.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "pais": self.pais,
            "descripcion": self.descripcion,
            "telefono": self.telefono,
            "horario": self.horario,
            "foto": self.foto,
        }
