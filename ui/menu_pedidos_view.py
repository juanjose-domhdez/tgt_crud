import flet as ft
from ui.styles import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FOND_BRAND,
    FONT_BODY,
)


COLOR_AMBAR_MENU = ft.Colors.AMBER_400


def MenuPedidosView(on_seleccionar_opcion=None, on_crear_pedido=None, on_ver_pedidos=None, on_regresar=None, page=None, **kwargs):
    """
    on_seleccionar_opcion: callback opcional que recibe 'nuevo' o 'ver'
    (mismo patrón que CitasMedidasMenuView). Si prefieres, puedes usar
    on_crear_pedido / on_ver_pedidos por separado en su lugar.
    """

    def click_nuevo(e):
        if on_seleccionar_opcion:
            on_seleccionar_opcion("nuevo")
        elif on_crear_pedido:
            on_crear_pedido()

    def click_ver(e):
        if on_seleccionar_opcion:
            on_seleccionar_opcion("ver")
        elif on_ver_pedidos:
            on_ver_pedidos()

    def tarjeta_opcion(icono, titulo, descripcion, texto_boton, on_click):
        lado_borde = ft.BorderSide(1, COLOR_BORDER)
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icono, size=55, color=COLOR_AMBAR_MENU),
                    ft.Text(
                        titulo,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT_PRIMARY,
                        style=ft.TextStyle(font_family=FOND_BRAND),
                    ),
                    ft.Text(
                        descripcion,
                        color=COLOR_TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER,
                        size=13,
                        style=ft.TextStyle(font_family=FONT_BODY),
                    ),
                    ft.ElevatedButton(
                        texto_boton,
                        icon=ft.Icons.ARROW_FORWARD,
                        style=ft.ButtonStyle(bgcolor=COLOR_AMBAR_MENU, color="#000000"),
                        on_click=on_click,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            padding=25,
            width=320,
            height=280,
            bgcolor=COLOR_BG_CARD,
            border_radius=15,
            border=ft.Border(top=lado_borde, right=lado_borde, bottom=lado_borde, left=lado_borde),
        )

    return ft.Container(
        expand=True,
        bgcolor=COLOR_BG_DARK,
        content=ft.Column(
            [
                ft.Text(
                    "MENÚ DE PEDIDOS",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_AMBAR_MENU,
                    style=ft.TextStyle(font_family=FOND_BRAND),
                ),
                ft.Text(
                    "Selecciona una opción:",
                    color=COLOR_TEXT_SECONDARY,
                    style=ft.TextStyle(font_family=FONT_BODY),
                ),
                ft.Container(height=20),
                ft.Row(
                    [
                        tarjeta_opcion(
                            ft.Icons.ADD_SHOPPING_CART,
                            "NUEVO PEDIDO",
                            "Registrar un nuevo pedido",
                            "Crear Pedido",
                            click_nuevo,
                        ),
                        tarjeta_opcion(
                            ft.Icons.ASSIGNMENT_OUTLINED,
                            "VER PEDIDOS",
                            "Estatus y entregas pendientes",
                            "Abrir Pedidos",
                            click_ver,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=40,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )