class Pedido:

    def __init__(
        self,
        id_pedido=None,
        id_cliente=None,
        id_empleado=None,
        fecha_pedido=None,
        fecha_entrega=None,
        anticipo=0.0,
        total=0.0,
        estado="",
    ):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.id_empleado = id_empleado
        self.fecha_pedido = fecha_pedido
        self.fecha_entrega = fecha_entrega
        self.anticipo = anticipo
        self.total = total
        self.estado = estado
        