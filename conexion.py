import psycopg2

class Conexion:
    @staticmethod
    def obtener_conexion():
        try:
            conexion = psycopg2.connect(
                host="localhost",
                database="the_glentemans_tailor",
                user="postgres",
                password="leca3020", 
                port="5432"
            )
            return conexion
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None