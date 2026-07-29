from conexion import Conexion 
from models.inventario_general import InventarioGeneral

class InventarioGeneralDAO:

    @classmethod
    def seleccionar(cls):
        sql = """
            SELECT i.id_inventario, i.id_accesorio, i.cantidad, i.stock_minimo, a.nombre
            FROM inventario_general i
            INNER JOIN accesorios a ON i.id_accesorio = a.id_accesorio
            ORDER BY i.id_inventario
        """
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()
                inventarios = []
                for reg in registros:
                    inv = InventarioGeneral(
                        id_inventario = reg [0],
                        id_accesorio = reg [1],
                        cantidad = reg [2],
                        stock_minimo = reg [3]
                    )
                    inventarios.append(inv)
                return inventarios

    def insertar (cls, inventario):
        sql = "INSERT INTO inventario_general (id_accesorio, cantidad, stock_minimo) VALUES (%s, %s, %s)"
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (inventario.id_accesorio, inventario.cantidad, inventario.stock_minimo)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    def actualizar(cls, inventario):
        sql = "UPDATE inventario_general SET id_accesorio = %s, cantidad = %s, stock_minimo = %s WHERE id_inventario = %"
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (inventario.id_accesorio, inventario.cantidad, inventario.stock_minimo, inventario.id_inventario)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    def eliminar(cls, id_inventario):
        sql = "DELETE FROM inventario_general WHERE id_inventario = %s"
        with Conexion.obtener_conexion() as conn:
            with conn.cursor () as cursor:
                cursor.execute(sql, (id_inventario,))
                conn.commit()
                return cursor.rowcount
