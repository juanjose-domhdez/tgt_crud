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
import dao.accesorio_dao as accesorio_dao
from dao.accesorio_dao import listar, insertar, eliminar, actualizar, esta_en_pedidos
from models.accesorio import Accesorio


def CatalogoView(page: ft.Page, on_regresar=None):

    # MODO EDICION
    accesorio_editando = {"id": None}
    
    # FILTRADO
    datos_completos = []
    categoria_seleccionada = {"valor": "Todos"}

    # CAMPOS DEL FORMULARIO (FONDO)
    txt_nombre = ft.TextField(
        label="Nombre del Accesorio", 
        border_color=COLOR_BORDER, 
        color=COLOR_TEXT_PRIMARY, 
        expand=True
    )
    txt_tipo = ft.TextField(
        label="Tipo / Categoría", 
        border_color=COLOR_BORDER, 
        color=COLOR_TEXT_PRIMARY, 
        expand=True
    )
    txt_precio = ft.TextField(
        label="Precio Unitario ($)", 
        border_color=COLOR_BORDER, 
        color=COLOR_TEXT_PRIMARY, 
        keyboard_type=ft.KeyboardType.NUMBER,
        width=150
    )
    txt_stock = ft.TextField(
        label="Stock / Restock", 
        value="1",
        border_color=COLOR_BORDER, 
        color=COLOR_TEXT_PRIMARY, 
        keyboard_type=ft.KeyboardType.NUMBER,
        width=130
    )

    # BUSCADOR DE CATEGORIAS
    txt_buscar = ft.TextField(
        hint_text="Buscar accesorio por nombre o tipo...",
        prefix_icon=ft.Icons.SEARCH,
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        content_padding=10,
        height=42,
        expand=True,
        on_change=lambda e: filtrar_tabla()
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

    def mostrar_mensaje(texto, es_error=False):
        lbl_mensaje.value = texto
        lbl_mensaje.color = ft.Colors.RED_400 if es_error else COLOR_GOLD
        lbl_mensaje.visible = True
        try:
            page.update()
        except Exception:
            pass

    def ocultar_mensaje():
        lbl_mensaje.visible = False

    def cancelar_edicion(e=None):
        accesorio_editando["id"] = None
        txt_nombre.value = ""
        txt_tipo.value = ""
        txt_precio.value = ""
        txt_stock.value = "1"
        btn_guardar.text = "Guardar Accesorio"
        btn_guardar.icon = ft.Icons.SAVE
        btn_cancelar_edicion.visible = False
        ocultar_mensaje()
        try:
            page.update()
        except Exception:
            pass

    # GUARDAR / ACTUALIZAR ACCESORIOS
    def guardar_accesorio(e):
        nombre = txt_nombre.value.strip() if txt_nombre.value else ""
        tipo = txt_tipo.value.strip() if txt_tipo.value else ""
        precio_raw = txt_precio.value.strip() if txt_precio.value else ""
        stock_raw = txt_stock.value.strip() if txt_stock.value else "0"
        
        precio_raw = precio_raw.replace("$", "").replace(",", "")

        if not nombre or not precio_raw:
            mostrar_mensaje("Ingresa un nombre y precio válidos.", es_error=True)
            return

        try:
            precio = float(precio_raw)
            stock = int(stock_raw)

            if accesorio_editando["id"] is None:
                try:
                    nuevo_accesorio = Accesorio(nombre=nombre, tipo=tipo, precio=precio, stock=stock)
                except TypeError:
                    nuevo_accesorio = Accesorio(nombre=nombre, tipo=tipo, precio=precio)
                
                insertar(nuevo_accesorio)
                msg = f"✓ Accesorio '{nombre}' guardado con éxito."
            else:
                try:
                    acc_actualizado = Accesorio(
                        id_accesorio=accesorio_editando["id"],
                        nombre=nombre,
                        tipo=tipo,
                        precio=precio,
                        stock=stock
                    )
                except TypeError:
                    acc_actualizado = Accesorio(
                        id_accesorio=accesorio_editando["id"],
                        nombre=nombre,
                        tipo=tipo,
                        precio=precio
                    )

                actualizar(acc_actualizado)
                msg = f"✓ Accesorio '{nombre}' actualizado con éxito."

            cancelar_edicion()
            cargar_datos_tabla()
            mostrar_mensaje(msg)

        except ValueError:
            mostrar_mensaje("Verifica que el precio y stock sean números válidos.", es_error=True)
        except Exception as ex:
            mostrar_mensaje(f"Error al guardar: {ex}", es_error=True)

    # BOTONES PARA EDICION DE ACCESORIOS
    btn_guardar = ft.ElevatedButton(
        "Guardar Accesorio",
        icon=ft.Icons.SAVE,
        bgcolor=COLOR_GOLD,
        color=COLOR_BG_DARK,
        on_click=guardar_accesorio
    )

    btn_cancelar_edicion = ft.OutlinedButton(
        "Cancelar Edición",
        icon=ft.Icons.CANCEL,
        icon_color=ft.Colors.RED_400,
        visible=False,
        on_click=cancelar_edicion
    )

    def cargar_en_formulario(id_acc, nombre, tipo, precio, stock=1):
        ocultar_mensaje()
        accesorio_editando["id"] = id_acc
        txt_nombre.value = nombre
        txt_tipo.value = tipo
        txt_precio.value = str(precio)
        txt_stock.value = str(stock)
        
        btn_guardar.text = "Actualizar Accesorio"
        btn_guardar.icon = ft.Icons.EDIT
        btn_cancelar_edicion.visible = True
        try:
            page.update()
        except Exception:
            pass

    # TABLA Y FILTROS POR CATEGORIA
    tabla_inventario = ft.DataTable(
        border=ft.Border.all(1, COLOR_BORDER),
        border_radius=8,
        heading_row_color=COLOR_BG_CARD,
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text("ID", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Accesorio", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Tipo", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Precio", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Stock", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
        ],
        rows=[]
    )

    def seleccionar_filtro_categoria(categoria):
        categoria_seleccionada["valor"] = categoria
        for btn in row_filtros.controls:
            if btn.data == categoria:
                btn.bgcolor = COLOR_GOLD
                btn.color = COLOR_BG_DARK
            else:
                btn.bgcolor = COLOR_BG_DARK
                btn.color = COLOR_TEXT_SECONDARY
        filtrar_tabla()

    categorias_filtro = ["Todos", "Corbata", "Moño", "Cinturón", "Pañuelo"]
    
    row_filtros = ft.Row(
        controls=[
            ft.ElevatedButton(
                cat,
                data=cat,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                ),
                bgcolor=COLOR_GOLD if cat == "Todos" else COLOR_BG_DARK,
                color=COLOR_BG_DARK if cat == "Todos" else COLOR_TEXT_SECONDARY,
                on_click=lambda e, c=cat: seleccionar_filtro_categoria(c)
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
                    ft.Icon(ft.Icons.INVENTORY_2, color=COLOR_GOLD, size=32),
                    ft.Column([
                        ft.Text("Total de Accesorios", size=13, color=COLOR_TEXT_SECONDARY),
                        ft.Text(f"{total_items} tipos registrados", size=18, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                    ], spacing=2)
                ])
            ),
        ])

    def extraer_datos_item(item):
        if isinstance(item, (list, tuple)):
            id_acc = item[0] if len(item) > 0 else ""
            nombre = item[1] if len(item) > 1 and item[1] is not None else ""
            tipo = item[2] if len(item) > 2 and item[2] is not None else ""
            try:
                precio = float(item[3]) if len(item) > 3 and item[3] is not None else 0.0
            except (ValueError, TypeError):
                precio = 0.0
            try:
                stock = int(item[4]) if len(item) > 4 and item[4] is not None else 1
            except (ValueError, TypeError):
                stock = 1
            return id_acc, str(nombre), str(tipo), precio, stock

        if hasattr(item, "id_accesorio") or hasattr(item, "nombre"):
            id_acc = getattr(item, "id_accesorio", getattr(item, "id", ""))
            nombre = getattr(item, "nombre", "")
            tipo = getattr(item, "tipo", "") or ""
            precio = getattr(item, "precio", 0.0) or 0.0
            stock = getattr(item, "stock", 1) or 1
            return id_acc, str(nombre), str(tipo), float(precio), int(stock)

        if isinstance(item, dict):
            id_acc = item.get("id_accesorio", item.get("id", ""))
            nombre = item.get("nombre", "")
            tipo = item.get("tipo", "")
            precio = float(item.get("precio", 0.0))
            stock = int(item.get("stock", 1))
            return id_acc, str(nombre), str(tipo), precio, stock

        return "", str(item), "", 0.0, 1

    #ELIMINAR ACCESORIO CON VALIDACIÓN DE PEDIDOS
    def confirmar_eliminar(id_p, nombre):
        en_uso = esta_en_pedidos(id_p)

        def inhabilitar_registro(e_accion):
            try:
                #NO USO = ELIMINAR
                eliminar(id_p)
                dialogo.open = False
                page.update()
                cargar_datos_tabla()
                mostrar_mensaje(f"✓ Accesorio '{nombre}' inhabilitado correctamente.")
            except Exception as ex:
                dialogo.open = False
                page.update()
                mostrar_mensaje(f"Error al procesar: {ex}", es_error=True)

        def cerrar_dialogo(e_canc):
            dialogo.open = False
            page.update()

        #REUTILIZAR LA VENTANA
        if en_uso:
            dialogo = ft.AlertDialog(
                title=ft.Row([
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER_400, size=28),
                    ft.Text("No se puede eliminar", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)
                ], spacing=10),
                content=ft.Text(
                    f"El accesorio '{nombre}' está registrado en uno o más pedidos activos.\n\n"
                    "Para proteger el historial de ventas y la integridad de la base de datos, no es posible borrarlo.",
                    color=COLOR_BG_DARK
                ),
                actions=[
                    ft.ElevatedButton(
                        "Entendido", 
                        bgcolor=COLOR_GOLD, 
                        color=COLOR_BG_DARK, 
                        on_click=cerrar_dialogo
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
        else:
            dialogo = ft.AlertDialog(
                title=ft.Text("Confirmar Inhabilitación", color=COLOR_GOLD, weight=ft.FontWeight.BOLD),
                content=ft.Text(f"¿Deseas inhabilitar '{nombre}'? Dejará de mostrarse en el catálogo activo."),
                actions=[
                    ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                    ft.ElevatedButton("Inhabilitar", bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE, on_click=inhabilitar_registro),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def filtrar_tabla():
        tabla_inventario.rows.clear()
        busqueda = txt_buscar.value.strip().lower() if txt_buscar.value else ""
        cat_filtro = categoria_seleccionada["valor"]

        for item in datos_completos:
            id_acc, nombre, tipo, precio, stock = extraer_datos_item(item)

            coincide_texto = (busqueda in nombre.lower()) or (busqueda in tipo.lower())
            coincide_cat = (cat_filtro == "Todos") or (cat_filtro.lower() == tipo.lower())

            if coincide_texto and coincide_cat:
                tabla_inventario.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(id_acc), color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(nombre, color=COLOR_TEXT_PRIMARY)),
                            ft.DataCell(ft.Text(tipo if tipo else "Sin categoría", color=COLOR_TEXT_SECONDARY)),
                            ft.DataCell(ft.Text(f"${precio:.2f}", color=COLOR_GOLD, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(f"{stock} pzas", color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                                    bgcolor=COLOR_BG_DARK,
                                    padding=6,
                                    border_radius=4
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT_OUTLINED,
                                            icon_color=COLOR_GOLD,
                                            tooltip="Editar Accesorio",
                                            on_click=lambda e, i=id_acc, n=nombre, t=tipo, p=precio, s=stock: cargar_en_formulario(i, n, t, p, s)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE,
                                            icon_color=ft.Colors.RED_400,
                                            tooltip="Eliminar Accesorio",
                                            on_click=lambda e, i=id_acc, n=nombre: confirmar_eliminar(i, n)
                                        ),
                                    ],
                                    spacing=0
                                )
                            ),
                        ]
                    )
                )

        try:
            page.update()
        except Exception:
            pass

    def cargar_datos_tabla():
        nonlocal datos_completos
        try:
            datos_completos = listar()
            if datos_completos is None:
                datos_completos = []
        except Exception as ex:
            print(f"❌ Error al llamar listar(): {ex}")
            datos_completos = []

        actualizar_metricas()
        filtrar_tabla()

    # VISTA PRINCIPAL
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
                        on_click=lambda _: on_regresar() if on_regresar else None
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "CONTROL DE ACCESORIOS E INVENTARIO",
                                font_family=FOND_BRAND,
                                size=22,
                                color=COLOR_GOLD,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Gestión y registro de accesorios",
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

            # FORMULARIO DE FONDO
            ft.Container(
                bgcolor=COLOR_BG_CARD,
                padding=20,
                border_radius=10,
                border=ft.Border.all(1, COLOR_BORDER),
                content=ft.Column(
                    controls=[
                        ft.Text("Registrar / Editar Accesorio", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                        ft.Row(controls=[txt_nombre, txt_tipo], spacing=15),
                        ft.Row(
                            controls=[
                                txt_precio,
                                txt_stock,
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

            #SECCIÓN INFERIOR
            ft.Row(
                controls=[
                    #COLUMNA IZQUIERDA - BUSCADOR + FILTROS
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
                                        ft.Text("Lista de Accesorios Registrados", size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
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

                    #COLUMNA - TOTAL DE ACCESORIOS
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

    cargar_datos_tabla()

    return vista_principal