from conexion import Conexion
from models.pedido import Pedido


class PedidoDAO:

    @classmethod
    def seleccionar(cls):
        sql = """
            SELECT
                p.id_pedido, p.id_cliente, cl.nombre_completo, p.id_empleado,
                e.nombre, p.fecha_pedido, p.fecha_entrega, p.anticipo, p.total, p.estado
            FROM pedido p
            INNER JOIN clientes cl ON p.id_cliente = cl.id_cliente
            LEFT JOIN empleados e ON p.id_empleado = e.id_empleado
            ORDER BY p.fecha_pedido DESC, p.id_pedido DESC
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()
                pedidos = []
                for r in registros:
                    pedidos.append({
                        "id_pedido": r[0],
                        "id_cliente": r[1],
                        "nombre_cliente": r[2],
                        "id_empleado": r[3],
                        "nombre_empleado": r[4] or "Sin asignar",
                        "fecha_pedido": r[5],
                        "fecha_entrega": r[6],
                        "anticipo": r[7],
                        "total": r[8],
                        "estado": r[9],
                    })
                return pedidos

    @classmethod
    def obtener_por_cliente(cls, id_cliente):
        sql = """
            SELECT id_pedido, id_cliente, id_empleado, fecha_pedido,
                   fecha_entrega, anticipo, total, estado
            FROM pedido
            WHERE id_cliente = %s
            ORDER BY fecha_pedido DESC
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_cliente,))
                registros = cursor.fetchall()
                return [
                    Pedido(
                        id_pedido=r[0], id_cliente=r[1], id_empleado=r[2],
                        fecha_pedido=r[3], fecha_entrega=r[4], anticipo=r[5],
                        total=r[6], estado=r[7],
                    )
                    for r in registros
                ]

    @classmethod
    def insertar(cls, pedido):
        sql = """
            INSERT INTO pedido (id_cliente, id_empleado, fecha_pedido, fecha_entrega, anticipo, total, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_pedido
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (
                    pedido.id_cliente, pedido.id_empleado, pedido.fecha_pedido,
                    pedido.fecha_entrega, pedido.anticipo, pedido.total, pedido.estado,
                )
                cursor.execute(sql, valores)
                nuevo_id = cursor.fetchone()[0]
                conn.commit()
                return nuevo_id

    @classmethod
    def actualizar(cls, pedido):
        sql = """
            UPDATE pedido
            SET id_cliente = %s, id_empleado = %s, fecha_pedido = %s, fecha_entrega = %s,
                anticipo = %s, total = %s, estado = %s
            WHERE id_pedido = %s
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (
                    pedido.id_cliente, pedido.id_empleado, pedido.fecha_pedido,
                    pedido.fecha_entrega, pedido.anticipo, pedido.total, pedido.estado,
                    pedido.id_pedido,
                )
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def eliminar(cls, id_pedido):
        sql = "DELETE FROM pedido WHERE id_pedido = %s"
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_pedido,))
                conn.commit()
                return cursor.rowcount

  