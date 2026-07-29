class InventarioGeneral:
    def __init__(self, id_inventario = None, id_accesorio = None, cantidad = 0, stock_minimo = 0):
        self.id_inventario = id_inventario
        self.id_accesorio = id_accesorio
        self.cantidad = cantidad
        self.stock_minimo = stock_minimo

    def __str__(self):
        return f"Inventario [ID: {self.id_inventario}, Accesorio ID: {self.id_accesorio}, Cantidad: {self.cantidad}, Stock Min: {self.stock_minimo}]"