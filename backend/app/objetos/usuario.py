from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import date
from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship
from ..database import Base

# Tabla auxiliar de amistades
user_friends = Table(
    'user_friends',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('created_at', TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
)

# Entidad del usuario con sus campos    
@dataclass
class Usuario:
    user_id: int
    username: str
    email: str
    password: str
    friends: list[int]
    birth_date: date

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


# Uso
# user1 = Usuario("john_doe", "john@example.com", "12345", [2, 3], date(1999,12,1))
# print(user1.__repr__())