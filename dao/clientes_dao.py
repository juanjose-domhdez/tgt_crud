from conexion import Conexion
from models.clientes import Cliente


class ClienteDAO:
    """
    NOTA: por ahora solo se agrega 'seleccionar', necesario para el
    combo de clientes del módulo de Citas. El CRUD completo
    (insertar/actualizar/eliminar) lo debe terminar quien lleva el
    módulo de clientes.
    """

    @classmethod
    def seleccionar(cls):
        sql = """
            SELECT id_cliente, nombre_completo, telefono, fecha_registro
            FROM clientes
            ORDER BY nombre_completo
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()
                return [
                    Cliente(id_cliente=r[0], nombre_completo=r[1], telefono=r[2], fecha_registro=r[3])
                    for r in registros
                ]
