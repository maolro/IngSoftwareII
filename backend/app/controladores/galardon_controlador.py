from flask import Blueprint, jsonify, request, abort, g
from sqlalchemy.orm import Session
from typing import List
from app.servicios import galardon_servicio

# Blueprint para las rutas de galardones
galardon_bp = Blueprint('galardon_bp', __name__)

@galardon_bp.route("/galardones/", methods=["POST"])
def crear_nuevo_galardon():
    """
    Crea un nuevo galardón (RF-4.5)
    """
    data = request.json
    if not data:
        abort(400, "No se proporcionaron datos para crear el galardon")
    
    # Validar campos obligatorios
    required_fields = ['nombre']
    for field in required_fields:
        if field not in data:
            abort(400, f"El campo '{field}' es obligatorio")
    
    try:
        nuevo_galardon = galardon_servicio.crear_galardon(db=g.db, galardon=data)
        return jsonify(nuevo_galardon.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        abort(500, description=str(e))

@galardon_bp.route("/galardones/", methods=["GET"])
def leer_galardones():
    """
    Obtiene una lista de todos los tipos de galardones
    """
    try:
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        
        galardones = galardon_servicio.obtener_galardones(db=g.db, skip=skip, limit=limit)
        
        # Convierte a lista de diccionarios
        galardones_dict = [galardon.to_dict() for galardon in galardones]
        return jsonify(galardones_dict), 200
    except Exception as e:
        abort(500, description=str(e))

@galardon_bp.route("/galardones/<int:galardon_id>/", methods=["GET"])
def leer_galardon_por_id(galardon_id: int):
    """
    Obtiene un tipo de galardón por su ID
    """
    try:
        db_galardon = galardon_servicio.obtener_galardon(db=g.db, galardon_id=galardon_id)
        if db_galardon is None:
            return jsonify({"error": "Galardon no encontrado"}), 404
        return jsonify(db_galardon.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@galardon_bp.route("/galardones/<int:galardon_id>/", methods=["PUT"])
def actualizar_galardon_por_id(galardon_id: int):
    """
    Actualiza un galardón por su ID (RF-4.5 - Admin)
    """
    data = request.json
    if not data:
        return jsonify({"error": "No se proporcionaron datos para actualizar el galardon"}), 400
    
    try:
        db_galardon = galardon_servicio.actualizar_galardon(
            db=g.db, 
            galardon_id=galardon_id, 
            galardon=data
        )
        if db_galardon is None:
            return jsonify({"error": "Galardon no encontrado"}), 404
        return jsonify(db_galardon.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@galardon_bp.route("/galardones/<int:galardon_id>/", methods=["DELETE"])
def eliminar_galardon_por_id(galardon_id: int):
    """
    Elimina un galardón por su ID (RF-4.5 - Admin)
    """
    try:
        eliminado = galardon_servicio.eliminar_galardon(db=g.db, galardon_id=galardon_id)
        if not eliminado:
            return jsonify({"error": "Galardon no encontrado"}), 404
        return jsonify({"message": "Galardon eliminado exitosamente"}), 200
    except Exception as e:
        abort(500, description=str(e))

@galardon_bp.route("/usuarios/<int:usuario_id>/galardones", methods=["GET"])
def leer_galardones_de_usuario(usuario_id: int):
    """
    Obtiene la lista de galardones que ha ganado un usuario específico (RF-5.5)
    """
    try:
        galardones = galardon_servicio.obtener_galardones_de_usuario(db=g.db, usuario_id=usuario_id)
        
        if not galardones:
            # Si no tiene galardones devuelve lista vacía
            return jsonify([]), 200
        
        # Convierte a lista de diccionarios
        galardones_dict = []
        for usuario_galardon in galardones:
            galardon_dict = usuario_galardon.to_dict()
            galardones_dict.append(galardon_dict)
            
        return jsonify(galardones_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@galardon_bp.route("/usuarios/<int:usuario_id>/galardones", methods=["POST"])
def asignar_galardon_a_usuario(usuario_id: int):
    """
    Asigna un galardón a un usuario específico
    """
    data = request.json
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    # Validate required fields
    required_fields = ['galardon_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"El campo '{field}' es obligatorio"}), 400
    
    try:
        # Extract optional fields with defaults
        galardon_id = data['galardon_id']
        nivel_actual = data.get('nivel_actual', 1)
        progreso_actual = data.get('progreso_actual', 0)
        
        # Call service layer
        usuario_galardon = galardon_servicio.asignar_galardon_a_usuario(
            db=g.db,
            usuario_id=usuario_id,
            galardon_id=galardon_id,
            nivel_actual=nivel_actual,
            progreso_actual=progreso_actual
        )
        
        return jsonify(usuario_galardon.to_dict()), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500