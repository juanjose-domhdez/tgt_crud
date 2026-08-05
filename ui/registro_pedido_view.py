import flet as ft
from datetime import datetime
from ui.styles import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_BORDER,
    COLOR_GOLD,
    COLOR_GOLD_HOVER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FONT_HEADING,
    FONT_BODY,
)


def campo_texto(label, **kwargs):
    return ft.TextField(
        label=label,
        color=COLOR_TEXT_PRIMARY,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY),
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        border_radius=8,
        cursor_color=COLOR_GOLD,
        **kwargs
    )


def campo_dropdown(label, options, **kwargs):
    return ft.Dropdown(
        label=label,
        color=COLOR_TEXT_PRIMARY,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY),
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        border_radius=8,
        options=options,
        **kwargs
    )


def tarjeta(contenido):
    lado = ft.BorderSide(1, COLOR_BORDER)
    return ft.Container(
        bgcolor=COLOR_BG_CARD,
        border=ft.Border(top=lado, right=lado, bottom=lado, left=lado),
        border_radius=12,
        padding=20,
        content=contenido
    )


def RegistroPedidoView(page=None, on_regresar=None):

    restante = ft.Text(
        "Restante: $0.00",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=COLOR_GOLD
    )

    txt_precio = campo_texto("Precio Total", width=180)

    txt_anticipo = campo_texto("Anticipo", width=180)

    cliente = campo_texto("Cliente", width=300)

    telefono = campo_texto(
        "Teléfono",
        width=200,
        max_length=10,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    opciones_prenda = [
        "Traje",
        "Saco",
        "Pantalón",
        "Camisa",
        "Chaleco",
        "Moño",
        "Pañuelo",
    ]

    filas_tipo_prenda = []

    for opcion in opciones_prenda:
        chk = ft.Checkbox(
            label=opcion,
            value=False,
            label_style=ft.TextStyle(color=COLOR_TEXT_PRIMARY),
            check_color=COLOR_BG_DARK,
            fill_color=COLOR_GOLD
        )
        cant = campo_texto(
            None,
            value="0",
            width=60,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        filas_tipo_prenda.append({
            "nombre": opcion,
            "checkbox": chk,
            "cantidad": cant
        })

    def obtener_prendas_seleccionadas():
        seleccionadas = []
        for fila in filas_tipo_prenda:
            if fila["checkbox"].value:
                try:
                    cantidad = int(fila["cantidad"].value or 0)
                except ValueError:
                    cantidad = 0
                if cantidad > 0:
                    seleccionadas.append((fila["nombre"], cantidad))
        return seleccionadas

    fecha_entrega = campo_texto("Fecha Entrega", width=200)


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


    def validar_telefono(e):
        valor = telefono.value or ""
        solo_digitos = "".join(ch for ch in valor if ch.isdigit())[:10]

        if solo_digitos != valor:
            telefono.value = solo_digitos
            if page:
                page.update()


    telefono.on_change = validar_telefono


    def regresar(e):
        if on_regresar:
            on_regresar()

    def guardar_pedido(e):
        prendas_seleccionadas = obtener_prendas_seleccionadas()

        if(
            not cliente.value
            or not prendas_seleccionadas
            or not fecha_entrega.value
            or not txt_precio.value
            or not txt_anticipo.value
        ):
            snack = ft.SnackBar(
                content=ft.Text("No se guardo correctamente. Complete los cambios obligatorios."),
                bgcolor=ft.Colors.RED_100
            )
        elif telefono.value and len(telefono.value) != 10:
            snack = ft.SnackBar(
                content=ft.Text("El teléfono debe tener 10 dígitos."),
                bgcolor=ft.Colors.RED_100
            )
        else:
            snack = ft.SnackBar(
                content=ft.Text("Se guardo correctamente."),
                bgcolor=COLOR_GOLD
            )

        page.overlay.append(snack)
        snack.open = True
        page.update()


    return ft.Container(

        expand=True,
        padding=30,
        bgcolor=COLOR_BG_DARK,

        content=ft.Column(

            scroll=ft.ScrollMode.AUTO,

            controls=[


                ft.Row(
                    [

                        ft.Text(
                            "REGISTRO DE PEDIDO",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            font_family=FONT_HEADING,
                            color=COLOR_GOLD
                        )

                    ]
                ),


                ft.Divider(color=COLOR_BORDER),


                tarjeta(
                    ft.Column(
                        [

                            ft.Text(
                                "Información del Cliente",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_TEXT_PRIMARY
                            ),


                            ft.Row(
                                [

                                    cliente,


                                    telefono,


                                    campo_texto("Correo", width=250)

                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),



                            ft.Row(
                                [

                                    campo_texto(
                                        "Fecha Pedido",
                                        value=datetime.now().strftime("%d/%m/%Y"),
                                        width=200
                                    ),


                                    fecha_entrega

                                ]
                            ),

                        ]
                    )
                ),


                ft.Container(height=15),


                tarjeta(
                    ft.Column(
                        [

                            ft.Text(
                                "Información de la Prenda",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_TEXT_PRIMARY
                            ),



                            ft.Text(
                                "Tipo de Prenda y cantidad",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=COLOR_TEXT_SECONDARY
                            ),

                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            fila["checkbox"],
                                            fila["cantidad"]
                                        ]
                                    )
                                    for fila in filas_tipo_prenda
                                ]
                            ),

                        ]
                    )
                ),


                ft.Container(height=15),


                tarjeta(
                    ft.Column(
                        [

                            ft.Text(
                                "Costos",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_TEXT_PRIMARY
                            ),



                            ft.Row(
                                [

                                    txt_precio,

                                    txt_anticipo,

                                    restante

                                ]
                            ),



                            ft.Divider(color=COLOR_BORDER),



                            campo_dropdown(
                                "Estado",
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



                            campo_texto(
                                "Observaciones",
                                multiline=True,
                                min_lines=4,
                                max_lines=6
                            ),

                        ]
                    )
                ),
        

                ft.Container(height=10),


                ft.Row(
                    [

                        ft.ElevatedButton(
                            "Guardar Pedido",
                            icon=ft.Icons.SAVE,
                            bgcolor=COLOR_GOLD,
                            color=COLOR_BG_DARK,
                            style=ft.ButtonStyle(
                                overlay_color=COLOR_GOLD_HOVER
                            ),
                            on_click=guardar_pedido
                        ),


                        ft.OutlinedButton(
                            "Cancelar",
                            style=ft.ButtonStyle(
                                color=COLOR_TEXT_PRIMARY,
                                side=ft.BorderSide(1, COLOR_BORDER)
                            ),
                            on_click=regresar
                        ),


                        ft.OutlinedButton(
                            "Regresar",
                            style=ft.ButtonStyle(
                                color=COLOR_TEXT_PRIMARY,
                                side=ft.BorderSide(1, COLOR_BORDER)
                            ),
                            on_click=regresar
                        )

                    ],

                    alignment=ft.MainAxisAlignment.END
                )

            ]

        )

    )