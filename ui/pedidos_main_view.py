import flet as ft

from ui.menu_pedidos_view import MenuPedidosView
from ui.registro_pedido_view import RegistroPedidoView
from ui.toma_medidas_view import TomaMedidasView


def PedidosMainView(page=None):

    contenedor = ft.Container(expand=True)

    def navegar(opcion):

        if opcion == "pedido":
            contenedor.content = RegistroPedidoView(
                page=page,
                on_regresar=lambda: navegar("menu")
            )

        elif opcion == "medidas":
            contenedor.content = TomaMedidasView(
                page=page,
                on_regresar=lambda: navegar("menu")
            )

        else:
            contenedor.content = MenuPedidosView(
                on_seleccionar_opcion=navegar
            )

        if page:
            page.update()

    contenedor.content = MenuPedidosView(
        on_seleccionar_opcion=navegar
    )

    return contenedor