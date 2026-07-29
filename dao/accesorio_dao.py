from conexion import Conexion
@staticmethod

def listar():

    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM accesorios")
    datos = cursor.fetchall()
    conexion.close()

    return datos


def insertar(accesorio):

    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    sql = """
    INSERT INTO accesorios(nombre,tipo,precio)
    VALUES(%s,%s,%s)
        """

    cursor.execute(sql,(
        accesorio.nombre,
        accesorio.tipo,
        accesorio.precio
    ))

    conexion.commit()
    conexion.close()


def eliminar(id):

    conexion=Conexion.obtener_conexion()
    cursor=conexion.cursor()
    cursor.execute(
        "DELETE FROM accesorios WHERE id_accesorio=%s",
        (id,)
    )

    conexion.commit()
    conexion.close()

def actualizar(accesorio):
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()
    sql = """
        UPDATE accesorios 
        SET nombre = %s, tipo = %s, precio = %s 
        WHERE id_accesorio = %s
    """
    cursor.execute(sql, (
        accesorio.nombre, 
        accesorio.tipo, 
        accesorio.precio, 
        accesorio.id_accesorio
    ))
    conexion.commit()
    conexion.close()