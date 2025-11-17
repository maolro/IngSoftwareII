from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import date
from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship
from app.base_datos import Base

# Tabla auxiliar de amistades
user_friends = Table(
    'user_friends',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('created_at', TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
)

@dataclass
class UsuarioCreate:
    username: str
    email: str
    password: str
    birth_date: date

class UsuarioDB(Base):
    __tablename__ = "users" # Nombre de la tabla

    # BIGINT AUTO_INCREMENT PRIMARY KEY
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # VARCHAR(50) UNIQUE NOT NULL
    username = Column(String(50), unique=True, nullable=False)
    # VARCHAR(100) UNIQUE NOT NULL
    email = Column(String(100), unique=True, nullable=False)
    # DATE
    birth_date = Column(Date)
    # VARCHAR(255) NOT NULL
    password_hash = Column(String(255), nullable=False)
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = Column(TIMESTAMP, nullable=False,
        server_default=text("CURRENT_TIMESTAMP"))
    # updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updated_at = Column(TIMESTAMP, nullable=False, 
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )
    # Gestion de amigos
    friends = relationship(
        "UsuarioDB",
        secondary=user_friends,
        primaryjoin=id == user_friends.c.user_id,
        secondaryjoin=id == user_friends.c.friend_id,
        backref="friend_of"
    )
    # Gestión de galardones
    galardones_obtenidos = relationship(
        "UsuarioGalardon", 
        back_populates="usuario",
        cascade="all, delete-orphan"  
    )
    # Gestión de degustaciones
    degustaciones = relationship(
        "DegustacionDB", 
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        """Convierte el usuario a un dict para respuestas de la API"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "friends": [friend.id for friend in self.friends],
            "galardones_obtenidos": [galardon.to_dict() for galardon in self.galardones_obtenidos],
            "degustaciones": [degustacion.to_dict() for degustacion in self.degustaciones] 
        }


# Uso
# user1 = Usuario("john_doe", "john@example.com", "12345", [2, 3], date(1999,12,1))
# print(user1.__repr__())