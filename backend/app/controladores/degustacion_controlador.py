# Endpoints HTTP relacionados con RF-3 (Degustaciones)
from flask import Blueprint, jsonify, request, abort, g
from sqlalchemy.orm import Session
from typing import List
from app.servicios import degustacion_servicio
import pdb

# Blueprint para las rutas de degustaciones
degustacion_bp = Blueprint('degustacion_bp', __name__)

@degustacion_bp.route("/degustaciones/", methods=["POST"])
def api_crear_degustacion():
    """
    Crea una nueva degustación (RF-3.1, RF-3.3, RF-3.5)
    """
    data = request.json
    # pdb.set_trace()
    if not data:
        abort(400, "No se proporcionaron datos para crear la degustación")
    
    try:
        nueva_degustacion = degustacion_servicio.crear_degustacion(db=g.db, degustacion_data=data)
        dict = nueva_degustacion.to_dict()
        return jsonify(dict), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@degustacion_bp.route("/degustaciones/", methods=["GET"])
def obtener_degustaciones():
    """
    Obtiene degustaciones con filtros opcionales
    """
    try:
        usuario_id = request.args.get('usuario_id', type=int)
        cerveza_id = request.args.get('cerveza_id', type=int)
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 50, type=int)
        
        if usuario_id:
            degustaciones = degustacion_servicio.obtener_degustaciones_por_usuario(
                db=g.db, usuario_id=usuario_id, skip=skip, limit=limit
            )
        elif cerveza_id:
            degustaciones = degustacion_servicio.obtener_degustaciones_por_cerveza(
                db=g.db, cerveza_id=cerveza_id, skip=skip, limit=limit
            )
        else:
            return jsonify({"error": "Se debe proporcionar usuario_id o cerveza_id"}), 400
        
        degustaciones_dict = [degustacion.to_dict() for degustacion in degustaciones]
        return jsonify(degustaciones_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@degustacion_bp.route("/degustaciones/<int:degustacion_id>/", methods=["GET"])
def obtener_degustacion_por_id(degustacion_id: int):
    """
    Obtiene una degustación por su ID
    """
    try:
        degustacion = degustacion_servicio.obtener_degustacion(db=g.db, degustacion_id=degustacion_id)
        if degustacion is None:
            return jsonify({"error": "Degustación no encontrada"}), 404
        return jsonify(degustacion.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@degustacion_bp.route("/degustaciones/<int:degustacion_id>/", methods=["PUT"])
def actualizar_degustacion(degustacion_id: int):
    """
    Actualiza una degustación existente
    """
    data = request.json
    if not data:
        return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400
    
    try:
        degustacion_actualizada = degustacion_servicio.actualizar_degustacion(
            db=g.db, degustacion_id=degustacion_id, degustacion_data=data
        )
        if degustacion_actualizada is None:
            return jsonify({"error": "Degustación no encontrada"}), 404
        return jsonify(degustacion_actualizada.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@degustacion_bp.route("/degustaciones/<int:degustacion_id>/", methods=["DELETE"])
def eliminar_degustacion(degustacion_id: int):
    """
    Elimina una degustación
    """
    try:
        eliminada = degustacion_servicio.eliminar_degustacion(db=g.db, degustacion_id=degustacion_id)
        if not eliminada:
            return jsonify({"error": "Degustación no encontrada"}), 404
        return jsonify({"message": "Degustación eliminada exitosamente"}), 200
    except Exception as e:
        abort(500, description=str(e))

@degustacion_bp.route("/degustaciones/mas-valoradas/", methods=["GET"])
def obtener_degustaciones_mas_valoradas():
    """
    Obtiene las degustaciones más valoradas con filtros (RF-5.6, RF-5.7)
    """
    try:
        estilo = request.args.get('estilo', type=str)
        pais = request.args.get('pais', type=str)
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        degustaciones = degustacion_servicio.obtener_degustaciones_mas_valoradas(
            db=g.db, estilo=estilo, pais=pais, skip=skip, limit=limit
        )
        
        degustaciones_dict = [degustacion.to_dict() for degustacion in degustaciones]
        return jsonify(degustaciones_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@degustacion_bp.route("/usuarios/<int:usuario_id>/actividad-amigos/", methods=["GET"])
def obtener_actividad_amigos(usuario_id: int):
    """
    Obtiene la actividad reciente de degustaciones de amigos (RF-3.8, RF-5.3)
    """
    try:
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 50, type=int)
        
        degustaciones = degustacion_servicio.obtener_actividad_amigos(
            db=g.db, usuario_id=usuario_id, skip=skip, limit=limit
        )
        
        degustaciones_dict = [degustacion.to_dict() for degustacion in degustaciones]
        return jsonify(degustaciones_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Rutas para comentarios en degustaciones ---

@degustacion_bp.route("/degustaciones/<int:degustacion_id>/comentarios/", methods=["POST"])
def agregar_comentario_degustacion(degustacion_id: int):
    """
    Agrega un comentario a una degustación (RF-2.7)
    """
    data = request.json
    if not data:
        abort(400, "No se proporcionaron datos para el comentario")
    
    # Incluir el degustacion_id en los datos
    data['degustacion_id'] = degustacion_id
    
    try:
        nuevo_comentario = degustacion_servicio.agregar_comentario_degustacion(db=g.db, comentario_data=data)
        return jsonify(nuevo_comentario.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        abort(500, description=str(e))

@degustacion_bp.route("/degustaciones/<int:degustacion_id>/comentarios/", methods=["GET"])
def obtener_comentarios_degustacion(degustacion_id: int):
    """
    Obtiene todos los comentarios de una degustación
    """
    try:
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        
        comentarios = degustacion_servicio.obtener_comentarios_degustacion(
            db=g.db, degustacion_id=degustacion_id, skip=skip, limit=limit
        )
        
        comentarios_dict = [comentario.to_dict() for comentario in comentarios]
        return jsonify(comentarios_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500