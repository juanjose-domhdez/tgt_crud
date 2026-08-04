import flet as ft
from datetime import datetime
from ui.styles import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_GOLD,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_BORDER,
    FOND_BRAND,
)
from dao.cita_dao import CitaDAO
from dao.clientes_dao import ClienteDAO
from dao.empleado_dao import EmpleadoDAO
from models.cita import Cita


def CitaView(page: ft.Page = None, on_regresar=None):

    dao = CitaDAO()

    # MODO EDICION
    cita_editando = {"id": None}

    # FILTRADO
    datos_completos = []
    motivo_seleccionado = {"valor": "Todos"}

    # OPCIONES DE COMBOS (se recargan cada vez que se abre la vista)
    dd_cliente = ft.Dropdown(
        label="Cliente",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        bgcolor=COLOR_BG_CARD,
        expand=True,
        options=[],
    )
    dd_empleado = ft.Dropdown(
        label="Empleado que atiende",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        bgcolor=COLOR_BG_CARD,
        expand=True,
        options=[],
    )

    txt_fecha = ft.TextField(
        label="Fecha (AAAA-MM-DD)",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        width=180
    )
    txt_hora = ft.TextField(
        label="Hora (HH:MM)",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        width=140
    )

    opciones_motivo = ["Toma de medidas", "Prueba de traje", "Entrega de pedido", "Asesoría / cotización"]

    dd_motivo = ft.Dropdown(
        label="Motivo",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        bgcolor=COLOR_BG_CARD,
        value=opciones_motivo[0],
        expand=True,
        options=[ft.dropdown.Option(m, content=ft.Text(m, color=COLOR_TEXT_PRIMARY)) for m in opciones_motivo],
    )

    # BUSCADOR
    txt_buscar = ft.TextField(
        hint_text="Buscar cita por cliente o empleado...",
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

    def cargar_combos():
        try:
            dd_cliente.options = [
                ft.dropdown.Option(str(c.id_cliente), content=ft.Text(c.nombre_completo, color=COLOR_TEXT_PRIMARY))
                for c in ClienteDAO.seleccionar()
            ]
        except Exception as ex:
            print(f"❌ Error al cargar clientes: {ex}")
            dd_cliente.options = []

        try:
            dd_empleado.options = [
                ft.dropdown.Option(str(emp.id_empleado), content=ft.Text(f"{emp.nombre} ({emp.puesto})", color=COLOR_TEXT_PRIMARY))
                for emp in EmpleadoDAO.seleccionar()
            ]
        except Exception as ex:
            print(f"❌ Error al cargar empleados: {ex}")
            dd_empleado.options = []

    def cancelar_edicion(e=None):
        cita_editando["id"] = None
        dd_cliente.value = None
        dd_empleado.value = None
        txt_fecha.value = ""
        txt_hora.value = ""
        dd_motivo.value = opciones_motivo[0]
        btn_guardar.text = "Agendar Cita"
        btn_guardar.icon = ft.Icons.SAVE
        btn_cancelar_edicion.visible = False
        ocultar_mensaje()
        actualizar_interfaz(e)

    # GUARDAR / ACTUALIZAR CITA
    def guardar_cita(e):
        if not dd_cliente.value or not dd_empleado.value:
            mostrar_mensaje("Selecciona un cliente y un empleado.", es_error=True, e=e)
            return

        fecha_raw = txt_fecha.value.strip() if txt_fecha.value else ""
        hora_raw = txt_hora.value.strip() if txt_hora.value else ""

        try:
            fecha = datetime.strptime(fecha_raw, "%Y-%m-%d").date()
            hora = datetime.strptime(hora_raw, "%H:%M").time()
        except ValueError:
            mostrar_mensaje("Revisa el formato de fecha (AAAA-MM-DD) y hora (HH:MM).", es_error=True, e=e)
            return

        cita = Cita(
            id_cita=cita_editando["id"],
            id_cliente=int(dd_cliente.value),
            id_empleado=int(dd_empleado.value),
            fecha=fecha,
            hora=hora,
            motivo=dd_motivo.value or "",
        )

        try:
            if cita_editando["id"] is None:
                dao.insertar(cita)
                msg = "✓ Cita agendada con éxito."
            else:
                dao.actualizar(cita)
                msg = "✓ Cita actualizada con éxito."

            cancelar_edicion(e)
            cargar_datos_tabla(e)
            mostrar_mensaje(msg, e=e)
        except Exception as ex:
            mostrar_mensaje(f"Error al guardar: {ex}", es_error=True, e=e)

    btn_guardar = ft.ElevatedButton(
        "Agendar Cita",
        icon=ft.Icons.SAVE,
        bgcolor=COLOR_GOLD,
        color=COLOR_BG_DARK,
        on_click=guardar_cita
    )

    btn_cancelar_edicion = ft.OutlinedButton(
        "Cancelar Edición",
        icon=ft.Icons.CANCEL,
        icon_color=ft.Colors.RED_400,
        visible=False,
        on_click=cancelar_edicion
    )

    def cargar_en_formulario(cita, e=None):
        ocultar_mensaje()
        cargar_combos()
        cita_editando["id"] = cita["id_cita"]
        dd_cliente.value = str(cita["id_cliente"])
        dd_empleado.value = str(cita["id_empleado"])
        txt_fecha.value = str(cita["fecha"])
        txt_hora.value = str(cita["hora"])[:5]
        dd_motivo.value = cita["motivo"] if cita["motivo"] in opciones_motivo else opciones_motivo[0]

        btn_guardar.text = "Actualizar Cita"
        btn_guardar.icon = ft.Icons.EDIT
        btn_cancelar_edicion.visible = True
        actualizar_interfaz(e)

    # TABLA DE CITAS
    tabla_citas = ft.DataTable(
        border=ft.Border.all(1, COLOR_BORDER),
        border_radius=8,
        heading_row_color=COLOR_BG_CARD,
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text("ID", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Cliente", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Empleado", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Fecha", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Hora", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Motivo", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
        ],
        rows=[]
    )

    def seleccionar_filtro_motivo(motivo, e=None):
        motivo_seleccionado["valor"] = motivo
        for btn in row_filtros.controls:
            if btn.data == motivo:
                btn.bgcolor = COLOR_GOLD
                btn.color = COLOR_BG_DARK
            else:
                btn.bgcolor = COLOR_BG_DARK
                btn.color = COLOR_TEXT_SECONDARY
        filtrar_tabla(e)

    motivos_filtro = ["Todos"] + opciones_motivo

    row_filtros = ft.Row(
        controls=[
            ft.ElevatedButton(
                m,
                data=m,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
                bgcolor=COLOR_GOLD if m == "Todos" else COLOR_BG_DARK,
                color=COLOR_BG_DARK if m == "Todos" else COLOR_TEXT_SECONDARY,
                on_click=lambda e, mm=m: seleccionar_filtro_motivo(mm, e)
            ) for m in motivos_filtro
        ],
        spacing=8,
        scroll=ft.ScrollMode.AUTO
    )

    def actualizar_metricas():
        col_metricas.controls.clear()
        total_citas = len(datos_completos)

        hoy = datetime.now().date()
        proximas = sorted(
            [c for c in datos_completos if c["fecha"] and c["fecha"] >= hoy],
            key=lambda c: (c["fecha"], c["hora"])
        )
        proxima_texto = "Sin citas próximas"
        if proximas:
            p = proximas[0]
            proxima_texto = f"{p['nombre_cliente']} - {p['fecha']} {str(p['hora'])[:5]}"

        col_metricas.controls.extend([
            ft.Text("Resumen de Citas", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Divider(color=COLOR_BORDER, height=10),
            ft.Container(
                bgcolor=COLOR_BG_DARK,
                padding=20,
                border_radius=8,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_MONTH, color=COLOR_GOLD, size=32),
                    ft.Column([
                        ft.Text("Total de Citas", size=13, color=COLOR_TEXT_SECONDARY),
                        ft.Text(f"{total_citas} citas registradas", size=18, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                    ], spacing=2)
                ])
            ),
            ft.Container(
                bgcolor=COLOR_BG_DARK,
                padding=20,
                border_radius=8,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Row([
                    ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE_OUTLINED, color=COLOR_GOLD, size=32),
                    ft.Column([
                        ft.Text("Próxima Cita", size=13, color=COLOR_TEXT_SECONDARY),
                        ft.Text(proxima_texto, size=14, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                    ], spacing=2, expand=True)
                ])
            ),
        ])

    def filtrar_tabla(e=None):
        tabla_citas.rows.clear()
        busqueda = txt_buscar.value.strip().lower() if txt_buscar.value else ""
        motivo_filtro = motivo_seleccionado["valor"]

        for cita in datos_completos:
            nombre_cliente = cita["nombre_cliente"] or ""
            nombre_empleado = cita["nombre_empleado"] or ""
            motivo = cita["motivo"] or ""

            coincide_texto = (busqueda in nombre_cliente.lower()) or (busqueda in nombre_empleado.lower())
            coincide_motivo = (motivo_filtro == "Todos") or (motivo_filtro == motivo)

            if coincide_texto and coincide_motivo:
                tabla_citas.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(cita["id_cita"]), color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(nombre_cliente, color=COLOR_TEXT_PRIMARY)),
                        ft.DataCell(ft.Text(nombre_empleado, color=COLOR_TEXT_PRIMARY)),
                        ft.DataCell(ft.Text(str(cita["fecha"]), color=COLOR_TEXT_SECONDARY)),
                        ft.DataCell(ft.Text(str(cita["hora"])[:5], color=COLOR_TEXT_SECONDARY)),
                        ft.DataCell(ft.Text(motivo, color=COLOR_TEXT_PRIMARY)),
                        ft.DataCell(ft.Row(controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED, icon_color=COLOR_GOLD,
                                tooltip="Editar Cita",
                                on_click=lambda e, c=cita: cargar_en_formulario(c, e)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400,
                                tooltip="Eliminar Cita",
                                on_click=lambda e, c=cita: confirmar_eliminar(c, e)
                            ),
                        ], spacing=0)),
                    ])
                )

        actualizar_interfaz(e)

    def cargar_datos_tabla(e=None):
        nonlocal datos_completos
        try:
            datos_completos = dao.seleccionar()
            if datos_completos is None:
                datos_completos = []
        except Exception as ex:
            print(f"❌ Error al llamar seleccionar(): {ex}")
            datos_completos = []

        actualizar_metricas()
        filtrar_tabla(e)

    # ELIMINAR CITA
    def confirmar_eliminar(cita, e=None):
        pg = obtener_pagina_activa(e)

        def borrar(e_borrar):
            nonlocal pg
            pg = obtener_pagina_activa(e_borrar) or pg
            try:
                dao.eliminar(cita["id_cita"])
                if pg:
                    dialogo.open = False
                    pg.update()
                cargar_datos_tabla(e_borrar)
                mostrar_mensaje("✓ Cita eliminada con éxito.", e=e_borrar)
            except Exception as ex:
                if pg:
                    dialogo.open = False
                    pg.update()
                mostrar_mensaje(f"Error al eliminar: {ex}", es_error=True, e=e_borrar)

        def cancelar(e_canc):
            nonlocal pg
            pg = obtener_pagina_activa(e_canc) or pg
            if pg:
                dialogo.open = False
                pg.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación", color=COLOR_GOLD, weight=ft.FontWeight.BOLD),
            content=ft.Text(f"¿Eliminar la cita de {cita['nombre_cliente']} el {cita['fecha']}?"),
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

    cargar_combos()
    cargar_datos_tabla()

    vista_principal = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=COLOR_GOLD,
                        icon_size=28,
                        tooltip="Volver al menú de Citas y Medidas",
                        on_click=lambda e: on_regresar() if on_regresar else None
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "AGENDA DE CITAS",
                                font_family=FOND_BRAND,
                                size=22,
                                color=COLOR_GOLD,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Citas de prueba, toma de medidas y entregas",
                                size=13,
                                color=COLOR_TEXT_SECONDARY,
                            ),
                        ],
                        spacing=2
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),

            ft.Divider(color=COLOR_BORDER, height=10),

            ft.Container(
                bgcolor=COLOR_BG_CARD,
                padding=20,
                border_radius=10,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Column(
                    controls=[
                        ft.Text("Agendar / Editar Cita", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                        ft.Row(controls=[dd_cliente, dd_empleado], spacing=15),
                        ft.Row(controls=[txt_fecha, txt_hora, dd_motivo], spacing=15),
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
                                        ft.Text("Citas Agendadas", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=10
                                ),
                                ft.Divider(color=COLOR_BORDER, height=5),
                                txt_buscar,
                                row_filtros,
                                ft.Divider(color=COLOR_BORDER, height=5),
                                ft.Row(controls=[tabla_citas], scroll=ft.ScrollMode.AUTO)
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
