from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, JSON, func
from sqlalchemy.orm import relationship
from app.database import Base # ¡Asegúrate de que 'Base' viene de 'app.database'
from app.objetos.usuario import UsuarioDB # Importa el modelo de Matías

class Galardon(Base):
    """
    Define un tipo de galardón (ej. "Maestro de IPA").
    El admin crea y gestiona estos (RF-4.5).
    """
    __tablename__ = "galardones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), unique=True, index=True, nullable=False)
    descripcion = Column(Text, nullable=False)
    imagen_url = Column(String(255))
    tipo = Column(String(50), nullable=False) 
    condiciones = Column(JSON, nullable=True)
    
    # Relación para saber qué usuarios tienen este galardón
    usuarios_que_lo_tienen = relationship("UsuarioGalardon", back_populates="galardon")

class UsuarioGalardon(Base):
    """
    Tabla de unión que registra el progreso de un usuario en un galardón.
    (ej. "Usuario 'Alex' tiene 'Maestro de IPA' Nivel 1")
    """
    __tablename__ = "usuario_galardones"

    usuario_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    galardon_id = Column(Integer, ForeignKey("galardones.id"), primary_key=True)
    
    nivel_actual = Column(Integer, nullable=False, default=1)
    progreso_actual = Column(Integer, nullable=0, default=0) # Progreso actual del usuario hacia el siguiente nivel
    obtenido_en = Column(TIMESTAMP, server_default=func.now())

    # Relaciones para acceder a los objetos
    usuario = relationship("UsuarioDB", back_populates="galardones_obtenidos")
    galardon = relationship("Galardon", back_populates="usuarios_que_lo_tienen")
