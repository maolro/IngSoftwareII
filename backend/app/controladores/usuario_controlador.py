from flask import Blueprint, jsonify, request, abort, g
from sqlalchemy.orm import Session
from typing import List
from ..servicios.usuario_servicio import UsuarioServicio

# --- Inicialización ---

usuario_bp = Blueprint('usuario_bp', __name__)

# --- HTTP Endpoints ---

# 1. POST (Create) - Registrar nuevo usuario
@usuario_bp.route("/usuarios/", methods=["POST"])
def create_new_user():
    """
    Registrar nuevo usuario
    """
    data = request.json
    if not data:
        return jsonify({
            "error": "No se proporcionaron datos para crear el usuario"
        }), 400  
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'birth_date']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"El campo '{field}' es obligatorio"
            }), 400    
    try:
        # Comprueba si el correo ya existe
        if UsuarioServicio.get_usuario_by_email(g.db, email=data['email']):
            return jsonify({
                "error": "El correo electrónico ya está registrado."
            }), 409
        
        # Comprueba si el nombre de usuario ya existe
        if UsuarioServicio.get_usuario_by_username(g.db, username=data['username']):
            return jsonify({
                "error": "El nombre de usuario ya está registrado."
            }), 409
        
        # Llama a la capa de servicios
        db_user = UsuarioServicio.create_usuario(g.db, data)

        return jsonify(db_user.to_dict()), 201
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {e}"
        }), 500


# 2. GET - Obtener todos los usuarios
@usuario_bp.route("/usuarios/", methods=["GET"])
def get_all_users():
    """
    Obtener lista de todos los usuarios
    """
    try:
        # Llama la función que obtiene todos los usuarios
        usersDB = UsuarioServicio.get_all_usuarios(db=g.db)
        usuarios_response = [usuario.to_dict() for usuario in usersDB]    
        return jsonify(usuarios_response), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {e}"
        }), 500


# 3. GET - Obtener un usuario específico por ID
@usuario_bp.route("/usuarios/<int:user_id>/", methods=["GET"])
def get_user_by_id(user_id: int):
    """
    Obtener usuario por ID
    """
    try:
        # Llama la función que trabaja sobre la base de datos
        db_user = UsuarioServicio.get_usuario_by_id(db=g.db, user_id=user_id)
        
        if db_user is None:
            return jsonify({
                "error": f"Usuario con ID {user_id} no encontrado."
            }), 404
            
        usuario_response = {
            "id": db_user.id, 
            "username": db_user.username,
            "email": db_user.email,
            "birth_date": db_user.birth_date.isoformat() if db_user.birth_date else None,
            "password": "",
            "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
            "friends": [friend.id for friend in db_user.friends] if hasattr(db_user, 'friends') else []
        }
        
        return jsonify(usuario_response), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {e}"
        }), 500


# 4. PUT - Actualizar usuario
@usuario_bp.route("/usuarios/<int:user_id>/", methods=["PUT"])
def update_user_by_id(user_id: int):
    """
    Actualizar información del usuario
    """
    data = request.json
    if not data:
        return jsonify({
            "error": f"No se proporcionaron datos para actualizar el usuario"
        }), 400
    
    try:
        db_user = UsuarioServicio.update_usuario(db=g.db, user_id=user_id, usuario=data)
    
        if db_user is None:
            return jsonify({
                "error": f"El usuario {user_id} no existe."
            }), 404
            
        usuario_response = {
            "id": db_user.id, 
            "username": db_user.username,
            "email": db_user.email,
            "birth_date": db_user.birth_date.isoformat() if db_user.birth_date else None,
            "password": "",
            "friends": [friend.id for friend in db_user.friends] if hasattr(db_user, 'friends') else []
        }
        
        return jsonify(usuario_response), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {e}"
        }), 500


# 5. DELETE - Eliminar usuario
@usuario_bp.route("/usuarios/<int:user_id>/", methods=["DELETE"])
def delete_user_by_id(user_id: int):
    """
    Eliminar usuario por ID
    """
    try:
        success = UsuarioServicio.delete_usuario(g.db, user_id)
        
        if not success:
            return jsonify({
                "error": f"El usuario {user_id} no existe."
            }), 404
        
        return jsonify({
            "message": f"Usuario con ID {user_id} eliminado correctamente."
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {e}"
        }), 500

# ENDPOINTS DE AMISTAD

# 6. POST - Agregar amigo a usuario
@usuario_bp.route("/usuarios/<int:user_id>/amigos/", methods=["POST"])
def add_friend(user_id: int):
    """
    Agregar un amigo a un usuario.
    """
    data = request.json
    if not data or 'friend_id' not in data:
        return jsonify({
                "error": f"El campo friend_id es obligatorio"
            }), 400
    
    friend_id = data['friend_id']
    
    try:
        # Para que no pueda añadirse como amigo a sí mismo
        if user_id == friend_id:
            return jsonify({
                "error": "No puedes agregarte a ti mismo como amigo."
            }), 400
        
        success = UsuarioServicio.crear_amistad(g.db, user_id, friend_id)
        
        if success:    
            return jsonify({
                "success": True,
                "message": f"Amigo agregado correctamente."
            }), 201
        else:
            return jsonify({
                "error": "No se pudo agregar el amigo. Verifica que ambos usuarios existan."
            }), 400
            
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500


# 7. GET - Obtener lista de amigos del usuario
@usuario_bp.route("/usuarios/<int:user_id>/amigos/", methods=["GET"])
def get_user_friends(user_id: int):
    """
    Obtiene todos los amigos de un usuario
    """
    try:
        friends = UsuarioServicio.obtener_amigos(g.db, user_id)
        
        # Convierte a formato de respuesta
        friend_responses = []
        for friend in friends:
            friend_responses.append({
                "id": friend.id,
                "username": friend.username,
                "email": friend.email,
                "birth_date": friend.birth_date.isoformat() if friend.birth_date else None,
                "password": "",  # No incluye contraseñas
                "friends": [] # No incluye amigos
            })
        
        return jsonify(friend_responses), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500


# 8. GET - Verificar si existe amistad entre usuarios
@usuario_bp.route("/usuarios/<int:user_id>/amigos/<int:friend_id>/", methods=["GET"])
def get_friend_info(user_id: int, friend_id: int):
    """
    Verificar si existe amistad entre usuarios
    """
    try:
        db_user = UsuarioServicio.get_usuario_by_id(db=g.db, user_id=user_id)
        # Comprueba si el usuario existe
        if db_user is None:
            return jsonify({
                "error": f"Usuario con ID {user_id} no encontrado."
            }), 404

        db_friend = UsuarioServicio.get_usuario_by_id(db=g.db, user_id=friend_id)
        # Comprueba si el amigo existe
        if db_friend is None:
            return jsonify({
                "error": f"El usuario de ID {user_id} no tiene ningún amigo con ID {friend_id}."
            }), 404
        
        # Devuelve información de usuario
        friend_response = {
            "id": db_friend.id, 
            "username": db_friend.username,
            "email": db_friend.email,
            "birth_date": db_friend.birth_date.isoformat() if db_friend.birth_date else None,
            "password": "",
            "friends": [friend.id for friend in db_friend.friends] if hasattr(db_friend, 'friends') else []
        }
        
        return jsonify(friend_response), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500


# 9. DELETE - Eliminar amigo de usuario
@usuario_bp.route("/usuarios/<int:user_id>/amigos/<int:friend_id>/", methods=["DELETE"])
def remove_friend(user_id: int, friend_id: int):
    """
    Eliminar un amigo de la lista de amigos de un usuario.
    """
    try:
        success = UsuarioServicio.eliminar_amistad(g.db, user_id, friend_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": f"Amigo eliminado correctamente."
            }), 200
        else:
            return jsonify({
                "error": "No se pudo eliminar el amigo. Verifica que la amistad exista."
            }), 400
            
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500