import flet as ft
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


# ============================================================
# DATOS DE EJEMPLO (MOCK)
# TODO (compañero de base de datos): reemplazar esta función
# por la consulta real, por ejemplo:
#     def obtener_pedidos():
#         return db.query("SELECT * FROM pedidos")
# Cada pedido debe llegar como un diccionario con estas claves.
# ============================================================
def obtener_pedidos_mock():
    return [
        {
            "id": 1,
            "cliente": "Juan Pérez",
            "prendas": "Traje x1, Moño x1",
            "fecha_entrega": "15/08/2026",
            "precio": 4500.00,
            "estado": "Pendiente"
        },
        {
            "id": 2,
            "cliente": "Carlos Ramírez",
            "prendas": "Pantalón x2",
            "fecha_entrega": "10/08/2026",
            "precio": 1800.00,
            "estado": "En proceso"
        },
        {
            "id": 3,
            "cliente": "Miguel Ángel Torres",
            "prendas": "Saco x1, Chaleco x1, Pañuelo x1",
            "fecha_entrega": "20/08/2026",
            "precio": 3200.00,
            "estado": "En confección"
        },
        {
            "id": 4,
            "cliente": "Roberto Gómez",
            "prendas": "Camisa x3",
            "fecha_entrega": "05/08/2026",
            "precio": 2100.00,
            "estado": "Terminado"
        },
        {
            "id": 5,
            "cliente": "Luis Hernández",
            "prendas": "Traje x1",
            "fecha_entrega": "01/08/2026",
            "precio": 5200.00,
            "estado": "Entregado"
        },
    ]


ESTADOS = ["Todos", "Pendiente", "En proceso", "En confección", "Terminado", "Entregado"]

COLOR_POR_ESTADO = {
    "Pendiente": ft.Colors.RED_300,
    "En proceso": ft.Colors.ORANGE_300,
    "En confección": ft.Colors.BLUE_300,
    "Terminado": ft.Colors.LIGHT_GREEN_300,
    "Entregado": COLOR_GOLD,
}


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


def tarjeta(contenido, expand=None):
    lado = ft.BorderSide(1, COLOR_BORDER)
    return ft.Container(
        bgcolor=COLOR_BG_CARD,
        border=ft.Border(top=lado, right=lado, bottom=lado, left=lado),
        border_radius=12,
        padding=20,
        content=contenido,
        expand=expand
    )


def PedidosMainView(page=None, on_regresar=None, on_ver_pedido=None):

    todos_los_pedidos = obtener_pedidos_mock()

    texto_busqueda = ft.TextField(
        hint_text="Buscar pedido por cliente...",
        hint_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY),
        color=COLOR_TEXT_PRIMARY,
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        border_radius=8,
        cursor_color=COLOR_GOLD,
        prefix_icon=ft.Icons.SEARCH,
        expand=True
    )

    estado_seleccionado = ft.Text("Todos")

    tabla_container = ft.Column(spacing=0)

    resumen_total = ft.Text(
        f"{len(todos_los_pedidos)} pedidos registrados",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=COLOR_TEXT_PRIMARY
    )

    resumen_pendientes = ft.Text(
        "",
        size=13,
        color=COLOR_TEXT_SECONDARY
    )


    def construir_fila(pedido):
        color_estado = COLOR_POR_ESTADO.get(pedido["estado"], COLOR_TEXT_SECONDARY)

        return ft.Container(
            padding=ft.Padding(top=12, right=10, bottom=12, left=10),
            border=ft.Border(bottom=ft.BorderSide(1, COLOR_BORDER)),
            content=ft.Row(
                [
                    ft.Container(ft.Text(str(pedido["id"]), color=COLOR_TEXT_PRIMARY), width=40),
                    ft.Container(ft.Text(pedido["cliente"], color=COLOR_TEXT_PRIMARY), expand=2),
                    ft.Container(ft.Text(pedido["prendas"], color=COLOR_TEXT_SECONDARY), expand=3),
                    ft.Container(ft.Text(pedido["fecha_entrega"], color=COLOR_TEXT_PRIMARY), expand=1),
                    ft.Container(ft.Text(f"${pedido['precio']:,.2f}", color=COLOR_TEXT_PRIMARY), expand=1),
                    ft.Container(
                        content=ft.Container(
                            content=ft.Text(pedido["estado"], size=12, color=COLOR_BG_DARK, weight=ft.FontWeight.BOLD),
                            bgcolor=color_estado,
                            border_radius=20,
                            padding=ft.Padding(top=4, right=10, bottom=4, left=10)
                        ),
                        expand=2
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.VISIBILITY_OUTLINED,
                                    icon_color=COLOR_GOLD,
                                    tooltip="Ver detalle",
                                    on_click=lambda e, p=pedido: on_ver_pedido(p) if on_ver_pedido else None
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_color=COLOR_TEXT_SECONDARY,
                                    tooltip="Editar"
                                ),
                            ],
                            spacing=0
                        ),
                        expand=1
                    ),
                ]
            )
        )


    def construir_encabezado():
        estilo = ft.TextStyle(weight=ft.FontWeight.BOLD, color=COLOR_GOLD, size=13)
        return ft.Container(
            padding=ft.Padding(top=10, right=10, bottom=10, left=10),
            border=ft.Border(bottom=ft.BorderSide(1, COLOR_BORDER)),
            content=ft.Row(
                [
                    ft.Container(ft.Text("ID", style=estilo), width=40),
                    ft.Container(ft.Text("Cliente", style=estilo), expand=2),
                    ft.Container(ft.Text("Prenda(s)", style=estilo), expand=3),
                    ft.Container(ft.Text("Entrega", style=estilo), expand=1),
                    ft.Container(ft.Text("Precio", style=estilo), expand=1),
                    ft.Container(ft.Text("Estado", style=estilo), expand=2),
                    ft.Container(ft.Text("Acciones", style=estilo), expand=1),
                ]
            )
        )


    def refrescar_tabla():
        filtro_texto = (texto_busqueda.value or "").strip().lower()
        filtro_estado = estado_seleccionado.value

        pedidos_filtrados = [
            p for p in todos_los_pedidos
            if (filtro_estado == "Todos" or p["estado"] == filtro_estado)
            and (filtro_texto in p["cliente"].lower())
        ]

        filas = [construir_encabezado()]

        if pedidos_filtrados:
            filas += [construir_fila(p) for p in pedidos_filtrados]
        else:
            filas.append(
                ft.Container(
                    padding=20,
                    content=ft.Text("No se encontraron pedidos.", color=COLOR_TEXT_SECONDARY)
                )
            )

        tabla_container.controls = filas

        pendientes = sum(1 for p in todos_los_pedidos if p["estado"] == "Pendiente")
        resumen_total.value = f"{len(todos_los_pedidos)} pedidos registrados"
        resumen_pendientes.value = f"{pendientes} pendientes de iniciar"

        if page:
            page.update()


    def buscar(e):
        refrescar_tabla()

    texto_busqueda.on_change = buscar


    botones_estado = {}

    def seleccionar_estado(estado):
        def handler(e):
            estado_seleccionado.value = estado
            for est, boton in botones_estado.items():
                if est == estado:
                    boton.bgcolor = COLOR_GOLD
                    boton.color = COLOR_BG_DARK
                else:
                    boton.bgcolor = COLOR_BG_CARD
                    boton.color = COLOR_TEXT_SECONDARY
            refrescar_tabla()
        return handler

    chips_estado = []
    for estado in ESTADOS:
        boton = ft.ElevatedButton(
            estado,
            bgcolor=COLOR_GOLD if estado == "Todos" else COLOR_BG_CARD,
            color=COLOR_BG_DARK if estado == "Todos" else COLOR_TEXT_SECONDARY,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                side=ft.BorderSide(1, COLOR_BORDER)
            )
        )
        boton.on_click = seleccionar_estado(estado)
        botones_estado[estado] = boton
        chips_estado.append(boton)


    def regresar(e):
        if on_regresar:
            on_regresar()


    vista = ft.Container(

        expand=True,
        padding=30,
        bgcolor=COLOR_BG_DARK,

        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[

                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=COLOR_GOLD,
                            on_click=regresar
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "VER PEDIDOS",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    font_family=FONT_HEADING,
                                    color=COLOR_GOLD
                                ),
                                ft.Text(
                                    "Estatus y entregas pendientes",
                                    size=13,
                                    color=COLOR_TEXT_SECONDARY
                                ),
                            ],
                            spacing=0
                        )
                    ]
                ),

                ft.Divider(color=COLOR_BORDER),

                ft.Row(
                    [

                        ft.Column(
                            [

                                tarjeta(
                                    ft.Column(
                                        [
                                            texto_busqueda,

                                            ft.Row(chips_estado, wrap=True),

                                            ft.Container(height=10),

                                            tabla_container,
                                        ]
                                    )
                                ),

                            ],
                            expand=3
                        ),

                        ft.Column(
                            [

                                tarjeta(
                                    ft.Column(
                                        [
                                            ft.Text(
                                                "Resumen",
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLOR_TEXT_PRIMARY
                                            ),
                                            ft.Container(height=10),
                                            resumen_total,
                                            resumen_pendientes,
                                        ]
                                    )
                                ),

                            ],
                            expand=1
                        ),

                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),

            ]
        )
    )

    refrescar_tabla()

    return vista