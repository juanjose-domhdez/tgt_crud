from conexion import Conexion

@staticmethod

def listar():
    conexion = Conexion.obtener_conexion()
    cursor = None
    try:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        sql = "SELECT id_accesorio, nombre, tipo, precio, stock FROM public.accesorios ORDER BY id_accesorio ASC;"
        
        cursor.execute(sql)
        filas = cursor.fetchall()
        return filas

    except Exception as ex:
        print(f"❌ Error en accesorio_dao.listar(): {ex}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def insertar(accesorio):

    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    sql = """
    INSERT INTO accesorios(nombre,tipo,precio,stock)
    VALUES(%s,%s,%s, %s)
        """

    cursor.execute(sql,(
        accesorio.nombre,
        accesorio.tipo,
        accesorio.precio,
        accesorio.stock
    ))

    conexion.commit()
    conexion.close()


def eliminar(id_accesorio):

    conexion=Conexion.obtener_conexion()
    cursor=conexion.cursor()
    sql= "DELETE FROM accesorios WHERE id_accesorio = %s"
    cursor.execute(sql, (id_accesorio,))
    conexion.commit()
    cursor.close()
    conexion.close()
    

def actualizar(accesorio):
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    sql = """
        UPDATE accesorios 
        SET nombre = %s, tipo = %s, precio = %s , stock = %s
        WHERE id_accesorio = %s
    """

    valores = (
        accesorio.nombre,
        accesorio.tipo,
        accesorio.precio,
        accesorio.stock,
        accesorio.id_accesorio
    )
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

def esta_en_pedidos(id_accesorio):
    sql= "SELECT COUNT (*) FROM detalle_accesorio WHERE id_accesorio = %s;"
    try:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql,(id_accesorio,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        return resultado[0] > 0 if resultado else False
    except Exception as ex:
        print(f"Error al verificar accesorios en pedidos: {ex}")
        return True
