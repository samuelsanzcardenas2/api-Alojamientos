from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.alojamientos.dtos import CrearAlojamientoDTO, ActualizarAlojamientoDTO
from app.seguridad import requiere_token

alojamientos_bp = Blueprint('alojamientos', __name__)

# El app factory asignara el servicio correspondiente
alojamiento_servicio = None


@alojamientos_bp.route('', methods=['GET'])
def listar_alojamientos():
    """Devuelve la lista de alojamientos publicos."""
    lista = alojamiento_servicio.listar_todos()
    return jsonify({
        'success': True,
        'message': 'Alojamientos listados.',
        'data': lista,
    }), 200


@alojamientos_bp.route('', methods=['POST'])
@requiere_token
def crear_alojamiento(usuario_id):
    """Crea un nuevo alojamiento para el usuario autenticado."""
    datos = request.get_json(silent=True) or {}
    dto = CrearAlojamientoDTO()
    try:
        datos_validados = dto.load(datos)
    except ValidationError as err:
        return jsonify({
            'success': False,
            'error': {'message': 'Datos de entrada invalidos.', 'details': err.messages}
        }), 400

    alojamiento = alojamiento_servicio.crear_alojamiento(datos_validados, usuario_id)
    return jsonify({
        'success': True,
        'message': 'Alojamiento creado con exito.',
        'data': alojamiento.to_dict(),
    }), 201


@alojamientos_bp.route('/<int:alojamiento_id>', methods=['GET'])
def obtener_alojamiento(alojamiento_id):
    """Devuelve el detalle de un alojamiento."""
    detalle = alojamiento_servicio.obtener_detalle(alojamiento_id)
    return jsonify({
        'success': True,
        'message': 'Detalle del alojamiento obtenido.',
        'data': detalle,
    }), 200


@alojamientos_bp.route('/<int:alojamiento_id>', methods=['PATCH'])
@requiere_token
def actualizar_alojamiento(alojamiento_id, usuario_id):
    """Actualiza el alojamiento si es propietario o admin."""
    datos = request.get_json(silent=True) or {}
    dto = ActualizarAlojamientoDTO()
    try:
        datos_validados = dto.load(datos)
    except ValidationError as err:
        return jsonify({
            'success': False,
            'error': {'message': 'Datos de entrada invalidos.', 'details': err.messages}
        }), 400

    alojamiento_modificado = alojamiento_servicio.actualizar_alojamiento(alojamiento_id, usuario_id, datos_validados)
    return jsonify({
        'success': True,
        'message': 'Alojamiento actualizado.',
        'data': alojamiento_modificado,
    }), 200


@alojamientos_bp.route('/<int:alojamiento_id>', methods=['DELETE'])
@requiere_token
def eliminar_alojamiento(alojamiento_id, usuario_id):
    """Elimina el alojamiento si es propietario o admin."""
    alojamiento_servicio.eliminar_alojamiento(alojamiento_id, usuario_id)
    return '', 204
