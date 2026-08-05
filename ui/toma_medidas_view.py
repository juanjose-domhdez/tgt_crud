import flet as ft

def TomaMedidasView(page=None, on_regresar=None):

    return ft.Column(
        [
            ft.Text(
                "TOMA DE MEDIDAS",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            ft.ElevatedButton(
                "Regresar",
                on_click=lambda _: on_regresar()
            )
        ]
    )