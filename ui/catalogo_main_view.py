import flet as ft
from ui.catalogo_menu_view import CatalogoMenuView
from ui.catalogo_accesorios_view import CatalogoView
from ui.prenda_view import PrendaView

def CatalogoMainView(page=None):
    contenedor = ft.Container(expand=True)

    def navegar(opcion):
        if opcion == "accesorios":
            contenedor.content = CatalogoView(page=page, on_regresar=lambda: navegar("menu"))
        elif opcion == "prendas":
            contenedor.content = PrendaView(on_regresar=lambda: navegar("menu"))
        else: # "menu"
            contenedor.content = CatalogoMenuView(on_seleccionar_opcion=navegar)
        
        # Solo actualizamos la página si ya está montada en pantalla
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

    # Inicializa con el menú principal sin forzar el update antes de tiempo
    if opcion_inicial := "menu":
        if opcion_inicial == "accesorios":
            contenedor.content = CatalogoView(page=page, on_regresar=lambda: navegar("menu"))
        elif opcion_inicial == "prendas":
            contenedor.content = PrendaView(on_regresar=lambda: navegar("menu"))
        else:
            contenedor.content = CatalogoMenuView(on_seleccionar_opcion=navegar)

    return contenedor