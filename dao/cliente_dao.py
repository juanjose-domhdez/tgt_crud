# dao/cliente_dao.py
from datetime import date

class Cliente:
    """Clase Modelo para representar la entidad Cliente."""
    def __init__(self, id_cliente=None, nombre_completo="", telefono="", fecha_registro=None, activo=True):
        self.id_cliente = id_cliente
        self.nombre_completo = nombre_completo
        self.telefono = telefono
        self.fecha_registro = fecha_registro or date.today().isoformat()
        self.activo = activo


class ClienteDAO:
    """Objeto de Acceso a Datos (DAO) para gestionar la tabla 'clientes' en PostgreSQL."""
    def __init__(self, connection):
        self.conn = connection

    def insertar_cliente(self, cliente_o_nombre, telefono=None, fecha_registro=None):
        """
        Inserta un nuevo cliente en la base de datos PostgreSQL incluyendo la fecha de registro.
        """
        if not self.conn:
            return False

        if isinstance(cliente_o_nombre, Cliente) or hasattr(cliente_o_nombre, 'nombre_completo'):
            nom = getattr(cliente_o_nombre, 'nombre_completo', '')
            tel = getattr(cliente_o_nombre, 'telefono', '')
            f_reg = getattr(cliente_o_nombre, 'fecha_registro', None) or date.today().isoformat()
        else:
            nom = cliente_o_nombre
            tel = telefono
            f_reg = fecha_registro or date.today().isoformat()

        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO clientes (nombre_completo, telefono, fecha_registro) 
                VALUES (%s, %s, %s)
                RETURNING id_cliente;
            """
            cursor.execute(query, (nom, tel, f_reg))
            nuevo_id = cursor.fetchone()[0]
            self.conn.commit()
            cursor.close()

            if isinstance(cliente_o_nombre, Cliente):
                cliente_o_nombre.id_cliente = nuevo_id

            return nuevo_id
        except Exception as ex:
            self.conn.rollback()
            print(f"Error al insertar cliente en BD: {ex}")
            return None

    # Alias de compatibilidad
    crear_cliente = insertar_cliente
    agregar_cliente = insertar_cliente

    def obtener_todos(self):
        """Obtiene la lista de clientes de la base de datos."""
        clientes = []
        if not self.conn:
            return clientes

        try:
            cursor = self.conn.cursor()
            query = """
                SELECT id_cliente, nombre_completo, telefono, fecha_registro 
                FROM clientes 
                ORDER BY id_cliente DESC;
            """
            cursor.execute(query)
            filas = cursor.fetchall()
            
            for f in filas:
                clientes.append(Cliente(
                    id_cliente=f[0],
                    nombre_completo=f[1],
                    telefono=f[2],
                    fecha_registro=str(f[3]) if f[3] else date.today().isoformat()
                ))
            cursor.close()
        except Exception as ex:
            print(f"Error al obtener clientes: {ex}")

        return clientes

    def buscar_por_filtro(self, texto_busqueda):
        """Busca clientes por coincidencia de nombre o teléfono."""
        clientes = []
        if not self.conn:
            return clientes

        try:
            cursor = self.conn.cursor()
            query = """
                SELECT id_cliente, nombre_completo, telefono, fecha_registro 
                FROM clientes 
                WHERE nombre_completo ILIKE %s OR telefono LIKE %s
                ORDER BY id_cliente DESC;
            """
            patron = f"%{texto_busqueda}%"
            cursor.execute(query, (patron, patron))
            filas = cursor.fetchall()

            for f in filas:
                clientes.append(Cliente(
                    id_cliente=f[0],
                    nombre_completo=f[1],
                    telefono=f[2],
                    fecha_registro=str(f[3]) if f[3] else date.today().isoformat()
                ))
            cursor.close()
        except Exception as ex:
            print(f"Error al buscar clientes: {ex}")

        return clientes

    def actualizar_cliente(self, cliente_o_id, nombre=None, telefono=None):
        """Actualiza un cliente en la base de datos."""
        if not self.conn:
            return False

        if isinstance(cliente_o_id, Cliente) or hasattr(cliente_o_id, 'id_cliente'):
            id_c = getattr(cliente_o_id, 'id_cliente', getattr(cliente_o_id, 'id', None))
            nom = getattr(cliente_o_id, 'nombre_completo', nombre)
            tel = getattr(cliente_o_id, 'telefono', telefono)
        else:
            id_c = cliente_o_id
            nom = nombre
            tel = telefono

        try:
            cursor = self.conn.cursor()
            query = """
                UPDATE clientes 
                SET nombre_completo = %s, telefono = %s 
                WHERE id_cliente = %s;
            """
            cursor.execute(query, (nom, tel, id_c))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            self.conn.rollback()
            print(f"Error al actualizar cliente en BD: {ex}")
            return False

    def eliminar_cliente(self, cliente_o_id):
        """Elimina un cliente por su ID de la base de datos."""
        if not self.conn:
            return False

        if isinstance(cliente_o_id, Cliente) or hasattr(cliente_o_id, 'id_cliente'):
            id_c = getattr(cliente_o_id, 'id_cliente', getattr(cliente_o_id, 'id', None))
        else:
            id_c = cliente_o_id

        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM clientes WHERE id_cliente = %s;"
            cursor.execute(query, (id_c,))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            self.conn.rollback()
            print(f"Error al eliminar cliente en BD: {ex}")
            return False