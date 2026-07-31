from conexion import Conexion
from models.empleado import Empleado


class EmpleadoDAO:

    @classmethod
    def seleccionar(cls):
        sql = """
            SELECT id_empleado, nombre, telefono, puesto
            FROM empleados
            ORDER BY id_empleado
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()

                empleados = []
                for reg in registros:
                    empleados.append(Empleado(
                        id_empleado=reg[0],
                        nombre=reg[1],
                        telefono=reg[2],
                        puesto=reg[3],
                    ))
                return empleados

    @classmethod
    def obtener_por_id(cls, id_empleado):
        sql = """
            SELECT id_empleado, nombre, telefono, puesto
            FROM empleados
            WHERE id_empleado = %s
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_empleado,))
                reg = cursor.fetchone()
                if reg is None:
                    return None
                return Empleado(id_empleado=reg[0], nombre=reg[1], telefono=reg[2], puesto=reg[3])

    @classmethod
    def insertar(cls, empleado):
        sql = "INSERT INTO empleados (nombre, telefono, puesto) VALUES (%s, %s, %s)"
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (empleado.nombre, empleado.telefono, empleado.puesto)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def actualizar(cls, empleado):
        sql = """
            UPDATE empleados
            SET nombre = %s, telefono = %s, puesto = %s
            WHERE id_empleado = %s
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (empleado.nombre, empleado.telefono, empleado.puesto, empleado.id_empleado)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def eliminar(cls, id_empleado):
        sql = "DELETE FROM empleados WHERE id_empleado = %s"
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_empleado,))
                conn.commit()
                return cursor.rowcount
