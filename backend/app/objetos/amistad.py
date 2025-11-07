# Entidad que modela amistad entre usuarios 
from sqlalchemy import TIMESTAMP, Column, Integer, ForeignKey, text

class FriendRelationship:
    user_id: int
    friend_id: int

class FriendDB:
    __tablename__ = "user_friends" # Nombre de la tabla
    # user_id BIGINT
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # friend_id BIGINT
    friend_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = Column(TIMESTAMP, nullable=False,
        server_default=text("CURRENT_TIMESTAMP"))