from conexion import Conexion
from models.detalle_accesorio import DetalleAccesorio

class DetalleAccesorioDAO:

    @classmethod
    def seleccionar_detalle(cls):
        sql = """
        SELECT 
        d.id_detalle_accesorio, 
        d.id_pedido, 
        d.id_accesorio, 
        a.nombre AS nombre_accesorio,
        a.precio AS precio_unitario,
        d.cantidad 
        FROM detalle_accesorio d
        INNER JOIN accesorios a ON d.id_accesorio = a.id_accesorio
        ORDER BY d.id_detalle_accesorio
        """
        
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()
                
                detalles = []
                for reg in registros:
                    detalle = {
                        "id_detalle_accesorio": reg[0],
                        "id_pedido": reg[1],
                        "id_accesorio": reg[2],
                        "nombre_accesorio": reg[3],
                        "precio_unitario": reg[4],
                        "cantidad": reg[5],
                        "subtotal": reg[4] * reg[5]
                    }
                    detalles.append(detalle)
                return detalles
    @classmethod
    def obtener_por_pedido(cls, id_pedido):
        sql = """
            SELECT 
                d.id_detalle_accesorio,
                d.id_accesorio,
                a.nombre,
                a.precio,
                d.cantidad
            FROM detalle_accesorio d
            INNER JOIN accesorios a ON d.id_accesorio = a.id_accesorio
            WHERE d.id_pedido = %s
        """
        
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_pedido,))
                return cursor.fetchall()

    @classmethod
    def actualizar(cls, detalle):
        sql = "UPDATE detalle_accesorio SET id_pedido=%s, id_accesorio=%s, cantidad=%s WHERE id_detalle_accesorio=%s"
        
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (detalle.id_pedido, detalle.id_accesorio, detalle.cantidad, detalle.id_detalle_accesorio)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    @classmethod       
    def eliminar(cls, id_detalle_accesorio):
        sql = "DELETE FROM detalle_accesorio WHERE id_detalle_accesorio=%s"
        
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_detalle_accesorio,))
                conn.commit()
                return cursor.rowcount