from conexion import Conexion
from models.clientes import Cliente


class ClienteDAO:

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

    @classmethod
    def obtener_por_id(cls, id_cliente):
        sql = """
            SELECT id_cliente, nombre_completo, telefono, fecha_registro
            FROM clientes
            WHERE id_cliente = %s
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_cliente,))
                reg = cursor.fetchone()
                if reg is None:
                    return None
                return Cliente(id_cliente=reg[0], nombre_completo=reg[1], telefono=reg[2], fecha_registro=reg[3])

    @classmethod
    def buscar_por_telefono(cls, telefono):
        if not telefono:
            return None
        sql = """
            SELECT id_cliente, nombre_completo, telefono, fecha_registro
            FROM clientes
            WHERE telefono = %s
            LIMIT 1
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (telefono,))
                reg = cursor.fetchone()
                if reg is None:
                    return None
                return Cliente(id_cliente=reg[0], nombre_completo=reg[1], telefono=reg[2], fecha_registro=reg[3])

    @classmethod
    def insertar(cls, cliente):
        sql = """
            INSERT INTO clientes (nombre_completo, telefono, fecha_registro)
            VALUES (%s, %s, %s)
            RETURNING id_cliente
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (cliente.nombre_completo, cliente.telefono, cliente.fecha_registro)
                cursor.execute(sql, valores)
                nuevo_id = cursor.fetchone()[0]
                conn.commit()
                return nuevo_id

    @classmethod
    def actualizar(cls, cliente):
        sql = """
            UPDATE clientes
            SET nombre_completo = %s, telefono = %s
            WHERE id_cliente = %s
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (cliente.nombre_completo, cliente.telefono, cliente.id_cliente)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def eliminar(cls, id_cliente):
        sql = "DELETE FROM clientes WHERE id_cliente = %s"
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_cliente,))
                conn.commit()
                return cursor.rowcount
