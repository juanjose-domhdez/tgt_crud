class Cliente:

    def __init__(
        self,
        id_cliente=None,
        nombre_completo="",
        telefono="",
        fecha_registro=None,
    ):
        self.id_cliente = id_cliente
        self.nombre_completo = nombre_completo
        self.telefono = telefono
        self.fecha_registro = fecha_registro