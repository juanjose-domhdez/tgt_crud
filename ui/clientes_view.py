import flet as ft
from datetime import date
from ui.styles import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_GOLD,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_BORDER,
    FOND_BRAND,
)
from dao.clientes_dao import ClienteDAO
from dao.cita_dao import CitaDAO
from dao.medidas_dao import MedidaDAO
from models.clientes import Cliente


def ClientesView(page: ft.Page = None, on_regresar=None):

    # MODO EDICION
    cliente_editando = {"id": None}

    # DATOS
    datos_completos = []

    # CAMPOS DEL FORMULARIO (alta rápida: solo lo esencial)
    txt_nombre = ft.TextField(
        label="Nombre completo",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        expand=True,
    )
    txt_telefono = ft.TextField(
        label="Teléfono",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        width=200,
    )

    # BUSCADOR
    txt_buscar = ft.TextField(
        hint_text="Buscar cliente por nombre o teléfono...",
        prefix_icon=ft.Icons.SEARCH,
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        content_padding=10,
        height=42,
        expand=True,
        on_change=lambda e: filtrar_tabla(e.page if e and hasattr(e, 'page') else None)
    )

    # MENSAJES
    lbl_mensaje = ft.Text(value="", color=COLOR_GOLD, size=14, weight=ft.FontWeight.BOLD, visible=False)

    col_metricas = ft.Column(spacing=12, expand=True)

    def obtener_pagina_activa(e=None):
        nonlocal page
        if e and hasattr(e, "page") and e.page:
            page = e.page
        return page

    def actualizar_interfaz(e=None):
        pg = obtener_pagina_activa(e)
        try:
            if pg:
                pg.update()
        except Exception:
            pass

    def mostrar_mensaje(texto, es_error=False, e=None):
        lbl_mensaje.value = texto
        lbl_mensaje.color = ft.Colors.RED_400 if es_error else COLOR_GOLD
        lbl_mensaje.visible = True
        actualizar_interfaz(e)

    def ocultar_mensaje():
        lbl_mensaje.visible = False

    def cancelar_edicion(e=None):
        cliente_editando["id"] = None
        txt_nombre.value = ""
        txt_telefono.value = ""
        btn_guardar.text = "Registrar Cliente"
        btn_guardar.icon = ft.Icons.PERSON_ADD_ALT_1
        btn_cancelar_edicion.visible = False
        ocultar_mensaje()
        actualizar_interfaz(e)

    # GUARDAR / ACTUALIZAR CLIENTE
    def guardar_cliente(e):
        nombre = (txt_nombre.value or "").strip()
        telefono = (txt_telefono.value or "").strip()

        if not nombre:
            mostrar_mensaje("El nombre completo es obligatorio.", es_error=True, e=e)
            return

        try:
            if cliente_editando["id"] is None:
                # Evitar duplicar: si ya existe alguien con ese teléfono, se avisa.
                if telefono:
                    existente = ClienteDAO.buscar_por_telefono(telefono)
                    if existente:
                        mostrar_mensaje(
                            f"Ya existe un cliente con ese teléfono: {existente.nombre_completo}.",
                            es_error=True, e=e
                        )
                        return

                cliente = Cliente(
                    nombre_completo=nombre,
                    telefono=telefono,
                    fecha_registro=date.today(),
                )
                ClienteDAO.insertar(cliente)
                msg = "✓ Cliente registrado con éxito."
            else:
                cliente = Cliente(
                    id_cliente=cliente_editando["id"],
                    nombre_completo=nombre,
                    telefono=telefono,
                )
                ClienteDAO.actualizar(cliente)
                msg = "✓ Cliente actualizado con éxito."

            cancelar_edicion(e)
            cargar_datos_tabla(e)
            mostrar_mensaje(msg, e=e)
        except Exception as ex:
            mostrar_mensaje(f"Error al guardar: {ex}", es_error=True, e=e)

    btn_guardar = ft.ElevatedButton(
        "Registrar Cliente",
        icon=ft.Icons.PERSON_ADD_ALT_1,
        bgcolor=COLOR_GOLD,
        color=COLOR_BG_DARK,
        on_click=guardar_cliente
    )

    btn_cancelar_edicion = ft.OutlinedButton(
        "Cancelar Edición",
        icon=ft.Icons.CANCEL,
        icon_color=ft.Colors.RED_400,
        visible=False,
        on_click=cancelar_edicion
    )

    def cargar_en_formulario(cliente, e=None):
        ocultar_mensaje()
        cliente_editando["id"] = cliente.id_cliente
        txt_nombre.value = cliente.nombre_completo
        txt_telefono.value = cliente.telefono
        btn_guardar.text = "Actualizar Cliente"
        btn_guardar.icon = ft.Icons.EDIT
        btn_cancelar_edicion.visible = True
        actualizar_interfaz(e)

    # TABLA DE CLIENTES
    tabla_clientes = ft.DataTable(
        border=ft.Border.all(1, COLOR_BORDER),
        border_radius=8,
        heading_row_color=COLOR_BG_CARD,
        column_spacing=25,
        columns=[
            ft.DataColumn(ft.Text("ID", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Teléfono", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Registrado", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
        ],
        rows=[]
    )

    def actualizar_metricas():
        col_metricas.controls.clear()
        total = len(datos_completos)
        reciente_texto = "Sin clientes aún"
        if datos_completos:
            ordenados = sorted(
                [c for c in datos_completos if c.fecha_registro],
                key=lambda c: c.fecha_registro,
                reverse=True
            )
            if ordenados:
                reciente_texto = f"{ordenados[0].nombre_completo} ({ordenados[0].fecha_registro})"

        col_metricas.controls.extend([
            ft.Text("Resumen de Clientes", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Divider(color=COLOR_BORDER, height=10),
            ft.Container(
                bgcolor=COLOR_BG_DARK,
                padding=20,
                border_radius=8,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Row([
                    ft.Icon(ft.Icons.CONTACTS, color=COLOR_GOLD, size=32),
                    ft.Column([
                        ft.Text("Total de Clientes", size=13, color=COLOR_TEXT_SECONDARY),
                        ft.Text(f"{total} registrados", size=18, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                    ], spacing=2)
                ])
            ),
            ft.Container(
                bgcolor=COLOR_BG_DARK,
                padding=20,
                border_radius=8,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON_ADD_ALT_1, color=COLOR_GOLD, size=32),
                    ft.Column([
                        ft.Text("Registro Más Reciente", size=13, color=COLOR_TEXT_SECONDARY),
                        ft.Text(reciente_texto, size=14, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                    ], spacing=2, expand=True)
                ])
            ),
        ])

    # HISTORIAL DE UN CLIENTE (citas + medidas)
    def ver_historial(cliente, e=None):
        pg = obtener_pagina_activa(e)

        try:
            citas = CitaDAO.obtener_por_cliente(cliente.id_cliente)
        except Exception as ex:
            citas = []
            print(f"❌ Error al obtener citas del cliente: {ex}")

        try:
            medidas = MedidaDAO.obtener_por_cliente(cliente.id_cliente)
        except Exception as ex:
            medidas = []
            print(f"❌ Error al obtener medidas del cliente: {ex}")

        lista_citas = ft.Column(spacing=6)
        if citas:
            for c in citas:
                lista_citas.controls.append(
                    ft.Container(
                        bgcolor=COLOR_BG_DARK,
                        padding=10,
                        border_radius=6,
                        border=ft.Border.all(1, COLOR_BORDER),
                        content=ft.Column(spacing=2, controls=[
                            ft.Text(f"{c['fecha']}  •  {str(c['hora'])[:5]}", color=COLOR_GOLD, weight=ft.FontWeight.BOLD, size=13),
                            ft.Text(f"Motivo: {c['motivo']}", color=COLOR_TEXT_PRIMARY, size=13),
                            ft.Text(f"Atiende: {c['nombre_empleado']}", color=COLOR_TEXT_SECONDARY, size=12),
                        ])
                    )
                )
        else:
            lista_citas.controls.append(ft.Text("Este cliente no tiene citas registradas.", color=COLOR_TEXT_SECONDARY, italic=True))

        lista_medidas = ft.Column(spacing=6)
        if medidas:
            for m in medidas:
                lista_medidas.controls.append(
                    ft.Container(
                        bgcolor=COLOR_BG_DARK,
                        padding=10,
                        border_radius=6,
                        border=ft.Border.all(1, COLOR_BORDER),
                        content=ft.Column(spacing=2, controls=[
                            ft.Text(f"Pedido #{m.id_pedido}  (ficha #{m.id_medida})", color=COLOR_GOLD, weight=ft.FontWeight.BOLD, size=13),
                            ft.Text(
                                f"Pecho: {m.pecho:g}  •  Cintura: {m.cintura:g}  •  Hombros: {m.hombros:g}",
                                color=COLOR_TEXT_PRIMARY, size=12
                            ),
                            ft.Text(
                                f"Manga: {m.manga:g}  •  Largo pantalón: {m.largo_pantalon:g}",
                                color=COLOR_TEXT_PRIMARY, size=12
                            ),
                        ])
                    )
                )
        else:
            lista_medidas.controls.append(ft.Text(
                "Este cliente no tiene fichas de medidas registradas todavía.",
                color=COLOR_TEXT_SECONDARY, italic=True
            ))

        dialogo = ft.AlertDialog(
            modal=True,
            bgcolor=COLOR_BG_CARD,
            title=ft.Text(f"Historial de {cliente.nombre_completo}", color=COLOR_GOLD, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=420,
                height=420,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=15,
                    controls=[
                        ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, color=COLOR_GOLD, size=18),
                                ft.Text("Citas", color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD)]),
                        lista_citas,
                        ft.Divider(color=COLOR_BORDER),
                        ft.Row([ft.Icon(ft.Icons.STRAIGHTEN, color=COLOR_GOLD, size=18),
                                ft.Text("Medidas", color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD)]),
                        lista_medidas,
                    ]
                )
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e2: cerrar_dialogo(dialogo, e2)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        if pg:
            pg.overlay.append(dialogo)
            dialogo.open = True
            pg.update()

    def cerrar_dialogo(dialogo, e=None):
        pg = obtener_pagina_activa(e)
        if pg:
            dialogo.open = False
            pg.update()

    def filtrar_tabla(e=None):
        tabla_clientes.rows.clear()
        busqueda = txt_buscar.value.strip().lower() if txt_buscar.value else ""

        for cliente in datos_completos:
            nombre = cliente.nombre_completo or ""
            telefono = cliente.telefono or ""
            coincide = (busqueda in nombre.lower()) or (busqueda in telefono.lower())

            if coincide:
                tabla_clientes.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(cliente.id_cliente), color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(nombre, color=COLOR_TEXT_PRIMARY)),
                        ft.DataCell(ft.Text(telefono or "-", color=COLOR_TEXT_PRIMARY)),
                        ft.DataCell(ft.Text(str(cliente.fecha_registro) if cliente.fecha_registro else "-", color=COLOR_TEXT_SECONDARY)),
                        ft.DataCell(ft.Row(controls=[
                            ft.IconButton(
                                icon=ft.Icons.HISTORY, icon_color=COLOR_GOLD,
                                tooltip="Ver historial (citas y medidas)",
                                on_click=lambda e, c=cliente: ver_historial(c, e)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED, icon_color=COLOR_GOLD,
                                tooltip="Editar Cliente",
                                on_click=lambda e, c=cliente: cargar_en_formulario(c, e)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400,
                                tooltip="Eliminar Cliente",
                                on_click=lambda e, c=cliente: confirmar_eliminar(c, e)
                            ),
                        ], spacing=0)),
                    ])
                )

        actualizar_interfaz(e)

    def cargar_datos_tabla(e=None):
        nonlocal datos_completos
        try:
            datos_completos = ClienteDAO.seleccionar()
            if datos_completos is None:
                datos_completos = []
        except Exception as ex:
            print(f"❌ Error al llamar seleccionar(): {ex}")
            datos_completos = []

        actualizar_metricas()
        filtrar_tabla(e)

    # ELIMINAR CLIENTE
    def confirmar_eliminar(cliente, e=None):
        pg = obtener_pagina_activa(e)

        def borrar(e_borrar):
            nonlocal pg
            pg = obtener_pagina_activa(e_borrar) or pg
            try:
                ClienteDAO.eliminar(cliente.id_cliente)
                if pg:
                    dialogo.open = False
                    pg.update()
                cargar_datos_tabla(e_borrar)
                mostrar_mensaje("✓ Cliente eliminado con éxito.", e=e_borrar)
            except Exception as ex:
                if pg:
                    dialogo.open = False
                    pg.update()
                mostrar_mensaje(
                    f"No se pudo eliminar (probablemente tiene citas o pedidos ligados): {ex}",
                    es_error=True, e=e_borrar
                )

        def cancelar(e_canc):
            nonlocal pg
            pg = obtener_pagina_activa(e_canc) or pg
            if pg:
                dialogo.open = False
                pg.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación", color=COLOR_GOLD, weight=ft.FontWeight.BOLD),
            content=ft.Text(f"¿Eliminar al cliente {cliente.nombre_completo}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Eliminar", bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE, on_click=borrar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        if pg:
            pg.overlay.append(dialogo)
            dialogo.open = True
            pg.update()

    cargar_datos_tabla()

    encabezado = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text(
                        "BASE DE CLIENTES",
                        font_family=FOND_BRAND,
                        size=22,
                        color=COLOR_GOLD,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Historial y medidas de clientes",
                        size=13,
                        color=COLOR_TEXT_SECONDARY,
                    ),
                ],
                spacing=2
            )
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    if on_regresar:
        encabezado.controls.insert(0, ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=COLOR_GOLD,
            icon_size=28,
            tooltip="Volver",
            on_click=lambda e: on_regresar()
        ))

    vista_principal = ft.Column(
        controls=[
            encabezado,

            ft.Divider(color=COLOR_BORDER, height=10),

            ft.Container(
                bgcolor=COLOR_BG_CARD,
                padding=20,
                border_radius=10,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Column(
                    controls=[
                        ft.Text("Registrar / Editar Cliente", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                        ft.Row(controls=[txt_nombre, txt_telefono], spacing=15),
                        ft.Row(
                            controls=[btn_guardar, btn_cancelar_edicion, lbl_mensaje],
                            spacing=15,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
                    spacing=12,
                )
            ),

            ft.Container(height=5),

            ft.Row(
                controls=[
                    ft.Container(
                        bgcolor=COLOR_BG_CARD,
                        padding=15,
                        border_radius=10,
                        border=ft.Border.all(1, COLOR_BORDER),
                        expand=2,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LIST_ALT, color=COLOR_GOLD),
                                        ft.Text("Clientes Registrados", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=10
                                ),
                                ft.Divider(color=COLOR_BORDER, height=5),
                                txt_buscar,
                                ft.Divider(color=COLOR_BORDER, height=5),
                                ft.Row(controls=[tabla_clientes], scroll=ft.ScrollMode.AUTO)
                            ],
                            spacing=10
                        )
                    ),
                    ft.Container(
                        bgcolor=COLOR_BG_CARD,
                        padding=15,
                        border_radius=10,
                        border=ft.Border.all(1, COLOR_BORDER),
                        expand=1,
                        content=col_metricas
                    )
                ],
                spacing=15,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    return vista_principal
