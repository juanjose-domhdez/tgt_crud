class Prenda:

    def __init__(
        self,
        id_prenda=None,
        id_pedido=None,
        tipo_prenda="",
        modelo="",
        talla="",
        color="",
        precio=0.0,
    ):
        self.id_prenda = id_prenda
        self.id_pedido = id_pedido
        self.tipo_prenda = tipo_prenda
        self.modelo = modelo
        self.talla = talla
        self.color = color
        self.precio = precio
