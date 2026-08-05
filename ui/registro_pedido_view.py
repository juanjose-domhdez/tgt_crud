import flet as ft
from datetime import datetime


def RegistroPedidoView(page=None, on_regresar=None):

    restante = ft.Text(
        "Restante: $0.00",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.AMBER_400
    )

    txt_precio = ft.TextField(
        label="Precio Total",
        width=180
    )

    txt_anticipo = ft.TextField(
        label="Anticipo",
        width=180
    )

    cliente = ft.TextField(
        label="Cliente",
        width=300,
    )

    tipo_prenda = ft.Dropdown(
        label="Tipo de Prenda",
        width=220,

        options=[
            ft.dropdown.Option("Traje"),
            ft.dropdown.Option("Saco"),
            ft.dropdown.Option("Pantalón"),
            ft.dropdown.Option("Camisa"),
            ft.dropdown.Option("Chaleco"),
            ft.dropdown.Option("Moño"),
            ft.dropdown.Option("Pañuelo"),
        ]
    )

    fecha_entrega = ft.TextField(
        label="Fecha Entrega",
        width=200
    )


    def calcular(e):
        try:
            precio = float(txt_precio.value or 0)
            anticipo = float(txt_anticipo.value or 0)

            restante.value = f"Restante: ${precio - anticipo:,.2f}"

        except:
            restante.value = "Restante: $0.00"

        if page:
            page.update()


    txt_precio.on_change = calcular
    txt_anticipo.on_change = calcular


    def regresar(e):
        if on_regresar:
            on_regresar()

    def guardar_pedido(e):
        if(
            not cliente.value
            or not tipo_prenda.value
            or not fecha_entrega.value
            or not txt_precio.value
            or not txt_anticipo.value
        ):
            snack = ft.SnackBar(
                content=ft.Text("No se guardo correctamente. Complete los cambios obligatorios."),
                bgcolor=ft.Colors.RED_100
            )
        else:
            snack = ft.SnackBar(
                content=ft.Text("Se guardo correctamente."),
                bgcolor=ft.Colors.AMBER_200
            )

        page.overlay.append(snack)
        snack.open = True
        page.update()


    return ft.Container(

        expand=True,
        padding=30,

        content=ft.Column(

            scroll=ft.ScrollMode.AUTO,

            controls=[


                ft.Row(
                    [

                        ft.Text(
                            "REGISTRO DE PEDIDO",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.AMBER_400
                        )

                    ]
                ),


                ft.Divider(),


                ft.Text(
                    "Información del Cliente",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),


                ft.Row(
                    [

                        cliente,


                        ft.TextField(
                            label="Teléfono",
                            width=200
                        ),


                        ft.TextField(
                            label="Correo",
                            width=250
                        )

                    ]
                ),



                ft.Row(
                    [

                        ft.TextField(
                            label="Fecha Pedido",
                            value=datetime.now().strftime("%d/%m/%Y"),
                            width=200
                        ),


                        fecha_entrega

                    ]
                ),



                ft.Divider(),



                ft.Text(
                    "Información de la Prenda",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),



                ft.Row(
                    [

                        tipo_prenda,


                        ft.TextField(
                            label="Tela",
                            width=200
                        ),


                        ft.TextField(
                            label="Color",
                            width=160
                        ),


                        ft.TextField(
                            label="Cantidad",
                            width=150
                        )

                    ]
                ),



                ft.Divider(),



                ft.Text(
                    "Costos",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),



                ft.Row(
                    [

                        txt_precio,

                        txt_anticipo,

                        restante

                    ]
                ),



                ft.Divider(),



                ft.Dropdown(
                    label="Estado",
                    width=250,

                    value="Pendiente",

                    options=[
                        ft.dropdown.Option("Pendiente"),
                        ft.dropdown.Option("En proceso"),
                        ft.dropdown.Option("En confección"),
                        ft.dropdown.Option("Terminado"),
                        ft.dropdown.Option("Entregado")
                    ]
                ),



                ft.TextField(
                    label="Observaciones",
                    multiline=True,
                    min_lines=4,
                    max_lines=6
                ),



                ft.Row(
                    [

                        ft.ElevatedButton(
                            "Guardar Pedido",
                            bgcolor=ft.Colors.AMBER_500,
                            color=ft.Colors.BLACK,
                            on_click=guardar_pedido
                        ),


                        ft.ElevatedButton(
                            "Cancelar",
                            bgcolor=ft.Colors.RED,
                            color=ft.Colors.WHITE,
                            on_click=regresar
                        ),


                        ft.OutlinedButton(
                            "Regresar",
                            on_click=regresar
                        )

                    ],

                    alignment=ft.MainAxisAlignment.END
                )

            ]

        )

    