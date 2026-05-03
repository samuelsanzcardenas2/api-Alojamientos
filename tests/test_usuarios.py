import json


class TestRegistroUsuario:
    """Pruebas de integracion para registro de usuarios."""

    def test_registro_exitoso(self, client):
        """Registro con datos validos debe crear usuario y responder 201."""
        resp = client.post('/api/v1/usuarios/registro', json={
            'correo': 'nuevo@ejemplo.com',
            'contrasena': '123456',
        })
        datos = json.loads(resp.data)

        assert resp.status_code == 201
        assert datos['success'] is True
        assert datos['data']['correo'] == 'nuevo@ejemplo.com'

    def test_email_duplicado(self, client):
        """Registrar dos veces el mismo email debe responder 400."""
        client.post('/api/v1/usuarios/registro', json={
            'correo': 'duplicado@ejemplo.com',
            'contrasena': '123456',
        })
        resp = client.post('/api/v1/usuarios/registro', json={
            'correo': 'duplicado@ejemplo.com',
            'contrasena': '123456',
        })
        assert resp.status_code == 400

    def test_contrasena_corta(self, client):
        """Contraseña menor a 6 caracteres debe responder 400."""
        resp = client.post('/api/v1/usuarios/registro', json={
            'correo': 'corta@ejemplo.com',
            'contrasena': '123',
        })
        assert resp.status_code == 400

    def test_email_invalido(self, client):
        """Email sin formato valido debe responder 400."""
        resp = client.post('/api/v1/usuarios/registro', json={
            'correo': 'no-es-email',
            'contrasena': '123456',
        })
        assert resp.status_code == 400


class TestLogin:
    """Pruebas de integracion para login."""

    def test_login_exitoso(self, client):
        """Login con credenciales validas debe devolver token y responder 200."""
        # Primero registrar
        client.post('/api/v1/usuarios/registro', json={
            'correo': 'login@ejemplo.com',
            'contrasena': '123456',
        })
        resp = client.post('/api/v1/usuarios/login', json={
            'correo': 'login@ejemplo.com',
            'contrasena': '123456',
        })
        datos = json.loads(resp.data)

        assert resp.status_code == 200
        assert datos['success'] is True
        assert 'access_token' in datos['data']

    def test_credenciales_invalidas(self, client):
        """Login con contraseña incorrecta debe responder 401."""
        client.post('/api/v1/usuarios/registro', json={
            'correo': 'wrong@ejemplo.com',
            'contrasena': '123456',
        })
        resp = client.post('/api/v1/usuarios/login', json={
            'correo': 'wrong@ejemplo.com',
            'contrasena': 'incorrecta',
        })
        assert resp.status_code == 401

    def test_usuario_no_existente(self, client):
        """Login con usuario que no existe debe responder 401."""
        resp = client.post('/api/v1/usuarios/login', json={
            'correo': 'fantasma@ejemplo.com',
            'contrasena': '123456',
        })
        assert resp.status_code == 401


class TestPerfil:
    """Pruebas de integracion para consulta y actualizacion de perfil."""

    def test_perfil_sin_token(self, client):
        """GET /perfil sin token debe responder 401."""
        resp = client.get('/api/v1/usuarios/perfil')
        assert resp.status_code == 401

    def test_perfil_con_token(self, client, usuario_auth):
        """GET /perfil con token valido debe responder 200."""
        resp = client.get('/api/v1/usuarios/perfil', headers=usuario_auth)
        datos = json.loads(resp.data)

        assert resp.status_code == 200
        assert datos['success'] is True
        assert 'data' in datos

    def test_actualizar_perfil(self, client, usuario_auth):
        """PATCH /perfil con datos validos debe responder 200."""
        resp = client.patch('/api/v1/usuarios/perfil', headers=usuario_auth, json={
            'nombre': 'Maria',
            'apellido': 'Lopez',
            'telefono': '+34600111222',
        })
        datos = json.loads(resp.data)

        assert resp.status_code == 200
        assert datos['data']['nombre'] == 'Maria'
        assert datos['data']['apellido'] == 'Lopez'

    def test_actualizacion_parcial(self, client, usuario_auth):
        """PATCH /perfil con un solo campo debe actualizar solo ese campo."""
        # Establecer estado inicial dentro del propio test
        r1 = client.patch('/api/v1/usuarios/perfil', headers=usuario_auth, json={
            'nombre': 'Ana',
            'apellido': 'Garcia',
        })
        assert r1.status_code == 200

        # Actualizar solo el telefono
        resp = client.patch('/api/v1/usuarios/perfil', headers=usuario_auth, json={
            'telefono': '+34600333444',
        })
        datos = json.loads(resp.data)

        assert resp.status_code == 200
        assert datos['data']['telefono'] == '+34600333444'
        # Los campos establecidos antes no se borran
        assert datos['data']['nombre'] == 'Ana'
        assert datos['data']['apellido'] == 'Garcia'