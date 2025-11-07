from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from ..objetos.usuario import Usuario, UsuarioCreate
from ..objetos.amistad import FriendRelationship, FriendRequest
from ..servicios.usuario_servicio import UsuarioServicio
from ..database import get_db

# --- Initialization ---

# 1. Create the FastAPI Router
usuario_router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# 2. Initialize the service layer
usuario_service = UsuarioServicio()


# --- HTTP Endpoints (Routes) ---

# 1. POST (Create)
@usuario_router.post(
    "/", 
    response_model=Usuario, 
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario"
)
# Crea nuevo usuario
def create_new_user(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        # Comprueba si el correo ya existe
        if usuario_service.get_usuario_by_email(db, email=usuario_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo electrónico ya está registrado."
            )
        
        # Comprueba si el nombre de usuario ya existe
        if usuario_service.get_usuario_by_username(db, username=usuario_data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El nombre de usuario ya está registrado."
            )
        
        # Llama a la capa de servicios
        db_user = usuario_service.create_usuario(db, usuario_data)

        # Convierte a usuario para devolver su información
        return Usuario(
            user_id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            birth_date=db_user.birth_date,
            password="",  
            friends=[]
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        # Obtiene errores
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor: {e}"
        )


# Obtiene todos los usuarios (GET)
@usuario_router.get(
    "/", 
    response_model=List[Usuario],
    summary="Obtener lista de todos los usuarios"
)
def get_all_users(db: Session = Depends(get_db)):
    # Llama la función que obtiene todos los usuarios
    usersDB = usuario_service.get_all_usuarios(db=db)
    return [
        Usuario(
            user_id=db_user.id, 
            username=db_user.username,
            email=db_user.email,
            birth_date=db_user.birth_date,
            password="",
            friends=[friend.id for friend in db_user.friends]
        ) for db_user in usersDB
    ]


# Obtiene un usuario específico
@usuario_router.get(
    "/{user_id}", 
    response_model=Usuario,
    summary="Obtener usuario por ID"
)
# Busca un único usuario en base a su nombre de usuario
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    # Llama la función que trabaja sobre la base de datos
    db_user = usuario_service.get_usuario_by_id(db=db, user_id=user_id)
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado."
        )
        
    return Usuario(
        user_id=db_user.id, 
        username=db_user.username,
        email=db_user.email,
        birth_date=db_user.birth_date,
        password="",
        friends=[friend.id for friend in db_user.friends]
    )


# Actualiza usuario
@usuario_router.put(
    "/{user_id}",
    response_model=Usuario,
    summary="Actualizar información del usuario"
)
def update_user_by_id(user_id: int, usuario: Usuario, db: Session = Depends(get_db)):
    try:
        db_user = usuario_service.update_usuario(db=db, user_id=user_id, usuario=usuario)
    
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El usuario {user_id} no existe."
            )
        return Usuario(
            user_id=db_user.id, 
            username=db_user.username,
            email=db_user.email,
            birth_date=db_user.birth_date,
            password="",
            friends=[friend.id for friend in db_user.friends]
        )
        
    except HTTPException as e:
        raise e


# Elimina usuario
@usuario_router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario por ID"
)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    success = usuario_service.delete_usuario(db, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado."
        )
    
    return {"message": f"Usuario con ID {user_id} eliminado correctamente."}

# ENDPOINTS DE AMISTAD

@usuario_router.post(
    "/{user_id}/amigos/",
    response_model=FriendRelationship,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar amigo a usuario"
)
def add_friend(friend_request: FriendRequest, db: Session = Depends(get_db)):
    """
    Agregar un amigo a un usuario.
    """
    user_id = friend_request.user_id
    friend_id = friend_request.friend_id
    try:
        # Para que no pueda añadirse como amigo a sí mismo
        if user_id == friend_id:
            return FriendRelationship(
                success=False,
                message="No puedes agregarte a ti mismo como amigo."
            )
        
        success = usuario_service.crear_amistad(db, user_id, friend_id)
        
        if success:    
            return FriendRelationship(
                success=True,
                message=f"Amigo agregado correctamente."
            )
        else:
            return FriendRelationship(
                success=False,
                message="No se pudo agregar el amigo. Verifica que ambos usuarios existan."
            )
            
    except Exception as e:
        return FriendRelationship(
            success=False,
            message=f"Error interno del servidor: {str(e)}"
        )

@usuario_router.get(
    "/{user_id}/amigos/",
    response_model=List[Usuario],
    summary="Obtener lista de amigos del usuario"
)
def get_user_friends(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los amigos de un usuario
    """
    try:
        friends = usuario_service.obtener_amigos(db, user_id)
        
        # Convierte a Usuario
        friend_responses = []
        for friend in friends:
            friend_responses.append(Usuario(
                user_id=friend.id,
                username=friend.username,
                email=friend.email,
                birth_date=friend.birth_date,
                password="",  # No incluye contraseñas
                friends=[] # No incluye amigos
            ))
        
        return friend_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo amigos: {str(e)}"
        )

@usuario_router.get(
    "/{user_id}/amigos/{friend_id}",
    response_model=Usuario,
    summary="Verificar si existe amistad entre usuarios"
)

@usuario_router.delete(
    "/{user_id}/amigos/{friend_id}",
    response_model=FriendRelationship,
    summary="Eliminar amigo de usuario"
)
def remove_friend(
    user_id: int,
    friend_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un amigo de la lista de amigos de un usuario.
    """
    try:
        success = usuario_service.eliminar_amistad(db, user_id, friend_id)
        
        if success:
            return FriendRelationship(
                success=True,
                message=f"Amigo eliminado correctamente."
            )
        else:
            return FriendRelationship(
                success=False,
                message="No se pudo eliminar el amigo. Verifica que la amistad exista."
            )
            
    except Exception as e:
        return FriendRelationship(
            success=False,
            message=f"Error interno del servidor: {str(e)}"
        )