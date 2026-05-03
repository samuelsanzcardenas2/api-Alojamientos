from functools import wraps

import jwt
from flask import request, jsonify, current_app


def requiere_token(f):
    """Decorador que exige un token JWT valido en el header Authorization.

    Inyecta `usuario_id` como argumento en la funcion decorada.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                'success': False,
                'error': {'message': 'Token no proporcionado.'}
            }), 401

        # Formato esperado: "Bearer <token>"
        partes = auth_header.split()
        if len(partes) != 2 or partes[0].lower() != 'bearer':
            return jsonify({
                'success': False,
                'error': {'message': 'Formato de token invalido. Use: Bearer <token>'}
            }), 401

        token = partes[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'],
            )
            usuario_id = payload['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'error': {'message': 'Token expirado.'}
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': {'message': 'Token invalido.'}
            }), 401

        return f(*args, usuario_id=usuario_id, **kwargs)
    return wrapper