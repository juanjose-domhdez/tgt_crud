from conexion import Conexion
from models.prenda import Prenda


class PrendaDAO:

    @classmethod

    def seleccionar(cls):
        sql = "SELECT * FROM public.prendas ORDER BY id_prenda ASC;"
        
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()
                
                prendas = []
                for reg in registros:
                    if len(reg) >= 8:
                        prendas.append(Prenda(
                            id_prenda=reg[0],
                            tipo_prenda=reg[2],
                            modelo=reg[3],
                            talla=reg[4],
                            color=reg[5],
                            precio=reg[6],
                            stock=reg[7]
                        ))
                    elif len(reg) == 7:
                        prendas.append(Prenda(
                            id_prenda=reg[0],
                            tipo_prenda=reg[1],
                            modelo=reg[2],
                            talla=reg[3],
                            color=reg[4],
                            precio=reg[5],
                            stock=reg[6]
                        ))
                return prendas

    @classmethod
    def obtener_por_pedido(cls, id_pedido):
        sql = """
            SELECT id_prenda, id_pedido, tipo_prenda, modelo, talla, color, precio, stock
            FROM prendas
            WHERE id_pedido = %s
            ORDER BY id_prenda
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_pedido,))
                registros = cursor.fetchall()
                return [
                    Prenda(id_prenda=r[0], id_pedido=r[1], tipo_prenda=r[2], modelo=r[3], talla=r[4], color=r[5], precio=r[6], stock=r[7])
                    for r in registros
                ]

    @classmethod
    def insertar(cls, prenda):
        sql = """
            INSERT INTO prendas (id_pedido, tipo_prenda, modelo, talla, color, precio, stock)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (prenda.id_pedido, prenda.tipo_prenda, prenda.modelo, prenda.talla, prenda.color, prenda.precio, prenda.stock)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod
    def actualizar(cls, prenda):
        sql = """
            UPDATE prendas
            SET tipo_prenda = %s, modelo = %s, talla = %s, color = %s, precio = %s, stock= %s
            WHERE id_prenda = %s
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (prenda.tipo_prenda, prenda.modelo, prenda.talla, prenda.color, prenda.precio, prenda.stock, prenda.id_prenda)
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

def esta_en_pedidos(id_prenda):
    sql= "SELECT COUNT (*) FROM prendas WHERE id_prenda = %s AND id_pedido IS NOT NULL;"
    try:
        cursor = Conexion.obtener_conexion()
        cursor = Conexion.cursor()
        cursor.execute(sql,(id_prenda,))
        resultado = cursor.fetchone()
        cursor.close()
        Conexion.close()

        return resultado[0] > 0 if resultado else False
    except Exception as ex:
        print(f"Error al verificar prendas en pedidos: {ex}")
        return True
