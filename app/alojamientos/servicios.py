from app import db
from app.dominios.alojamientos.modelos import Alojamiento
from app.dominios.alojamientos.repositorios import AlojamientoRepositorio
from app.dominios.usuarios.servicios import PermisoDenegadoError


# --- Excepciones de dominio ---

class AlojamientoNoEncontradoError(Exception):
    pass


# --- Servicio de alojamientos ---

class AlojamientoServicio:
    """Logica de negocio para alojamientos."""

    def crear_alojamiento(self, datos, usuario_id):
        """Crea un nuevo alojamiento asignado al usuario autenticado."""
        alojamiento = Alojamiento(
            titulo=datos['titulo'],
            descripcion=datos['descripcion'],
            precio_noche=datos['precio_noche'],
            ciudad=datos['ciudad'],
            usuario_id=usuario_id,
        )
        AlojamientoRepositorio.guardar(alojamiento)
        return alojamiento

    def listar_todos(self):
        """Devuelve lista de todos los alojamientos (publico)."""
        alojamientos = AlojamientoRepositorio.obtener_todos()
        return [a.to_dict() for a in alojamientos]

    def obtener_detalle(self, alojamiento_id):
        """Obtiene el detalle de un alojamiento (publico)."""
        alojamiento = AlojamientoRepositorio.obtener_por_id(alojamiento_id)
        if not alojamiento:
            raise AlojamientoNoEncontradoError(
                f'Alojamiento con id {alojamiento_id} no encontrado.'
            )
        return alojamiento.to_dict()

    def actualizar_alojamiento(self, alojamiento_id, usuario_id, datos):
        """Actualiza parcialmente un alojamiento. Solo propietario o admin."""
        alojamiento = AlojamientoRepositorio.obtener_por_id(alojamiento_id)
        if not alojamiento:
            raise AlojamientoNoEncontradoError(
                f'Alojamiento con id {alojamiento_id} no encontrado.'
            )

        # Consultar rol del usuario para verificar permiso
        from app.dominios.usuarios.repositorios import UsuarioRepositorio
        usuario = UsuarioRepositorio.obtener_por_id(usuario_id)
        es_admin = usuario is not None and usuario.rol == 'admin'

        if not es_admin and alojamiento.usuario_id != usuario_id:
            raise PermisoDenegadoError(
                'Permiso denegado. Solo el propietario o un administrador pueden editar este alojamiento.'
            )

        if datos.get('titulo') is not None:
            alojamiento.titulo = datos['titulo']
        if datos.get('descripcion') is not None:
            alojamiento.descripcion = datos['descripcion']
        if datos.get('precio_noche') is not None:
            alojamiento.precio_noche = datos['precio_noche']
        if datos.get('ciudad') is not None:
            alojamiento.ciudad = datos['ciudad']

        AlojamientoRepositorio.guardar(alojamiento)
        return alojamiento.to_dict()

    def eliminar_alojamiento(self, alojamiento_id, usuario_id):
        """Elimina un alojamiento. Solo propietario o admin."""
        alojamiento = AlojamientoRepositorio.obtener_por_id(alojamiento_id)
        if not alojamiento:
            raise AlojamientoNoEncontradoError(
                f'Alojamiento con id {alojamiento_id} no encontrado.'
            )

        # Consultar rol del usuario para verificar permiso
        from app.dominios.usuarios.repositorios import UsuarioRepositorio
        usuario = UsuarioRepositorio.obtener_por_id(usuario_id)
        es_admin = usuario is not None and usuario.rol == 'admin'

        if not es_admin and alojamiento.usuario_id != usuario_id:
            raise PermisoDenegadoError(
                'Permiso denegado. Solo el propietario o un administrador pueden eliminar este alojamiento.'
            )

        AlojamientoRepositorio.eliminar(alojamiento)