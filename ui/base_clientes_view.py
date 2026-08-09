# ui/base_clientes_view.py
import flet as ft
from dao.cliente_dao import ClienteDAO
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

def BaseClientesView(page: ft.Page, on_regresar, db_connection=None, on_crear_pedido=None):
    cliente_dao = ClienteDAO(db_connection) if db_connection else None

    # Contenedor dinámico de la tabla
    contenedor_tabla = ft.Column(scroll=ft.ScrollMode.AUTO)

    def obtener_id_cliente(c):
        return getattr(c, 'id_cliente', getattr(c, 'id', None))

    # -------------------------------------------------------------
    # EVENTOS Y VENTANAS MODALES (ELIMINAR Y EDITAR)
    # -------------------------------------------------------------

    def abrir_dialogo_eliminar(cliente):
        id_cliente = obtener_id_cliente(cliente)

        def cerrar_dialogo(e=None):
            page.pop_dialog()

        def confirmar_eliminar(e):
            if cliente_dao and id_cliente is not None:
                exito = cliente_dao.eliminar_cliente(cliente)
                if exito:
                    refrescar_tabla()
            cerrar_dialogo()

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor="#F5F3ED",
            shape=ft.RoundedRectangleBorder(radius=16),
            title=ft.Text(
                "Confirmar Inhabilitación", 
                color="#C88E38", 
                font_family=FOND_BRAND, 
                weight=ft.FontWeight.BOLD,
                size=20
            ),
            content=ft.Container(
                content=ft.Text(
                    f"¿Deseas inhabilitar/eliminar a '{getattr(cliente, 'nombre_completo', '')}'? Dejará de mostrarse en la lista activa de clientes.",
                    color="#333333",
                    font_family=FONT_BODY,
                    size=14
                ),
                padding=10
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo, style=ft.ButtonStyle(color="#4A607A")),
                ft.ElevatedButton(
                    "Inhabilitar", 
                    on_click=confirmar_eliminar,
                    style=ft.ButtonStyle(bgcolor="#E25C5C", color="white", shape=ft.RoundedRectangleBorder(radius=10))
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # En esta versión de Flet ya no se usa page.dialog / dlg.open;
        # el diálogo se abre y se cierra a través de la página.
        page.show_dialog(dlg)

    def abrir_dialogo_editar(cliente):
        id_cliente = obtener_id_cliente(cliente)

        txt_id_display = ft.TextField(
            label="ID Cliente",
            value=str(id_cliente) if id_cliente else "",
            disabled=True,
            border_color=COLOR_BORDER,
            text_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY)
        )

        txt_edit_nombre = ft.TextField(
            label="Nombre Completo",
            value=str(getattr(cliente, 'nombre_completo', '')),
            border_color=COLOR_BORDER,
            focused_border_color=COLOR_GOLD,
            text_style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)
        )

        txt_edit_tel = ft.TextField(
            label="Teléfono (10 dígitos)",
            value=str(getattr(cliente, 'telefono', '')),
            max_length=10,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=COLOR_BORDER,
            focused_border_color=COLOR_GOLD,
            text_style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)
        )

        def cerrar_dialogo(e=None):
            page.pop_dialog()

        def guardar_cambios(e):
            if txt_edit_nombre.value.strip() and len(txt_edit_tel.value.strip()) == 10:
                setattr(cliente, 'nombre_completo', txt_edit_nombre.value.strip())
                setattr(cliente, 'telefono', txt_edit_tel.value.strip())
                
                if cliente_dao:
                    exito = cliente_dao.actualizar_cliente(cliente)
                    if exito:
                        refrescar_tabla()
                cerrar_dialogo()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Cliente", color=COLOR_GOLD, font_family=FOND_BRAND),
            content=ft.Container(
                width=400,
                content=ft.Column(
                    controls=[txt_id_display, txt_edit_nombre, txt_edit_tel],
                    spacing=12,
                    tight=True
                )
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar Cambios", on_click=guardar_cambios, bgcolor=COLOR_GOLD, color="black"),
            ],
            bgcolor=COLOR_BG_CARD,
        )

        page.show_dialog(dlg)

    def iniciar_pedido(cliente):
        if on_crear_pedido:
            on_crear_pedido(cliente)
        else:
            snack = ft.SnackBar(
                content=ft.Text(f"Iniciando pedido para: {getattr(cliente, 'nombre_completo', '')}", color=COLOR_TEXT_PRIMARY),
                bgcolor=COLOR_BG_CARD,
                open=True
            )
            page.snack_bar = snack
            page.update()

    # -------------------------------------------------------------
    # RENDERIZADO DE TABLA Y REFRESCADO
    # -------------------------------------------------------------

    def construir_dt(lista_clientes):
        filas = []
        for c in lista_clientes:
            cliente_curr = c
            
            id_val = str(obtener_id_cliente(cliente_curr))
            nombre = str(getattr(cliente_curr, 'nombre_completo', ''))
            tel = str(getattr(cliente_curr, 'telefono', ''))
            fecha = str(getattr(cliente_curr, 'fecha_registro', ''))

            def hacer_click_pedido(e, cli=cliente_curr):
                iniciar_pedido(cli)

            def hacer_click_editar(e, cli=cliente_curr):
                abrir_dialogo_editar(cli)

            def hacer_click_eliminar(e, cli=cliente_curr):
                abrir_dialogo_eliminar(cli)

            btn_pedido = ft.IconButton(
                icon=ft.Icons.SHOPPING_BAG_OUTLINED,
                icon_color=COLOR_GOLD,
                tooltip="Nuevo Pedido",
                on_click=hacer_click_pedido
            )

            btn_editar = ft.IconButton(
                icon=ft.Icons.EDIT_OUTLINED,
                icon_color=COLOR_GOLD,
                tooltip="Editar Cliente",
                on_click=hacer_click_editar
            )

            btn_eliminar = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=ft.Colors.RED_400,
                tooltip="Eliminar Cliente",
                on_click=hacer_click_eliminar
            )

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(id_val, color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
                        ft.DataCell(ft.Text(nombre, color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
                        ft.DataCell(ft.Text(tel, color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
                        ft.DataCell(ft.Text(fecha, color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
                        ft.DataCell(
                            ft.Row(
                                controls=[btn_pedido, btn_editar, btn_eliminar],
                                spacing=0,
                                wrap=False
                            )
                        ),
                    ]
                )
            )

        return ft.DataTable(
            border=ft.Border.all(1, COLOR_BORDER),
            border_radius=8,
            vertical_lines=ft.BorderSide(1, COLOR_BORDER),
            horizontal_lines=ft.BorderSide(1, COLOR_BORDER),
            heading_row_color=COLOR_BG_CARD,
            columns=[
                ft.DataColumn(ft.Text("ID", font_family=FOND_BRAND, color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nombre Completo", font_family=FOND_BRAND, color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Teléfono", font_family=FOND_BRAND, color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Fecha de Registro", font_family=FOND_BRAND, color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Acciones", font_family=FOND_BRAND, color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ],
            rows=filas
        )

    def refrescar_tabla(filtro=""):
        if cliente_dao:
            if filtro:
                datos = cliente_dao.buscar_por_filtro(filtro)
            else:
                datos = cliente_dao.obtener_todos()
        else:
            datos = []
        
        contenedor_tabla.controls = [construir_dt(datos)]
        if page:
            page.update()

    # Carga inicial de datos
    if cliente_dao:
        contenedor_tabla.controls = [construir_dt(cliente_dao.obtener_todos())]

    def realizar_busqueda(e):
        refrescar_tabla(e.control.value.strip())

    txt_busqueda = ft.TextField(
        hint_text="Buscar por nombre o teléfono...",
        prefix_icon=ft.Icons.SEARCH,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        text_style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY),
        on_change=realizar_busqueda,
        expand=True
    )

    return ft.Container(
        expand=True,
        bgcolor=COLOR_BG_DARK,
        padding=30,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=COLOR_GOLD,
                            on_click=lambda _: on_regresar(),
                        ),
                        ft.Text(
                            "BASE DE DATOS DE CLIENTES",
                            font_family=FOND_BRAND,
                            size=22,
                            color=COLOR_GOLD,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(height=10),
                ft.Row(controls=[txt_busqueda]),
                ft.Container(height=10),
                ft.Container(
                    bgcolor=COLOR_BG_CARD,
                    padding=20,
                    border_radius=10,
                    border=ft.Border.all(1, COLOR_BORDER),
                    content=contenedor_tabla,
                    expand=True
                )
            ],
            spacing=15,
        )
    )