from datetime import date, datetime
from uuid import uuid4
from sqlalchemy import Connection, MetaData, Table, create_engine, select, text, except_
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from ..objetos.usuario import Usuario, UsuarioDB, UsuarioCreate

table_name = "users"

from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import List, Optional
from uuid import UUID
from passlib.context import CryptContext # Para hashear contraseñas

# Importamos los modelos de la base de datos (DB) y los modelos Pydantic (objetos)
# Asumiendo que están en 'app/objetos/usuario.py' según tus imports
from ..objetos.usuario import Usuario

# Configuración del contexto de hasheo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsuarioServicio:
    """
    Esta clase contiene toda la lógica de negocio (CRUD)
    para interactuar con la base de datos de Usuarios.
    """

    def get_password_hash(self, password: str) -> str:
        """Hashea una contraseña en texto plano."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica una contraseña en texto plano contra un hash."""
        return pwd_context.verify(plain_password, hashed_password)

    # --- Funciones CRUD (Llamadas por el controlador) ---

    def get_usuario_by_email(self, db: Session, email: str) -> Optional[UsuarioDB]:
        """
        (POST) Busca un usuario por su email.
        Usado por el controlador para verificar duplicados.
        """
        return db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

    def get_usuario_by_username(self, db: Session, username: str) -> Optional[UsuarioDB]:
        """
        (GET /username) Busca un usuario por su nombre de usuario.
        """
        return db.query(UsuarioDB).filter(UsuarioDB.username == username).first()

    def get_usuario_by_id(self, db: Session, user_id: int) -> Optional[UsuarioDB]:
        """
        Busca un usuario por su ID (int).
        """
        return db.query(UsuarioDB).filter(UsuarioDB.id == user_id).first()

    def get_all_usuarios(self, db: Session) -> List[UsuarioDB]:
        """
        (GET /) Devuelve una lista de todos los usuarios.
        """
        return db.query(UsuarioDB).all()

    def create_usuario(self, db: Session, usuario: dict) -> UsuarioDB:
        """
        (POST) Crea un nuevo usuario en la base de datos.
        Hashea la contraseña antes de guardarla.
        """
        # Filtramos la entrada para incluir solo columnas del modelo
        atributos_modelo = UsuarioDB.__table__.columns.keys()
        data_limpia = {k: v for k, v in usuario.items() if k in atributos_modelo}  
        
        # Hasheamos la contraseña
        if 'password' in usuario:
            data_limpia["password_hash"] = self.get_password_hash(usuario['password'])  
        
        # Convertimos adecuadamente la fecha si es un string
        if 'birth_date' in data_limpia and isinstance(data_limpia['birth_date'], str):
            try:
                data_limpia['birth_date'] = datetime.strptime(data_limpia['birth_date'], '%Y-%m-%d').date()
            except ValueError as e:
                raise ValueError(f"Formato invalido para la fecha. Usa YYYY-MM-DD: {e}")
            
        # Añadimos al usuario
        db_user = UsuarioDB(**data_limpia)
        db.add(db_user)
        try:
            db.commit()
            db.refresh(db_user)
            return db_user
        except exc.SQLAlchemyError as e:
            db.rollback()
            # Relanzamos la excepción para que el controlador la maneje
            raise e

    def update_usuario(self, db: Session, user_id: int, usuario: dict) -> Optional[UsuarioDB]:
        """
        (PUT) Actualiza un usuario existente.
        """
        db_user = self.get_usuario_by_id(db, user_id)
        if not db_user:
            return None # El controlador devolverá 404

        # Actualiza los campos basados en el modelo 'Usuario'
        for key, value in usuario.items():
            # Solo actualizar si el atributo existe en el modelo
            if hasattr(db_user, key):
                # Convertir birth_date de string a date object si es necesario
                if key == "birth_date" and isinstance(value, str):
                    try:
                        value = datetime.strptime(value, '%Y-%m-%d').date()
                    except ValueError:
                        raise ValueError(f"Formato de fecha inválido: {value}. Use YYYY-MM-DD")
                
                # Validación para username único 
                if key == "username" and value != db_user.username:
                    existing_user = self.get_usuario_by_username(db, value)
                    if existing_user:
                        raise ValueError("No puedes cambiar el username al de un usuario que ya existe")
                
                # Validación para email único
                if key == "email" and value != db_user.email:
                    existing_user = self.get_usuario_by_email(db, value)
                    if existing_user:
                        raise ValueError("El email ya está registrado por otro usuario")
                    
                setattr(db_user, key, value)
        
        db.add(db_user)
        try:
            db.commit()
            db.refresh(db_user)
            return db_user
        except exc.SQLAlchemyError as e:
            db.rollback()
            raise e

    def delete_usuario(self, db: Session, user_id: int) -> bool:
        """
        (DELETE) Elimina un usuario por su ID. Devuelve True si tuvo éxito, False si no se encontró.
        """
        db_user = self.get_usuario_by_id(db, user_id)
        
        if not db_user:
            return False # No encontrado

        db.delete(db_user)
        try:
            db.commit()
            return True
        except exc.SQLAlchemyError as e:
            db.rollback()
            raise e
        
    def crear_amistad(self, db: Session, user_id: int, friend_id: int) -> bool:
        """
        Crea una relación de amistad entre dos usuarios
        """
        try:
            # Comprueba si existen los usuarios
            user = self.get_usuario_by_id(db, user_id)
            friend = self.get_usuario_by_id(db, friend_id)
            
            if not user or not friend:
                return False
            
            # Comprueba si ya son amigos
            if friend_id in user.friends:
                return True
            
            # Añade relación
            user.friends.append(friend)
            friend.friends.append(user)
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise e
        
    def obtener_amigos(self, db: Session, user_id: int) -> List[UsuarioDB]:
        """
        Obtiene la lista de amigos de un usuario
        """
        user = self.get_usuario_by_id(db, user_id)
        if not user:
            return []
        return user.friends
    
    def eliminar_amistad(self, db: Session, user_id: int, friend_id: int) -> bool:
        """
        Remove friend relationship
        """
        try:
            user = self.get_usuario_by_id(db, user_id)
            friend = self.get_usuario_by_id(db, friend_id)
            
            if not user or not friend:
                return False
            
            # Remove friend relationship
            if friend in user.friends:
                user.friends.remove(friend)
                db.commit()
                return True
            return False
            
        except Exception as e:
            db.rollback()
            print(f"Error removing friend: {e}")
            return False
