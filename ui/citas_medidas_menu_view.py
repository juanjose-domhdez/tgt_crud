import flet as ft

def CitasMedidasMenuView(on_seleccionar_opcion):
    """
    on_seleccionar_opcion: función callback que recibe 'citas' o 'medidas'
    """
    card_citas = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.CALENDAR_MONTH_OUTLINED, size=55, color=ft.Colors.AMBER_400),
                ft.Text("CITAS", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(
                    "Agenda de citas para prueba, toma de medidas y entregas",
                    color=ft.Colors.WHITE_54,
                    text_align=ft.TextAlign.CENTER,
                    size=13
                ),
                ft.ElevatedButton(
                    "Abrir Citas",
                    icon=ft.Icons.ARROW_FORWARD,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_500, color=ft.Colors.BLACK),
                    on_click=lambda _: on_seleccionar_opcion("citas")
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

    card_medidas = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.STRAIGHTEN_OUTLINED, size=55, color=ft.Colors.AMBER_400),
                ft.Text("MEDIDAS", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(
                    "Fichas técnicas de confección por pedido",
                    color=ft.Colors.WHITE_54,
                    text_align=ft.TextAlign.CENTER,
                    size=13
                ),
                ft.ElevatedButton(
                    "Abrir Medidas",
                    icon=ft.Icons.ARROW_FORWARD,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_500, color=ft.Colors.BLACK),
                    on_click=lambda _: on_seleccionar_opcion("medidas")
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
                ft.Text("MENÚ DE CITAS Y MEDIDAS", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400),
                ft.Text("Selecciona la sección a la que deseas entrar:", color=ft.Colors.WHITE_70),
                ft.Container(height=20),
                ft.Row(
                    [card_citas, card_medidas],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=40
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        expand=True,
    )
