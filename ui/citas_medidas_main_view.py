import flet as ft
from ui.citas_medidas_menu_view import CitasMedidasMenuView
from ui.cita_view import CitaView
from ui.medida_view import MedidaView

def CitasMedidasMainView(page=None):
    contenedor = ft.Container(expand=True)

    def navegar(opcion):
        if opcion == "citas":
            contenedor.content = CitaView(page=page, on_regresar=lambda: navegar("menu"))
        elif opcion == "medidas":
            contenedor.content = MedidaView(page=page, on_regresar=lambda: navegar("menu"))
        else:  # "menu"
            contenedor.content = CitasMedidasMenuView(on_seleccionar_opcion=navegar)

        if page:
            try:
                page.update()
            except Exception:
                pass
        elif contenedor.page:
            try:
                contenedor.page.update()
            except Exception:
                pass

    contenedor.content = CitasMedidasMenuView(on_seleccionar_opcion=navegar)

    return contenedor
