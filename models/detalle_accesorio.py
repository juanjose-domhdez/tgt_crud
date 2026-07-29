class DetalleAccesorio:
    def __init__(self, id_detalle_accesorio=None, id_pedido=None, id_accesorio=None, cantidad=0):
        self.id_detalle_accesorio = id_detalle_accesorio
        self.id_pedido = id_pedido
        self.id_accesorio = id_accesorio
        self.cantidad = cantidad

    def __str__(self):
        return f"Detalle [ID: {self.id_detalle_accesorio}, Pedido: {self.id_pedido}, Accesorio: {self.id_accesorio}, Cantidad: {self.cantidad}]"