from conexion import Conexion
from models.detalle_accesorio import DetalleAccesorio

class DetalleAccesorioDAO:

    @classmethod
    def seleccionar_detalle(cls):
        sql = "SELECT id_detalle_accesorio, id_pedido, id_accesorio, cantidad FROM detalle_accesorio ORDER BY id_detalle_accesorio"
        
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()
                
                detalles = []
                for reg in registros:
                    detalle = DetalleAccesorio(
                        id_detalle_accesorio=reg[0],
                        id_pedido=reg[1],
                        id_accesorio=reg[2],
                        cantidad=reg[3]
                    )
                    detalles.append(detalle)
                return detalles

    def insertar_detalle(cls, detalle):
        sql = "INSERT INTO detalle_accesorio (id_pedido, id_accesorio, cantidad) VALUES (%s, %s, %s)"
        
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (detalle.id_pedido, detalle.id_accesorio, detalle.cantidad)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount

    def actualizar_detalle(cls, detalle):
        sql = "UPDATE detalle_accesorio SET id_pedido=%s, id_accesorio=%s, cantidad=%s WHERE id_detalle_accesorio=%s"
        
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                valores = (detalle.id_pedido, detalle.id_accesorio, detalle.cantidad, detalle.id_detalle_accesorio)
                cursor.execute(sql, valores)
                conn.commit()
                return cursor.rowcount
            
    def eliminar(cls, id_detalle_accesorio):
        sql = "DELETE FROM detalle_accesorio WHERE id_detalle_accesorio=%s"
        
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_detalle_accesorio,))
                conn.commit()
                return cursor.rowcount