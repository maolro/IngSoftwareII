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
        
        # Comprueba si realmente son amigos
        is_friend = any(f.id == friend_id for f in db_user.friends)
        
        if not is_friend:
            return jsonify({
                "error": f"El usuario {user_id} no es amigo de {friend_id}."
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

# ENDPOINTS DE LOGIN   
@usuario_bp.route("/usuarios/login/", methods=["POST"])
def login():
    """
    Endpoint para login
    """
    data = request.json
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    # Comprueba si están los campos correctos
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"El campo '{field}' es obligatorio"
            }), 400    
        
    username = data['username']
    password = data['password']

    try:
        # Comrpueba si el usuario existe
        usuario = UsuarioServicio.get_usuario_by_username(g.db, username)
        
        if not usuario:
            return jsonify({"error": "El usuario indicado no existe"}), 401
        
        # Comprueba si la contraseña coincide
        if not (UsuarioServicio.verify_password(password, usuario.password_hash)):
            return jsonify({"error": "Contraseña incorrecta"}), 401
                
        # Preparar respuesta
        response_data = {
            "id": usuario.id, 
            "username": usuario.username,
            "email": usuario.email,
            "birth_date": usuario.birth_date.isoformat() if usuario.birth_date else None,
            "friends": [friend.id for friend in usuario.friends] 
                if hasattr(usuario, 'friends') else []
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# ENDPOINTS DE ACTIVIDAD
@usuario_bp.route("/usuarios/<int:user_id>/actividad/", methods=["GET"])
def get_user_activity(user_id: int):
    """
    Obtener actividad reciente (degustaciones) de los amigos del usuario
    """
    try:
        # Verificar que el usuario existe
        user = UsuarioServicio.get_usuario_by_id(g.db, user_id)
        if not user:
             return jsonify({"error": f"Usuario {user_id} no encontrado"}), 404

        # Llamar al servicio
        recent_tastings = UsuarioServicio.get_recent_friends_activity(g.db, user_id, limit=5)
        
        # Formatear respuesta
        response = []
        for tasting in recent_tastings:
            data = tasting.to_dict()
            
            # Enriquecer con datos del amigo (nombre y avatar)
            if tasting.usuario:
                data['nombre_usuario'] = tasting.usuario.username
            
            # Enriquecer con nombre de la cerveza (útil para el feed)
            if tasting.cerveza:
                data['nombre_cerveza'] = tasting.cerveza.nombre
                
            response.append(data)

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500

# ENDPOINTS DE SOLICITUDES DE AMISTAD

@usuario_bp.route("/usuarios/<int:user_id>/solicitudes/", methods=["POST"])
def send_friend_request(user_id: int):
    """
    El usuario (user_id) envía una solicitud a otro usuario (friend_id en el body)
    """
    data = request.json
    friend_id = data.get('friend_id')

    if not friend_id:
        return jsonify({"error": "Se requiere friend_id"}), 400
    
    if user_id == friend_id:
        return jsonify({"error": "No puedes enviarte solicitud a ti mismo"}), 400

    try:
        UsuarioServicio.crear_solicitud_amistad(g.db, sender_id=user_id, receiver_id=friend_id)
        return jsonify({"message": "Solicitud enviada correctamente"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuario_bp.route("/usuarios/<int:user_id>/solicitudes/", methods=["GET"])
def get_pending_requests(user_id: int):
    """
    Ver todas las solicitudes pendientes que ha recibido el usuario
    """
    try:
        requests = UsuarioServicio.obtener_solicitudes_pendientes(g.db, user_id)
        return jsonify([req.to_dict() for req in requests]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuario_bp.route("/usuarios/<int:user_id>/solicitudes/<int:sender_id>/aceptar", methods=["POST"])
def accept_request(user_id: int, sender_id: int):
    """
    El usuario (user_id) acepta la solicitud enviada por sender_id
    """
    try:
        success = UsuarioServicio.aceptar_solicitud(g.db, receiver_id=user_id, sender_id=sender_id)
        if success:
            return jsonify({"message": "Solicitud aceptada. Ahora son amigos."}), 200
        else:
            return jsonify({"error": "Solicitud no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuario_bp.route("/usuarios/<int:user_id>/solicitudes/<int:sender_id>", methods=["DELETE"])
def reject_request(user_id: int, sender_id: int):
    """
    El usuario (user_id) rechaza (borra) la solicitud enviada por sender_id
    """
    try:
        success = UsuarioServicio.rechazar_solicitud(g.db, receiver_id=user_id, sender_id=sender_id)
        if success:
            return jsonify({"message": "Solicitud rechazada/eliminada."}), 200
        else:
            return jsonify({"error": "Solicitud no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    