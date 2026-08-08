from conexion import Conexion
from models.cita import Cita


class CitaDAO:

    @classmethod
    def obtener_por_cliente(cls, id_cliente):
        sql = """
            SELECT
                c.id_cita,
                c.id_cliente,
                cl.nombre_completo,
                c.id_empleado,
                e.nombre,
                c.fecha,
                c.hora,
                c.motivo
            FROM cita c
            INNER JOIN clientes cl ON c.id_cliente = cl.id_cliente
            INNER JOIN empleados e ON c.id_empleado = e.id_empleado
            WHERE c.id_cliente = %s
            ORDER BY c.fecha DESC, c.hora DESC
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_cliente,))
                registros = cursor.fetchall()

                citas = []
                for reg in registros:
                    citas.append({
                        "id_cita": reg[0],
                        "id_cliente": reg[1],
                        "nombre_cliente": reg[2],
                        "id_empleado": reg[3],
                        "nombre_empleado": reg[4],
                        "fecha": reg[5],
                        "hora": reg[6],
                        "motivo": reg[7],
                    })
                return citas

    @classmethod
    def seleccionar(cls):
        sql = """
            SELECT
                c.id_cita,
                c.id_cliente,
                cl.nombre_completo,
                c.id_empleado,
                e.nombre,
                c.fecha,
                c.hora,
                c.motivo
            FROM cita c
            INNER JOIN clientes cl ON c.id_cliente = cl.id_cliente
            INNER JOIN empleados e ON c.id_empleado = e.id_empleado
            ORDER BY c.fecha, c.hora
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()

                citas = []
                for reg in registros:
                    citas.append({
                        "id_cita": reg[0],
                        "id_cliente": reg[1],
                        "nombre_cliente": reg[2],
                        "id_empleado": reg[3],
                        "nombre_empleado": reg[4],
                        "fecha": reg[5],
                        "hora": reg[6],
                        "motivo": reg[7],
                    })
                return citas

    @classmethod
    def insertar(cls, cita):
        sql = """
            INSERT INTO cita (id_cliente, id_empleado, fecha, hora, motivo)
            VALUES (%s, %s, %s, %s, %s)
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (cita.id_cliente, cita.id_empleado, cita.fecha, cita.hora, cita.motivo)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def actualizar(cls, cita):
        sql = """
            UPDATE cita
            SET id_cliente = %s, id_empleado = %s, fecha = %s, hora = %s, motivo = %s
            WHERE id_cita = %s
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (cita.id_cliente, cita.id_empleado, cita.fecha, cita.hora, cita.motivo, cita.id_cita)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def eliminar(cls, id_cita):
        sql = "DELETE FROM cita WHERE id_cita = %s"
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_cita,))
                conn.commit()
                return cursor.rowcount
