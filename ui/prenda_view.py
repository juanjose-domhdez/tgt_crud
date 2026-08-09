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
from dao.prenda_dao import PrendaDAO
from models.prenda import Prenda


def PrendaView(page: ft.Page = None, on_regresar=None):

    dao = PrendaDAO()

    
    prenda_editando = {"id": None}
    
    # FILTRADO
    datos_completos = []
    categoria_seleccionada = {"valor": "Todos"}

    
    txt_nombre = ft.TextField(
        label="Nombre / Modelo", 
        border_color=COLOR_BORDER, 
        color=COLOR_TEXT_PRIMARY, 
        expand=True
    )

    dd_tipo = ft.Dropdown(
        label="Tipo / Categoría",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        bgcolor=COLOR_BG_CARD,
        expand=True,
        value="Saco",
        options=[
            ft.dropdown.Option("Saco", content=ft.Text("Saco", color=COLOR_TEXT_PRIMARY)),
            ft.dropdown.Option("Pantalón", content=ft.Text("Pantalón", color=COLOR_TEXT_PRIMARY)),
            ft.dropdown.Option("Chaleco", content=ft.Text("Chaleco", color=COLOR_TEXT_PRIMARY)),
            ft.dropdown.Option("Camisa", content=ft.Text("Camisa", color=COLOR_TEXT_PRIMARY)),
            ft.dropdown.Option("Traje Completo", content=ft.Text("Traje Completo", color=COLOR_TEXT_PRIMARY)),
        ]
    )

    # TALLA - COLOR - PRECIO - STOCK
    txt_talla = ft.TextField(
        label="Talla (ej. S, M, L)", 
        border_color=COLOR_BORDER, 
        color=COLOR_TEXT_PRIMARY, 
        width=180
    )

    txt_color = ft.TextField(
        label="Color", 
        border_color=COLOR_BORDER, 
        color=COLOR_TEXT_PRIMARY, 
        expand=True
    )

    txt_precio = ft.TextField(
        label="Precio Base ($)", 
        border_color=COLOR_BORDER, 
        color=COLOR_TEXT_PRIMARY, 
        keyboard_type=ft.KeyboardType.NUMBER,
        width=150
    )

    txt_stock = ft.TextField(
        label="Stock",
        value="1",
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=120
    )

    # BUSCADOR
    txt_buscar = ft.TextField(
        hint_text="Buscar prenda por modelo, tipo, talla o color...",
        prefix_icon=ft.Icons.SEARCH,
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        content_padding=10,
        height=42,
        expand=True,
        on_change=lambda e: filtrar_tabla(e.page if e and hasattr(e, 'page') else None)
    )

    # MENSAJES
    lbl_mensaje = ft.Text(
        value="",
        color=COLOR_GOLD,
        size=14,
        weight=ft.FontWeight.BOLD,
        visible=False
    )

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
        prenda_editando["id"] = None
        txt_nombre.value = ""
        dd_tipo.value = "Saco"
        txt_talla.value = ""
        txt_color.value = ""
        txt_precio.value = ""
        txt_stock.value = "1"
        btn_guardar.text = "Guardar Prenda"
        btn_guardar.icon = ft.Icons.SAVE
        btn_cancelar_edicion.visible = False
        ocultar_mensaje()
        actualizar_interfaz(e)

    # GUARDAR / ACTUALIZAR PRENDAS
    def guardar_prenda(e):
        nombre = txt_nombre.value.strip() if txt_nombre.value else ""
        tipo = dd_tipo.value if dd_tipo.value else "Saco"
        talla = txt_talla.value.strip() if txt_talla.value else "-"
        color = txt_color.value.strip() if txt_color.value else "-"
        precio_raw = txt_precio.value.strip() if txt_precio.value else ""
        stock_raw = txt_stock.value.strip() if txt_stock.value else "1"
        
        precio_raw = precio_raw.replace("$", "").replace(",", "")

        if not nombre or not precio_raw:
            mostrar_mensaje("Ingresa un modelo y precio válidos.", es_error=True, e=e)
            return

        try:
            precio = float(precio_raw)
            stock = int(stock_raw)

            if prenda_editando["id"] is None:
                nueva_prenda = Prenda(
                    tipo_prenda=tipo,
                    modelo=nombre,
                    talla=talla,
                    color=color,
                    precio=precio,
                    stock=stock
                )
                dao.insertar(nueva_prenda)
                msg = f"✓ Prenda '{nombre}' guardada con éxito."
            else:
                prenda_actualizada = Prenda(
                    id_prenda=prenda_editando["id"],
                    tipo_prenda=tipo,
                    modelo=nombre,
                    talla=talla,
                    color=color,
                    precio=precio,
                    stock=stock
                )
                dao.actualizar(prenda_actualizada)
                msg = f"✓ Prenda '{nombre}' actualizada con éxito."

            cancelar_edicion(e)
            cargar_datos_tabla(e)
            mostrar_mensaje(msg, e=e)

        except ValueError:
            mostrar_mensaje("Verifica que el precio y stock sean valores numéricos válidos.", es_error=True, e=e)
        except Exception as ex:
            mostrar_mensaje(f"Error al guardar: {ex}", es_error=True, e=e)

    # BOTONES DE ACCIÓN
    btn_guardar = ft.ElevatedButton(
        "Guardar Prenda",
        icon=ft.Icons.SAVE,
        bgcolor=COLOR_GOLD,
        color=COLOR_BG_DARK,
        on_click=guardar_prenda
    )

    btn_cancelar_edicion = ft.OutlinedButton(
        "Cancelar Edición",
        icon=ft.Icons.CANCEL,
        icon_color=ft.Colors.RED_400,
        visible=False,
        on_click=cancelar_edicion
    )

    def cargar_en_formulario(id_prenda, modelo, tipo, talla, color, precio, stock=1, e=None):
        ocultar_mensaje()
        prenda_editando["id"] = id_prenda
        txt_nombre.value = modelo
        
        opciones_validas = ["Saco", "Pantalón", "Chaleco", "Camisa", "Traje Completo"]
        dd_tipo.value = tipo if tipo in opciones_validas else "Saco"
        
        txt_talla.value = talla if talla != "-" else ""
        txt_color.value = color if color != "-" else ""
        txt_precio.value = str(precio)
        txt_stock.value = str(stock)
        
        btn_guardar.text = "Actualizar Prenda"
        btn_guardar.icon = ft.Icons.EDIT
        btn_cancelar_edicion.visible = True
        actualizar_interfaz(e)

    # TABLA DE PRENDAS
    tabla_inventario = ft.DataTable(
        border=ft.Border.all(1, COLOR_BORDER),
        border_radius=8,
        heading_row_color=COLOR_BG_CARD,
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text("ID", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Tipo", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Modelo", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Talla", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Color", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Precio Base", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Stock", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
        ],
        rows=[]
    )

    def seleccionar_filtro_categoria(categoria, e=None):
        categoria_seleccionada["valor"] = categoria
        for btn in row_filtros.controls:
            if btn.data == categoria:
                btn.bgcolor = COLOR_GOLD
                btn.color = COLOR_BG_DARK
            else:
                btn.bgcolor = COLOR_BG_DARK
                btn.color = COLOR_TEXT_SECONDARY
        filtrar_tabla(e)

    categorias_filtro = ["Todos", "Saco", "Pantalón", "Chaleco", "Camisa", "Traje Completo"]
    
    row_filtros = ft.Row(
        controls=[
            ft.ElevatedButton(
                cat,
                data=cat,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
                bgcolor=COLOR_GOLD if cat == "Todos" else COLOR_BG_DARK,
                color=COLOR_BG_DARK if cat == "Todos" else COLOR_TEXT_SECONDARY,
                on_click=lambda e, c=cat: seleccionar_filtro_categoria(c, e)
            ) for cat in categorias_filtro
        ],
        spacing=8,
        scroll=ft.ScrollMode.AUTO
    )

    def actualizar_metricas():
        col_metricas.controls.clear()
        total_items = len(datos_completos)

        col_metricas.controls.extend([
            ft.Text("Resumen del Inventario", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Divider(color=COLOR_BORDER, height=10),
            
            ft.Container(
                bgcolor=COLOR_BG_DARK,
                padding=20,
                border_radius=8,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECKROOM, color=COLOR_GOLD, size=32),
                    ft.Column([
                        ft.Text("Total de Prendas", size=13, color=COLOR_TEXT_SECONDARY),
                        ft.Text(f"{total_items} prendas registradas", size=18, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                    ], spacing=2)
                ])
            ),
        ])

    def extraer_datos_item(item):
        if hasattr(item, "id_prenda") or hasattr(item, "modelo"):
            id_p = getattr(item, "id_prenda", getattr(item, "id", ""))
            tipo = getattr(item, "tipo_prenda", "") or ""
            modelo = getattr(item, "modelo", "") or ""
            talla = getattr(item, "talla", "-") or "-"
            color = getattr(item, "color", "-") or "-"
            precio = getattr(item, "precio", 0.0) or 0.0
            stock = getattr(item, "stock", 1) or 1
            return id_p, str(tipo), str(modelo), str(talla), str(color), float(precio), int(stock)

        if isinstance(item, (list, tuple)):
            id_p = item[0] if len(item) > 0 else ""
            tipo = item[1] if len(item) > 1 and item[1] is not None else ""
            modelo = item[2] if len(item) > 2 and item[2] is not None else ""
            talla = item[3] if len(item) > 3 and item[3] is not None else "-"
            color = item[4] if len(item) > 4 and item[4] is not None else "-"
            try:
                precio = float(item[5]) if len(item) > 5 and item[5] is not None else 0.0
            except (ValueError, TypeError):
                precio = 0.0
            try:
                stock = int(item[6]) if len(item) > 6 and item[6] is not None else 1
            except (ValueError, TypeError):
                stock = 1

            return id_p, str(tipo), str(modelo), str(talla), str(color), precio, stock

        return "", "", str(item), "-", "-", 0.0, 1

    def filtrar_tabla(e=None):
        tabla_inventario.rows.clear()
        busqueda = txt_buscar.value.strip().lower() if txt_buscar.value else ""
        cat_filtro = categoria_seleccionada["valor"]

        for item in datos_completos:
            id_p, tipo, modelo, talla, color, precio, stock = extraer_datos_item(item)

            coincide_texto = (
                (busqueda in modelo.lower()) or 
                (busqueda in tipo.lower()) or 
                (busqueda in talla.lower()) or 
                (busqueda in color.lower())
            )
            coincide_cat = (cat_filtro == "Todos") or (cat_filtro.lower() == tipo.lower())

            if coincide_texto and coincide_cat:
                tabla_inventario.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(id_p), color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(tipo if tipo else "-", color=COLOR_TEXT_SECONDARY)),
                            ft.DataCell(ft.Text(modelo if modelo else "-", color=COLOR_TEXT_PRIMARY)),
                            ft.DataCell(ft.Text(talla if talla else "-", color=COLOR_TEXT_PRIMARY)),
                            ft.DataCell(ft.Text(color if color else "-", color=COLOR_TEXT_PRIMARY)),
                            ft.DataCell(ft.Text(f"${precio:.2f}", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(str(stock), color=COLOR_TEXT_PRIMARY)),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT_OUTLINED,
                                            icon_color=COLOR_GOLD,
                                            tooltip="Editar Prenda",
                                            on_click=lambda e, i=id_p, m=modelo, t=tipo, ta=talla, c=color, p=precio, s=stock: cargar_en_formulario(i, m, t, ta, c, p, s, e)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE,
                                            icon_color=ft.Colors.RED_400,
                                            tooltip="Eliminar Prenda",
                                            on_click=lambda e, i=id_p, m=modelo: confirmar_eliminar(i, m, e)
                                        ),
                                    ],
                                    spacing=0
                                )
                            ),
                        ]
                    )
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

    # ELIMINAR PRENDA
    def confirmar_eliminar(id_p, nombre, e=None):
        pg = obtener_pagina_activa(e)

        def borrar(e_borrar):
            nonlocal pg
            pg = obtener_pagina_activa(e_borrar) or pg
            try:
                dao.eliminar(id_p)
                if pg:
                    dialogo.open = False
                    pg.update()
                cargar_datos_tabla(e_borrar)
                mostrar_mensaje(f"✓ Prenda '{nombre}' eliminada con éxito.", e=e_borrar)
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
            content=ft.Text(f"¿Estás seguro de que deseas eliminar '{nombre}'?"),
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
            # PARTE SUPERIOR
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=COLOR_GOLD,
                        icon_size=28,
                        tooltip="Volver al menú de catálogo",
                        on_click=lambda e: on_regresar() if on_regresar else None
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "CONTROL DE PRENDAS E INVENTARIO",
                                font_family=FOND_BRAND,
                                size=22,
                                color=COLOR_GOLD,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Gestión y registro de prendas",
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

            # REGISTRO Y EDICIÓN
            ft.Container(
                bgcolor=COLOR_BG_CARD,
                padding=20,
                border_radius=10,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Column(
                    controls=[
                        ft.Text("Registrar / Editar Prenda", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                        ft.Row(controls=[txt_nombre, dd_tipo], spacing=15),
                        ft.Row(
                            controls=[
                                txt_talla,
                                txt_color,
                                txt_precio,
                                txt_stock,
                            ],
                            spacing=15
                        ),
                        ft.Row(
                            controls=[
                                btn_guardar,
                                btn_cancelar_edicion,
                                lbl_mensaje
                            ],
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
                                        ft.Text("Lista de Prendas Registradas", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=10
                                ),
                                ft.Divider(color=COLOR_BORDER, height=5),
                                txt_buscar,
                                row_filtros,
                                ft.Divider(color=COLOR_BORDER, height=5),
                                ft.Row(
                                    controls=[tabla_inventario],
                                    scroll=ft.ScrollMode.AUTO
                                )
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

   
    vista_principal.refrescar = cargar_datos_tabla

    return vista_principal