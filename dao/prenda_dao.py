from conexion import Conexion
from models.prenda import Prenda


class PrendaDAO:

    @classmethod
    def seleccionar(cls):
        sql = """
            SELECT id_prenda, id_pedido, tipo_prenda, modelo, talla, color, precio
            FROM prendas
            ORDER BY id_prenda
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()

                prendas = []
                for reg in registros:
                    prendas.append(Prenda(
                        id_prenda=reg[0],
                        id_pedido=reg[1],
                        tipo_prenda=reg[2],
                        modelo=reg[3],
                        talla=reg[4],
                        color=reg[5],
                        precio=reg[6],
                    ))
                return prendas

    @classmethod
    def obtener_por_pedido(cls, id_pedido):
        sql = """
            SELECT id_prenda, id_pedido, tipo_prenda, modelo, talla, color, precio
            FROM prendas
            WHERE id_pedido = %s
            ORDER BY id_prenda
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_pedido,))
                registros = cursor.fetchall()
                return [
                    Prenda(id_prenda=r[0], id_pedido=r[1], tipo_prenda=r[2], modelo=r[3], talla=r[4], color=r[5], precio=r[6])
                    for r in registros
                ]

    @classmethod
    def insertar(cls, prenda):
        sql = """
            INSERT INTO prendas (id_pedido, tipo_prenda, modelo, talla, color, precio)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (prenda.id_pedido, prenda.tipo_prenda, prenda.modelo, prenda.talla, prenda.color, prenda.precio)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def actualizar(cls, prenda):
        sql = """
            UPDATE prendas
            SET id_pedido = %s, tipo_prenda = %s, modelo = %s, talla = %s, color = %s, precio = %s
            WHERE id_prenda = %s
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (prenda.id_pedido, prenda.tipo_prenda, prenda.modelo, prenda.talla, prenda.color, prenda.precio, prenda.id_prenda)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def eliminar(cls, id_prenda):
        sql = "DELETE FROM prendas WHERE id_prenda = %s"
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_prenda,))
                conn.commit()
                return cursor.rowcount
