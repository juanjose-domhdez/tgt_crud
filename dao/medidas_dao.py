from conexion import Conexion
from models.medidas import Medida


class MedidaDAO:

    @classmethod
    def obtener_por_cliente(cls, id_cliente):
        sql = """
            SELECT m.id_medida, m.id_pedido, m.pecho, m.cintura, m.hombros, m.manga, m.largo_pantalon
            FROM medidas m
            INNER JOIN pedido p ON m.id_pedido = p.id_pedido
            WHERE p.id_cliente = %s
            ORDER BY m.id_medida DESC
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_cliente,))
                registros = cursor.fetchall()
                return [
                    Medida(
                        id_medida=r[0], id_pedido=r[1], pecho=r[2], cintura=r[3],
                        hombros=r[4], manga=r[5], largo_pantalon=r[6],
                    )
                    for r in registros
                ]

    @classmethod
    def seleccionar(cls):
        sql = """
            SELECT id_medida, id_pedido, pecho, cintura, hombros, manga, largo_pantalon
            FROM medidas
            ORDER BY id_medida DESC
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()
                return [
                    Medida(
                        id_medida=r[0], id_pedido=r[1], pecho=r[2], cintura=r[3],
                        hombros=r[4], manga=r[5], largo_pantalon=r[6],
                    )
                    for r in registros
                ]

    @classmethod
    def insertar(cls, medida):
        sql = """
            INSERT INTO medidas (id_pedido, pecho, cintura, hombros, manga, largo_pantalon)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (medida.id_pedido, medida.pecho, medida.cintura, medida.hombros, medida.manga, medida.largo_pantalon)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def actualizar(cls, medida):
        sql = """
            UPDATE medidas
            SET id_pedido = %s, pecho = %s, cintura = %s, hombros = %s, manga = %s, largo_pantalon = %s
            WHERE id_medida = %s
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (medida.id_pedido, medida.pecho, medida.cintura, medida.hombros, medida.manga, medida.largo_pantalon, medida.id_medida)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def eliminar(cls, id_medida):
        sql = "DELETE FROM medidas WHERE id_medida = %s"
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_medida,))
                conn.commit()
                return cursor.rowcount
