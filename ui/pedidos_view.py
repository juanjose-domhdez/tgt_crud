import flet as ft

def vista_nuevo_pedido(page: ft.Page):

    return ft.View(
        route="/nuevo_pedido",
        bgcolor="#0F172A",
        controls=[
            ft.AppBar(
                title=ft.Text(
                    "Nuevo Pedido de Traje",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                ),
                bgcolor="#1E293B",
                color="white",
            ),

            ft.Container(
                expand=True,
                padding=30,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "NUEVO PEDIDO DE TRAJE",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color="#F4C542",
                        ),

                        ft.Divider(),

                        ft.Text(
                            "Aquí irá el formulario del pedido.",
                            size=18,
                            color="white70",
                        ),

                        ft.Container(expand=True),

                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.ElevatedButton(
                                    "Regresar",
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=lambda e: page.go("/")
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )