class Cita:

    def __init__(
        self,
        id_cita=None,
        id_cliente=None,
        id_empleado=None,
        fecha=None,
        hora=None,
        motivo="",
    ):
        self.id_cita = id_cita
        self.id_cliente = id_cliente
        self.id_empleado = id_empleado
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
