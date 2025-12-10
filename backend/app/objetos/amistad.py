# Entidad que modela amistad entre usuarios 
from dataclasses import dataclass
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, ForeignKey, text
from app.base_datos import Base

@dataclass
class FriendRelationship:
    success: bool
    message: str

@dataclass
class FriendRequest:
    friend_id: int
    is_accepted: bool

class FriendDB:
    __tablename__ = "user_friends" # Nombre de la tabla
    # user_id BIGINT
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # friend_id BIGINT
    friend_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = Column(TIMESTAMP, nullable=False,
        server_default=text("CURRENT_TIMESTAMP"))
    
class FriendRequestDB(Base):
    __tablename__ = "friend_requests" # Nombre de la tabla
    # user_id BIGINT
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # friend_id BIGINT
    friend_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # is_accepted BOOL
    is_accepted = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    # Relaciones para obtener datos de los usuarios fácilmente
    sender = relationship("UsuarioDB", foreign_keys=[user_id])
    receiver = relationship("UsuarioDB", foreign_keys=[friend_id])

    def to_dict(self):
        return {
            "sender_id": self.user_id,
            "receiver_id": self.friend_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            # Incluimos datos básicos del enviador para el frontend
            "sender_username": self.sender.username if self.sender else None,
            "sender_email": self.sender.email if self.sender else None,
        }