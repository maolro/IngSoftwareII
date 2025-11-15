from flask import Blueprint, jsonify, request, abort, g
from app.servicios.cerveceria_servicio import CerveceriaService

# Blueprint para modularizar las APIs de cervecerías
cerveceria_bp = Blueprint('cerveceria_bp', __name__)

@cerveceria_bp.route("/cervecerias/", methods=["POST"])
def api_crear_cerveceria():
    """
    Endpoint para RF-3.6 (DAR DE ALTA UNA CERVECERÍA).
    Crea una cervecería si no existe con el mismo nombre.
    """
    data = request.json
    if not data or 'nombre' not in data or 'direccion' not in data:
        abort(400, "Los campos 'nombre' y 'direccion' son obligatorios.")
        
    try:
        nueva_cerveceria = CerveceriaService.crear_cerveceria(g.db, data)
        cerveceria_dict = nueva_cerveceria.to_dict()
        return jsonify(cerveceria_dict), 201  # 201 Created
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500
    
@cerveceria_bp.route("/cervecerias/<int:cerveceria_id>/", methods=["DELETE"])
def eliminar_cerveza(cerveceria_id: int):
    """
    Elimina una cerveza por su ID
    """
    try:
        eliminado = CerveceriaService.eliminar_cerveceria(db=g.db, cerveceria_id=cerveceria_id)
        if not eliminado:
            return jsonify({"error": "Cerveceria no encontrada"}), 404
        return jsonify({"message": "Cerveceria eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cerveceria_bp.route("/cervecerias/", methods=["GET"])
def api_buscar_cervecerias():
    """
    Endpoint para listar o filtrar cervecerías.
    Soporta búsqueda por nombre y filtrado por ciudad o país.
    """
    q = request.args.get('q')
    ciudad = request.args.get('ciudad')
    pais = request.args.get('pais')
    
    try:
        cervecerias = CerveceriaService.buscar_cervecerias(g.db, q=q, ciudad=ciudad, pais=pais)
        resultado = [c.to_dict() for c in cervecerias]
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500


@cerveceria_bp.route("/cervecerias/<int:id_cerveceria>/", methods=["GET"])
def api_get_detalle_cerveceria(id_cerveceria: int):
    """
    Endpoint para obtener detalle de una cervecería específica.
    Incluye información general y cantidad de 'me gusta'.
    """
    try:
        cerveceria = CerveceriaService.get_cerveceria_por_id(g.db, id_cerveceria)
        if not cerveceria:
            return jsonify({"error": "Cerveceria no encontrada"}), 404
                
        cerveceria_dict = cerveceria.to_dict()
        return jsonify(cerveceria_dict), 200
    
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500

@cerveceria_bp.route("/cervecerias/sugeridas/", methods=["GET"])
def api_sugerencias_cervecerias():
    """
    Endpoint para RNF-8 (geolocalización).
    Devuelve cervecerías cercanas al usuario según lat/lon y radio.
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        radio = request.args.get('radio', default=5, type=float)
        
        if lat is None or lon is None:
            abort(400, "Los parámetros 'lat' y 'lon' son obligatorios.")
        
        sugerencias = CerveceriaService.get_cervecerias_cercanas(g.db, lat, lon, radio)
        return jsonify([c.to_dict() for c in sugerencias]), 200
    
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500
