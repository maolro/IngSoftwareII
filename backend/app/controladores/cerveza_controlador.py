from flask import Blueprint, jsonify, request, abort, g
from app.servicios.cerveza_servicio import CervezaService
from app.servicios.usuario_servicio import UsuarioServicio

# Uso blueprint, para meter las APIs en "paquetes" y ser más modular.
cerveza_bp = Blueprint('cerveza_bp', __name__)

@cerveza_bp.route("/cervezas/", methods=["POST"])
def api_crear_cerveza():
    """
    Endpoint para RF-3.2 (DAR DE ALTA UNA CERVEZA).
    Espera un JSON con los datos de la cerveza.
    """
    data = request.json
    if not data or 'nombre' not in data:
        abort(400, "El campo 'nombre' es obligatorio.")
        
    try:
        nueva_cerveza = CervezaService.crear_cerveza(g.db, data)
        cerveza_dict = nueva_cerveza.to_dict()
        cerveza_dict['valoracion_promedio'] = 0.0 # Valor inicial
        return jsonify(cerveza_dict), 201 # 201 Created
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 409    
    except Exception as e:
        # Aquí usamos 500 para un error genérico
        abort(500, description=str(e))

@cerveza_bp.route("/cervezas/", methods=["GET"])
def api_buscar_cervezas():
    """
    Endpoint para RF-3.1 (Buscar) y RF-5.7 (Filtrar).
    --- AHORA OPTIMIZADO (SIN N+1) ---
    """
    
    # 1. Obtenemos parámetros
    q = request.args.get('q')
    estilo = request.args.get('estilo')
    pais = request.args.get('pais')
    
    # 2. Llamamos al servicio (que ahora devuelve tuplas)
    #    Restauramos el try/except para robustez
    try:
        cervezas_con_valoracion = CervezaService.buscar_cervezas(g.db, q=q, estilo=estilo, pais=pais)
        
        # 3. Preparamos la respuesta
        resultado = []
        
        # 'cervezas_con_valoracion' es list[tuple(Cerveza, float)]
        for cerveza, valoracion in cervezas_con_valoracion:
            # Obtiene la valoración promedio
            valoracion = CervezaService.get_valoracion_promedio(g.db, cerveza.id) 
            # Convierte a diccionario
            cerveza_dict = cerveza.to_dict()
            # Asignamos la valoración (manejando el caso None si no tiene ratings)
            val_promedio_final = round(valoracion, 2) if valoracion is not None else 0.0
            # Prepara el resultado
            resultado.append({
                "id": cerveza_dict['id'],
                "nombre": cerveza_dict['nombre'],
                "estilo": cerveza_dict['estilo'],
                "pais_procedencia": cerveza_dict.get('pais_procedencia'),
                "porcentaje_alcohol": cerveza_dict.get('porcentaje_alcohol'),
                "valoracion_promedio": val_promedio_final
            })
            
        return jsonify(resultado), 200

    except Exception as e:
        abort(500, description=str(e))

@cerveza_bp.route("/cervezas/<int:id_cerveza>/", methods=["GET"])
def api_get_detalle_cerveza(id_cerveza: int):
    """
    Endpoint para RF-3.4 (Detalle con valoración).
    """
    try:
        cerveza = CervezaService.get_cerveza_por_id(g.db, id_cerveza)
        if not cerveza:
            abort(404, "Cerveza no encontrada.") # Usamos 404
            
        cerveza_dict = cerveza.to_dict()
        # cerveza_dict['valoracion_promedio'] = CervezaService.get_valoracion_promedio(g.db, id_cerveza)
        
        return jsonify(cerveza_dict), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cerveza_bp.route("/cervezas/<int:cerveza_id>/", methods=["DELETE"])
def eliminar_cerveza(cerveza_id: int):
    """
    Elimina una cerveza por su ID
    """
    try:
        eliminado = CervezaService.eliminar_cerveza(db=g.db, cerveza_id=cerveza_id)
        if not eliminado:
            return jsonify({"error": "Cerveza no encontrada"}), 404
        return jsonify({"message": "Cerveza eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cerveza_bp.route("/usuarios/<int:id_usuario>/cervezas/favoritas/", methods=["GET"])
def api_get_favoritas(id_usuario: int):
    """
    Endpoint para RF-5.4 (Top 3 favoritas del usuario).
    """
    try:
        # Si el usuario no existe, devuelve error 404
        if not UsuarioServicio.get_usuario_by_id(id_usuario):
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        favoritas = CervezaService.get_favoritas_usuario(g.db, id_usuario)
        # Si el usuario existe pero no tiene favoritas, devolver [] (lista vacía) 
        return jsonify(favoritas), 200
    except Exception as e:
        abort(500, description=str(e))
        
@cerveza_bp.route("/cervezas/estilos/", methods=["GET"])
def api_get_estilos():
    """
    Endpoint para RNF-4 (Obtener lista de estilos únicos).
    """
    try:
        estilos = CervezaService.get_estilos_unicos(g.db)
        return jsonify(estilos), 200
    except Exception as e:
        abort(500, description=str(e))

@cerveza_bp.route("/cervezas/paises/", methods=["GET"])
def api_get_paises():
    """
    Endpoint para RNF-4 (Obtener lista de países únicos).
    """
    try:
        paises = CervezaService.get_paises_unicos(g.db)
        return jsonify(paises), 200
    except Exception as e:
        abort(500, description=str(e))