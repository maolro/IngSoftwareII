# Entidad de la calificación de una cerveza
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Float, func
from sqlalchemy.orm import relationship
from app.base_datos import Base

class DegustacionDB(Base):
    """
    Modelo para representar una degustación (review) de cerveza.
    RF-3.1, RF-3.3, RF-3.5, RF-3.8
    """
    __tablename__ = "degustaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    cerveza_id = Column(Integer, ForeignKey("cervezas.id"), nullable=False, index=True)
    cerveceria_id = Column(Integer, ForeignKey("cervecerias.id"), nullable=True, index=True)
    puntuacion = Column(Float, nullable=True) 
    comentario = Column(Text, nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_actualizacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relaciones
    usuario = relationship("UsuarioDB", back_populates="degustaciones")
    cerveza = relationship("Cerveza", back_populates="degustaciones")
    cerveceria = relationship("Cerveceria", back_populates="degustaciones")
    comentarios = relationship("ComentarioDegustacion", back_populates="degustacion")

    def to_dict(self):
        """
        Convierte el objeto Degustacion en un diccionario para la API.
        """
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "cerveza_id": self.cerveza_id,
            "cerveceria_id": self.cerveceria_id,
            "puntuacion": self.puntuacion,
            "comentario": self.comentario,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            "usuario": self.usuario.to_dict() if self.usuario else None,
            "cerveza": self.cerveza.to_dict() if self.cerveza else None,
            "cerveceria": self.cerveceria.to_dict() if self.cerveceria else None
        }

class ComentarioDegustacion(Base):
    """
    Modelo para comentarios en degustaciones (RF-2.7)
    """
    __tablename__ = "comentarios_degustaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    degustacion_id = Column(Integer, ForeignKey("degustaciones.id"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    comentario = Column(Text, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relaciones
    degustacion = relationship("DegustacionDB", back_populates="comentarios")
    usuario = relationship("UsuarioDB")

    def to_dict(self):
        """
        Convierte el objeto ComentarioDegustacion en un diccionario para la API.
        """
        return {
            "id": self.id,
            "degustacion_id": self.degustacion_id,
            "usuario_id": self.usuario_id,
            "comentario": self.comentario,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "usuario": self.usuario.to_dict() if self.usuario else None
        }