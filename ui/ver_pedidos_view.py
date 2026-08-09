import flet as ft
from datetime import datetime

from ui.styles import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_BORDER,
    COLOR_GOLD,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FOND_BRAND,
    FONT_BODY,
)


try:
    from dao.pedido_dao import PedidoDAO
except Exception:
    import dao.pedido_dao as PedidoDAO

try:
    from dao.clientes_dao import ClienteDAO
except Exception:
    import dao.clientes_dao as ClienteDAO


def VerPedidosView(on_nuevo_pedido=None, on_regresar=None, page=None, **kwargs):
    COLOR_DANGER = "#EF4444"
    COLOR_SUCCESS = "#22C55E"
    COLOR_WARNING = "#F59E0B"
    COLOR_INFO = "#3B82F6"

    columna_pedidos = ft.Column(spacing=10)

    def obtener_color_estado(estado):
        est = str(estado or "").lower()
        if any(w in est for w in ["entregado", "terminado", "completado"]):
            return COLOR_SUCCESS
        elif any(w in est for w in ["proceso", "confeccion", "confección", "diseño"]):
            return COLOR_INFO
        else:
            return COLOR_WARNING

    input_busqueda = ft.TextField(
        hint_text="Buscar por cliente o ID de pedido...",
        hint_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        expand=True,
        height=45,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )

    input_filtro_estado = ft.Dropdown(
        value="Todos",
        options=[
            ft.dropdown.Option("Todos", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
            ft.dropdown.Option("Pendiente", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
            ft.dropdown.Option("En Proceso", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
            ft.dropdown.Option("En Confección", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
            ft.dropdown.Option("Terminado", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
            ft.dropdown.Option("Entregado", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
        ],
        width=180,
        height=45,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )

    def obtener_valor(obj, clave, defecto=None):
        if isinstance(obj, dict):
            return obj.get(clave, defecto)
        elif isinstance(obj, (tuple, list)):
            mapeo_indices = {
                "id_pedido": 0, "id": 0,
                "id_cliente": 1, "nombre_cliente": 1,
                "fecha_pedido": 2,
                "fecha_entrega": 3,
                "total": 4,
                "anticipo": 5,
                "estado": 6
            }
            idx = mapeo_indices.get(clave)
            if idx is not None and idx < len(obj):
                return obj[idx]
            return defecto
        else:
            return getattr(obj, clave, defecto)

    def cargar_pedidos(e=None):
        columna_pedidos.controls.clear()
        texto_busqueda = (input_busqueda.value or "").strip().lower()
        estado_filtro = input_filtro_estado.value or "Todos"

        mapa_clientes = {}
        try:
            clientes_db = ClienteDAO.seleccionar() if hasattr(ClienteDAO, "seleccionar") else (ClienteDAO.obtener_todos() if hasattr(ClienteDAO, "obtener_todos") else [])
            for c in clientes_db:
                id_c = obtener_valor(c, "id_cliente", obtener_valor(c, "id"))
                nom_c = obtener_valor(c, "nombre_completo", obtener_valor(c, "nombre", f"Cliente #{id_c}"))
                if id_c:
                    mapa_clientes[id_c] = nom_c
        except Exception as ex:
            print(f"Error cargando clientes: {ex}")

        pedidos_db = []
        try:
            pedidos_db = PedidoDAO.seleccionar()
        except Exception as ex:
            print(f"Error cargando pedidos desde PedidoDAO: {ex}")

        if not pedidos_db:
            columna_pedidos.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay pedidos registrados en la base de datos.",
                        color=COLOR_TEXT_SECONDARY,
                        style=ft.TextStyle(font_family=FONT_BODY),
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=20,
                    alignment=ft.alignment.center,
                )
            )
        else:
            for ped in pedidos_db:
                id_p = obtener_valor(ped, "id_pedido", obtener_valor(ped, "id", "N/A"))
                id_c = obtener_valor(ped, "id_cliente", None)

                nombre_cliente = obtener_valor(ped, "nombre_cliente", None)
                if not nombre_cliente:
                    nombre_cliente = mapa_clientes.get(id_c, f"Cliente #{id_c}" if id_c else "Cliente General")

                f_pedido = obtener_valor(ped, "fecha_pedido", "")
                if isinstance(f_pedido, datetime):
                    f_pedido_str = f_pedido.strftime("%d/%m/%Y")
                else:
                    f_pedido_str = str(f_pedido) if f_pedido else "N/A"

                f_entrega = obtener_valor(ped, "fecha_entrega", "")
                if isinstance(f_entrega, datetime):
                    f_entrega_str = f_entrega.strftime("%d/%m/%Y")
                else:
                    f_entrega_str = str(f_entrega) if f_entrega else "N/A"

                total = float(obtener_valor(ped, "total", 0.0) or 0.0)
                anticipo = float(obtener_valor(ped, "anticipo", 0.0) or 0.0)
                restante = total - anticipo
                estado = str(obtener_valor(ped, "estado", "Pendiente"))

                if estado_filtro != "Todos" and estado.lower() != estado_filtro.lower():
                    continue

                if texto_busqueda:
                    coincide_id = texto_busqueda in str(id_p).lower()
                    coincide_cliente = texto_busqueda in str(nombre_cliente).lower()
                    if not (coincide_id or coincide_cliente):
                        continue

                tarjeta = ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        f"Pedido #{id_p}",
                                        weight=ft.FontWeight.BOLD,
                                        color=COLOR_GOLD,
                                        size=15,
                                        style=ft.TextStyle(font_family=FOND_BRAND),
                                    ),
                                    ft.Text(
                                        f"👤 {nombre_cliente}",
                                        color=COLOR_TEXT_PRIMARY,
                                        size=13,
                                        style=ft.TextStyle(font_family=FONT_BODY),
                                    ),
                                ],
                                expand=3,
                                spacing=4,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        f"📅 Pedido: {f_pedido_str}",
                                        color=COLOR_TEXT_SECONDARY,
                                        size=12,
                                        style=ft.TextStyle(font_family=FONT_BODY),
                                    ),
                                    ft.Text(
                                        f"🚚 Entrega: {f_entrega_str}",
                                        color=COLOR_TEXT_PRIMARY,
                                        size=12,
                                        weight=ft.FontWeight.W_500,
                                        style=ft.TextStyle(font_family=FONT_BODY),
                                    ),
                                ],
                                expand=3,
                                spacing=4,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        f"Total: ${total:,.2f}",
                                        color=COLOR_TEXT_PRIMARY,
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                        style=ft.TextStyle(font_family=FONT_BODY),
                                    ),
                                    ft.Text(
                                        f"Restante: ${restante:,.2f}",
                                        color=COLOR_DANGER if restante > 0 else COLOR_SUCCESS,
                                        size=12,
                                        style=ft.TextStyle(font_family=FONT_BODY),
                                    ),
                                ],
                                expand=2,
                                spacing=4,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    estado,
                                    color="#000000",
                                    weight=ft.FontWeight.BOLD,
                                    size=11,
                                    style=ft.TextStyle(font_family=FONT_BODY),
                                ),
                                bgcolor=obtener_color_estado(estado),
                                padding=ft.Padding.symmetric(horizontal=10, vertical=5),
                                border_radius=12,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=15,
                    bgcolor=COLOR_BG_CARD,
                    border=ft.Border.all(1, COLOR_BORDER),
                    border_radius=10,
                )
                columna_pedidos.controls.append(tarjeta)

        try:
            columna_pedidos.update()
        except Exception:
            pass

    input_busqueda.on_change = cargar_pedidos
    input_filtro_estado.on_change = cargar_pedidos

    cargar_pedidos()

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLOR_GOLD,
                                    on_click=lambda _: on_regresar() if on_regresar else None,
                                    tooltip="Volver al Inicio",
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            "HISTORIAL DE PEDIDOS",
                                            size=22,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLOR_GOLD,
                                            style=ft.TextStyle(font_family=FOND_BRAND),
                                        ),
                                        ft.Text(
                                            "Consulta y gestiona todos los pedidos registrados",
                                            size=12,
                                            color=COLOR_TEXT_SECONDARY,
                                            style=ft.TextStyle(font_family=FONT_BODY),
                                        ),
                                    ],
                                    spacing=2,
                                ),
                            ]
                        ),
                        ft.ElevatedButton(
                            "+ Nuevo Pedido",
                            style=ft.ButtonStyle(bgcolor=COLOR_GOLD, color="#000000"),
                            on_click=lambda _: on_nuevo_pedido() if on_nuevo_pedido else None,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=10),
                ft.Row(
                    [
                        input_busqueda,
                        input_filtro_estado,
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            icon_color=COLOR_GOLD,
                            on_click=cargar_pedidos,
                            tooltip="Actualizar lista desde BD",
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(color=COLOR_BORDER),
                ft.Container(
                    content=ft.ListView(
                        controls=[columna_pedidos],
                        spacing=10,
                    ),
                    expand=True,
                ),
            ],
            spacing=10,
        ),
        padding=20,
        expand=True,
        bgcolor=COLOR_BG_DARK,
    )