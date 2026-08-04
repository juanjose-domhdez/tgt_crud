import flet as ft
from ui.styles import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_GOLD,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_BORDER,
    FOND_BRAND,
)
from dao.medidas_dao import MedidaDAO
from models.medidas import Medida


def MedidaView(page: ft.Page = None, on_regresar=None):

    dao = MedidaDAO()

    # MODO EDICION
    medida_editando = {"id": None}

    # DATOS
    datos_completos = []

    # CAMPOS DEL FORMULARIO
    txt_pedido = ft.TextField(
        label="ID de Pedido",
        hint_text="Ej. 12",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=150
    )
    txt_pecho = ft.TextField(
        label="Pecho (cm)",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=140
    )
    txt_cintura = ft.TextField(
        label="Cintura (cm)",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=140
    )
    txt_hombros = ft.TextField(
        label="Hombros (cm)",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=140
    )
    txt_manga = ft.TextField(
        label="Largo de Manga (cm)",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=170
    )
    txt_largo_pantalon = ft.TextField(
        label="Largo de Pantalón (cm)",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=180
    )

    # BUSCADOR
    txt_buscar = ft.TextField(
        hint_text="Buscar ficha por número de pedido...",
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
        medida_editando["id"] = None
        txt_pedido.value = ""
        txt_pecho.value = ""
        txt_cintura.value = ""
        txt_hombros.value = ""
        txt_manga.value = ""
        txt_largo_pantalon.value = ""
        btn_guardar.text = "Guardar Ficha"
        btn_guardar.icon = ft.Icons.SAVE
        btn_cancelar_edicion.visible = False
        ocultar_mensaje()
        actualizar_interfaz(e)

    def _a_decimal(valor, campo, e):
        valor = (valor or "").strip().replace(",", ".")
        if valor == "":
            return 0.0, None
        try:
            return float(valor), None
        except ValueError:
            return None, f"El campo '{campo}' debe ser un número válido."

    # GUARDAR / ACTUALIZAR FICHA DE MEDIDAS
    def guardar_medida(e):
        pedido_raw = txt_pedido.value.strip() if txt_pedido.value else ""
        if not pedido_raw:
            mostrar_mensaje("Ingresa el ID de pedido al que pertenece la ficha.", es_error=True, e=e)
            return
        try:
            id_pedido = int(pedido_raw)
        except ValueError:
            mostrar_mensaje("El ID de pedido debe ser un número entero.", es_error=True, e=e)
            return

        pecho, err = _a_decimal(txt_pecho.value, "Pecho", e)
        if err:
            mostrar_mensaje(err, es_error=True, e=e)
            return
        cintura, err = _a_decimal(txt_cintura.value, "Cintura", e)
        if err:
            mostrar_mensaje(err, es_error=True, e=e)
            return
        hombros, err = _a_decimal(txt_hombros.value, "Hombros", e)
        if err:
            mostrar_mensaje(err, es_error=True, e=e)
            return
        manga, err = _a_decimal(txt_manga.value, "Largo de manga", e)
        if err:
            mostrar_mensaje(err, es_error=True, e=e)
            return
        largo_pantalon, err = _a_decimal(txt_largo_pantalon.value, "Largo de pantalón", e)
        if err:
            mostrar_mensaje(err, es_error=True, e=e)
            return

        medida = Medida(
            id_medida=medida_editando["id"],
            id_pedido=id_pedido,
            pecho=pecho,
            cintura=cintura,
            hombros=hombros,
            manga=manga,
            largo_pantalon=largo_pantalon,
        )

        try:
            if medida_editando["id"] is None:
                dao.insertar(medida)
                msg = "✓ Ficha de medidas guardada con éxito."
            else:
                dao.actualizar(medida)
                msg = "✓ Ficha de medidas actualizada con éxito."

            cancelar_edicion(e)
            cargar_datos_tabla(e)
            mostrar_mensaje(msg, e=e)
        except Exception as ex:
            mostrar_mensaje(f"Error al guardar: {ex}", es_error=True, e=e)

    btn_guardar = ft.ElevatedButton(
        "Guardar Ficha",
        icon=ft.Icons.SAVE,
        bgcolor=COLOR_GOLD,
        color=COLOR_BG_DARK,
        on_click=guardar_medida
    )

    btn_cancelar_edicion = ft.OutlinedButton(
        "Cancelar Edición",
        icon=ft.Icons.CANCEL,
        icon_color=ft.Colors.RED_400,
        visible=False,
        on_click=cancelar_edicion
    )

    def cargar_en_formulario(medida, e=None):
        ocultar_mensaje()
        medida_editando["id"] = medida.id_medida
        txt_pedido.value = str(medida.id_pedido) if medida.id_pedido is not None else ""
        txt_pecho.value = str(medida.pecho)
        txt_cintura.value = str(medida.cintura)
        txt_hombros.value = str(medida.hombros)
        txt_manga.value = str(medida.manga)
        txt_largo_pantalon.value = str(medida.largo_pantalon)

        btn_guardar.text = "Actualizar Ficha"
        btn_guardar.icon = ft.Icons.EDIT
        btn_cancelar_edicion.visible = True
        actualizar_interfaz(e)

    # TABLA DE FICHAS DE MEDIDAS
    tabla_medidas = ft.DataTable(
        border=ft.Border.all(1, COLOR_BORDER),
        border_radius=8,
        heading_row_color=COLOR_BG_CARD,
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text("ID", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Pedido", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Pecho", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Cintura", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Hombros", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Manga", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Largo Pantalón", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
        ],
        rows=[]
    )

    def actualizar_metricas():
        col_metricas.controls.clear()
        total = len(datos_completos)
        ultimo_texto = "Sin registros aún"
        if datos_completos:
            u = datos_completos[0]
            ultimo_texto = f"Pedido #{u.id_pedido} (ficha #{u.id_medida})"

        col_metricas.controls.extend([
            ft.Text("Resumen de Fichas", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Divider(color=COLOR_BORDER, height=10),
            ft.Container(
                bgcolor=COLOR_BG_DARK,
                padding=20,
                border_radius=8,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Row([
                    ft.Icon(ft.Icons.STRAIGHTEN, color=COLOR_GOLD, size=32),
                    ft.Column([
                        ft.Text("Total de Fichas", size=13, color=COLOR_TEXT_SECONDARY),
                        ft.Text(f"{total} fichas registradas", size=18, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                    ], spacing=2)
                ])
            ),
            ft.Container(
                bgcolor=COLOR_BG_DARK,
                padding=20,
                border_radius=8,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Row([
                    ft.Icon(ft.Icons.HISTORY, color=COLOR_GOLD, size=32),
                    ft.Column([
                        ft.Text("Último Registro", size=13, color=COLOR_TEXT_SECONDARY),
                        ft.Text(ultimo_texto, size=14, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                    ], spacing=2, expand=True)
                ])
            ),
        ])

    def filtrar_tabla(e=None):
        tabla_medidas.rows.clear()
        busqueda = txt_buscar.value.strip().lower() if txt_buscar.value else ""

        for m in datos_completos:
            coincide = (busqueda == "") or (busqueda in str(m.id_pedido).lower())
            if coincide:
                tabla_medidas.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(m.id_medida), color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"#{m.id_pedido}", color=COLOR_TEXT_PRIMARY)),
                        ft.DataCell(ft.Text(f"{m.pecho:g}", color=COLOR_TEXT_SECONDARY)),
                        ft.DataCell(ft.Text(f"{m.cintura:g}", color=COLOR_TEXT_SECONDARY)),
                        ft.DataCell(ft.Text(f"{m.hombros:g}", color=COLOR_TEXT_SECONDARY)),
                        ft.DataCell(ft.Text(f"{m.manga:g}", color=COLOR_TEXT_SECONDARY)),
                        ft.DataCell(ft.Text(f"{m.largo_pantalon:g}", color=COLOR_TEXT_SECONDARY)),
                        ft.DataCell(ft.Row(controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED, icon_color=COLOR_GOLD,
                                tooltip="Editar Ficha",
                                on_click=lambda e, m=m: cargar_en_formulario(m, e)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400,
                                tooltip="Eliminar Ficha",
                                on_click=lambda e, m=m: confirmar_eliminar(m, e)
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

    # ELIMINAR FICHA
    def confirmar_eliminar(medida, e=None):
        pg = obtener_pagina_activa(e)

        def borrar(e_borrar):
            nonlocal pg
            pg = obtener_pagina_activa(e_borrar) or pg
            try:
                dao.eliminar(medida.id_medida)
                if pg:
                    dialogo.open = False
                    pg.update()
                cargar_datos_tabla(e_borrar)
                mostrar_mensaje("✓ Ficha eliminada con éxito.", e=e_borrar)
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
            content=ft.Text(f"¿Eliminar la ficha de medidas del pedido #{medida.id_pedido}?"),
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
                                "FICHAS TÉCNICAS DE MEDIDAS",
                                font_family=FOND_BRAND,
                                size=22,
                                color=COLOR_GOLD,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Registro de medidas de confección por pedido",
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
                        ft.Text("Registrar / Editar Ficha de Medidas", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                        ft.Row(controls=[txt_pedido, txt_pecho, txt_cintura, txt_hombros], spacing=15, wrap=True),
                        ft.Row(
                            controls=[txt_manga, txt_largo_pantalon, btn_guardar, btn_cancelar_edicion, lbl_mensaje],
                            spacing=15,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            wrap=True
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
                                        ft.Text("Fichas Registradas", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=10
                                ),
                                ft.Divider(color=COLOR_BORDER, height=5),
                                txt_buscar,
                                ft.Divider(color=COLOR_BORDER, height=5),
                                ft.Row(controls=[tabla_medidas], scroll=ft.ScrollMode.AUTO)
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
