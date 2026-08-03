import flet as ft

def CatalogoMenuView(on_seleccionar_opcion):
    """
    on_seleccionar_opcion: función callback que recibe 'accesorios' o 'prendas'
    """
    card_accesorios = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.WATCH_OUTLINED, size=55, color=ft.Colors.AMBER_400),
                ft.Text("ACCESORIOS", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(
                    "Gestión e inventario de accesorios",
                    color=ft.Colors.WHITE_54,
                    text_align=ft.TextAlign.CENTER,
                    size=13
                ),
                ft.ElevatedButton(
                    "Abrir Accesorios",
                    icon=ft.Icons.ARROW_FORWARD,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_500, color=ft.Colors.BLACK),
                    on_click=lambda _: on_seleccionar_opcion("accesorios")
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=25,
        width=320,
        height=280,
        bgcolor="#1E293B",
        border_radius=15,
        border=ft.Border.all(1, ft.Colors.BLUE_GREY_800)
    )

    card_prendas = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.CHECKROOM_OUTLINED, size=55, color=ft.Colors.AMBER_400),
                ft.Text("PRENDAS", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(
                    "Gestión e inventario de prendas",
                    color=ft.Colors.WHITE_54,
                    text_align=ft.TextAlign.CENTER,
                    size=13
                ),
                ft.ElevatedButton(
                    "Abrir Prendas",
                    icon=ft.Icons.ARROW_FORWARD,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_500, color=ft.Colors.BLACK),
                    on_click=lambda _: on_seleccionar_opcion("prendas")
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=25,
        width=320,
        height=280,
        bgcolor="#1E293B",
        border_radius=15,
        border=ft.Border.all(1, ft.Colors.BLUE_GREY_800)
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("MENÚ DE CATÁLOGOS E INVENTARIO", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400),
                ft.Text("Selecciona la categoría a la que deseas entrar:", color=ft.Colors.WHITE_70),
                ft.Container(height=20),
                ft.Row(
                    [card_accesorios, card_prendas],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=40
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        expand=True,
    )