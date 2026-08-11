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

from dao.pedido_dao import PedidoDAO
from models.pedido import Pedido
from dao.prenda_dao import PrendaDAO
from models.prenda import Prenda
from dao.detalle_accesorio_dao import DetalleAccesorioDAO
from models.detalle_accesorio import DetalleAccesorio


def RegistroPedidoView(on_regresar=None, on_guardar_exito=None, page=None, **kwargs):
    COLOR_DANGER = "#EF4444"
    COLOR_SUCCESS = "#22C55E"

    ALTURA_CAMPO = 55
    PADDING_CAMPO = ft.Padding.symmetric(horizontal=12, vertical=14)


    opciones_clientes = []
    mapa_clientes = {}
    opciones_empleados = []
    lista_prendas_catalogo = []
    lista_accesorios_catalogo = []

    # Cargar Clientes
    try:
        from dao.clientes_dao import ClienteDAO
        clientes_db = ClienteDAO.seleccionar()
        for c in clientes_db:
            c_id_str = str(c.id_cliente)
            mapa_clientes[c_id_str] = c
            opciones_clientes.append(
                ft.dropdown.Option(
                    key=c_id_str, 
                    text=c.nombre_completo,
                    style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)
                )
            )
    except Exception as err:
        print(f"❌ Error cargando clientes desde BD: {err}")

    # Cargar Empleados
    try:
        from dao.empleado_dao import EmpleadoDAO
        empleados_db = EmpleadoDAO.seleccionar()
        for emp in empleados_db:
            opciones_empleados.append(
                ft.dropdown.Option(
                    key=str(emp.id_empleado), 
                    text=emp.nombre,
                    style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)
                )
            )
    except Exception as err:
        print(f"❌ Error cargando empleados desde BD: {err}")

    # Cargar Prendas (catálogo)
    try:
        prendas_db = PrendaDAO.seleccionar()
        for p in prendas_db:
            p_key = f"prenda_{p.id_prenda}"
            p_nombre = f"{p.tipo_prenda} ({p.modelo})" if getattr(p, "modelo", None) else p.tipo_prenda
            p_precio = float(p.precio) if p.precio else 0.0
            p_talla = getattr(p, "talla", "N/A")
            p_color = getattr(p, "color", "N/A")
            p_stock = int(getattr(p, "stock", 0) or 0)

            lista_prendas_catalogo.append({
                "key": p_key,
                "id_real": p.id_prenda,
                "nombre": str(p_nombre),
                "precio": p_precio,
                "tipo": "prenda",
                "label": f"[Prenda] {p_nombre} - Color: {p_color} - Talla: {p_talla} - Stock: {p_stock} - ${p_precio:,.2f}",
                "tipo_prenda": p.tipo_prenda,
                "modelo": getattr(p, "modelo", None),
                "talla": p_talla,
                "color": p_color,
                "stock": p_stock,
            })
    except Exception as err:
        print(f"❌ Error cargando prendas desde BD: {err}")

    # Cargar Accesorios (catálogo)
    try:
        import dao.accesorio_dao as accesorio_dao
        accesorios_db = accesorio_dao.listar()
        for a in accesorios_db:
            a_id = a[0]
            a_nombre = a[1]
            a_tipo = a[2] if len(a) > 2 and a[2] else "Accesorio"
            a_precio = float(a[3]) if len(a) > 3 and a[3] else 0.0
            a_stock = int(a[4]) if len(a) > 4 and a[4] is not None else 0
            a_key = f"accesorio_{a_id}"

            lista_accesorios_catalogo.append({
                "key": a_key,
                "id_real": a_id,
                "nombre": str(a_nombre),
                "precio": a_precio,
                "tipo": "accesorio",
                "label": f"[Accesorio] {a_nombre} - Stock: {a_stock} - ${a_precio:,.2f}",
                "tipo_accesorio": a_tipo,
                "stock": a_stock,
            })
    except Exception as err:
        print(f"❌ Error cargando accesorios desde BD: {err}")

    #CONTROLES DE CLIENTE, EMPLEADO Y FECHAS
    input_telefono = ft.TextField(
        label="Teléfono",
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        read_only=False,
        max_length=10,
        keyboard_type=ft.KeyboardType.PHONE,
        input_filter=ft.NumbersOnlyInputFilter(),
        expand=True,
        height=ALTURA_CAMPO,
        content_padding=PADDING_CAMPO,
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )

    def al_seleccionar_cliente(e):
        cliente_id = input_cliente.value
        if cliente_id in mapa_clientes:
            cliente = mapa_clientes[cliente_id]
            tel = getattr(cliente, "telefono", None) or getattr(cliente, "num_telefono", "") or ""
            tel_filtrado = "".join(filter(str.isdigit, str(tel)))[:10]
            input_telefono.value = tel_filtrado
            try:
                input_telefono.update()
            except Exception:
                pass

    input_cliente = ft.Dropdown(
        label="Cliente",
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        hint_text="Selecciona un cliente",
        hint_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        options=opciones_clientes,
        expand=True,
        height=ALTURA_CAMPO,
        content_padding=PADDING_CAMPO,
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )
    input_cliente.on_change = al_seleccionar_cliente

    input_empleado = ft.Dropdown(
        label="Empleado que atiende",
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        hint_text="Selecciona un empleado",
        hint_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        options=opciones_empleados,
        expand=True,
        height=ALTURA_CAMPO,
        content_padding=PADDING_CAMPO,
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )
    if len(opciones_empleados) == 1:
        input_empleado.value = opciones_empleados[0].key

    fecha_actual_str = datetime.now().strftime("%d/%m/%Y")
    input_fecha_pedido = ft.TextField(
        label="Fecha Pedido",
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        value=fecha_actual_str,
        read_only=True,
        width=160,
        height=ALTURA_CAMPO,
        content_padding=PADDING_CAMPO,
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )
    input_fecha_entrega = ft.TextField(
        label="Fecha Entrega",
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        hint_text="DD/MM/AAAA",
        hint_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        width=160,
        height=ALTURA_CAMPO,
        content_padding=PADDING_CAMPO,
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )

    #SECCIÓN CATÁLOGO Y SELECCIÓN 
    columna_items_pedido = ft.Column(spacing=8)
    items_agregados_data = []

    item_seleccionado_temporal = {"item": None}

    txt_item_seleccionado_info = ft.Text(
        "Ningún artículo seleccionado", color=COLOR_TEXT_SECONDARY, style=ft.TextStyle(font_family=FONT_BODY), expand=True,
    )

    input_cantidad = ft.TextField(
        label="Cantidad",
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        value="1",
        width=120,
        height=ALTURA_CAMPO,
        content_padding=PADDING_CAMPO,
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )

    def agregar_item_oficial(e):
        prod_data = item_seleccionado_temporal["item"]
        if not prod_data:
            return

        cant_str = input_cantidad.value
        cant = int(cant_str) if cant_str and cant_str.isdigit() and int(cant_str) > 0 else 1

        if cant > prod_data["stock"]:
            txt_item_seleccionado_info.value = f"❌ Stock insuficiente. Disponibles: {prod_data['stock']}"
            txt_item_seleccionado_info.color = COLOR_DANGER
            try:
                txt_item_seleccionado_info.update()
            except Exception:
                pass
            return

        prod_nombre = prod_data["nombre"]
        prod_precio = prod_data["precio"]
        subtotal = prod_precio * cant

        item_dict = {
            "id_item": prod_data["id_real"],
            "tipo": prod_data["tipo"],
            "nombre": prod_nombre,
            "cantidad": cant,
            "precio_unitario": prod_precio,
            "subtotal": subtotal,
            "tipo_prenda": prod_data.get("tipo_prenda"),
            "modelo": prod_data.get("modelo"),
            "talla": prod_data.get("talla"),
            "color": prod_data.get("color"),
            "objeto_original": prod_data,
        }
        items_agregados_data.append(item_dict)

        # Descontar stock localmente para vista previa inmediata (NO FUNCIONA)
        prod_data["stock"] -= cant
        if prod_data["tipo"] == "prenda":
            p_color = prod_data.get('color', 'N/A')
            prod_data["label"] = f"[Prenda] {prod_nombre} - Color: {p_color} - Talla: {prod_data.get('talla', 'N/A')} - Stock: {prod_data['stock']} - ${prod_precio:,.2f}"
        else:
            prod_data["label"] = f"[Accesorio] {prod_nombre} - Stock: {prod_data['stock']} - ${prod_precio:,.2f}"

        fila_item = None
        def eliminar_item(evt):
            items_agregados_data.remove(item_dict)
            prod_data["stock"] += cant
            if prod_data["tipo"] == "prenda":
                p_color = prod_data.get('color', 'N/A')
                prod_data["label"] = f"[Prenda] {prod_nombre} - Color: {p_color} - Talla: {prod_data.get('talla', 'N/A')} - Stock: {prod_data['stock']} - ${prod_precio:,.2f}"
            else:
                prod_data["label"] = f"[Accesorio] {prod_nombre} - Stock: {prod_data['stock']} - ${prod_precio:,.2f}"

            columna_items_pedido.controls.remove(fila_item)
            columna_items_pedido.update()
            recalcular_total_automatico()

        btn_eliminar = ft.Container(
            content=ft.Text("❌ Quitar", color=COLOR_DANGER, size=12, weight=ft.FontWeight.BOLD),
            padding=6,
            border=ft.Border.all(1, COLOR_DANGER),
            border_radius=5,
            ink=True,
            on_click=eliminar_item,
        )

        fila_item = ft.Container(
            content=ft.Row(
                [
                    ft.Text("✔", color=COLOR_GOLD, size=16),
                    ft.Text(
                        f"[{item_dict['tipo'].capitalize()}] {prod_nombre}",
                        weight=ft.FontWeight.W_500, expand=True,
                        style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
                    ),
                    ft.Text(
                        f"Cant: {cant}", weight=ft.FontWeight.BOLD,
                        style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_SECONDARY),
                    ),
                    ft.Text(
                        f"${subtotal:,.2f}", weight=ft.FontWeight.BOLD,
                        style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_GOLD),
                    ),
                    btn_eliminar,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=10,
            border=ft.Border.all(1, COLOR_BORDER),
            border_radius=8,
            bgcolor=COLOR_BG_CARD,
        )

        columna_items_pedido.controls.append(fila_item)
        columna_items_pedido.update()

        item_seleccionado_temporal["item"] = None
        txt_item_seleccionado_info.value = "Ningún artículo seleccionado"
        txt_item_seleccionado_info.color = COLOR_TEXT_SECONDARY
        input_cantidad.value = "1"
        try:
            txt_item_seleccionado_info.update()
            input_cantidad.update()
        except Exception:
            pass

        recalcular_total_automatico()

    #PRENDAS
    columna_resultados_prendas = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)

    def abrir_dialogo_prendas(e):
        dialogo_p = ft.AlertDialog()

        def filtrar_prendas(filtro):
            columna_resultados_prendas.controls.clear()
            for p in lista_prendas_catalogo:
                if filtro and filtro != "Todos":
                    t_prenda = str(p.get("tipo_prenda", "")).lower()
                    if filtro.lower() not in t_prenda:
                        continue

                def seleccionar_esta_prenda(evt, prod=p):
                    item_seleccionado_temporal["item"] = prod
                    p_color_str = prod.get('color', 'N/A')
                    txt_item_seleccionado_info.value = f"Seleccionado: [Prenda] {prod['nombre']} - Color: {p_color_str} - Talla: {prod.get('talla', 'N/A')} - Stock: {prod['stock']} - ${prod['precio']:,.2f}"
                    txt_item_seleccionado_info.color = COLOR_TEXT_PRIMARY
                    try:
                        txt_item_seleccionado_info.update()
                    except Exception:
                        pass
                    dialogo_p.open = False
                    page.update()

                fila = ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(p["label"], color=COLOR_TEXT_PRIMARY, style=ft.TextStyle(font_family=FONT_BODY), expand=True),
                            ft.OutlinedButton(
                                "Seleccionar",
                                style=ft.ButtonStyle(
                                    color=COLOR_TEXT_PRIMARY, 
                                    side=ft.BorderSide(1, COLOR_BORDER)
                                ),
                                on_click=seleccionar_esta_prenda,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=10,
                    border_radius=6,
                    bgcolor=COLOR_BG_DARK,
                    border=ft.Border.all(1, COLOR_BORDER),
                )
                columna_resultados_prendas.controls.append(fila)
            try:
                columna_resultados_prendas.update()
            except Exception:
                pass

        def btn_f(f_nombre):
            return ft.ElevatedButton(
                f_nombre,
                style=ft.ButtonStyle(bgcolor=COLOR_BG_CARD, color=COLOR_TEXT_PRIMARY),
                on_click=lambda evt: filtrar_prendas(f_nombre),
            )

        row_filtros_p = ft.Row(
            [
                btn_f("Todos"),
                btn_f("Chaleco"),
                btn_f("Pantalón"),
                btn_f("Saco"),
                btn_f("Camisa"),
                btn_f("Traje Completo"),
            ],
            wrap=True,
            spacing=8,
        )
        filtrar_prendas("Todos")

        dialogo_p.title = ft.Text("Filtrar y Seleccionar Prenda", color=COLOR_GOLD, style=ft.TextStyle(font_family=FOND_BRAND))
        dialogo_p.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Filtra por tipo de prenda:", size=12, color=COLOR_TEXT_SECONDARY, style=ft.TextStyle(font_family=FONT_BODY)),
                    row_filtros_p,
                    ft.Divider(color=COLOR_BORDER),
                    ft.Container(content=columna_resultados_prendas, height=300, width=540),
                ],
                spacing=10,
            ),
            bgcolor=COLOR_BG_CARD,
        )
        dialogo_p.bgcolor = COLOR_BG_CARD
        dialogo_p.actions = [ft.TextButton("Cerrar", on_click=lambda evt: setattr(dialogo_p, 'open', False) or page.update())]

        if page:
            page.overlay.append(dialogo_p)
            dialogo_p.open = True
            page.update()

    # ACCESORIOS
    columna_resultados_accesorios = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)

    def abrir_dialogo_accesorios(e):
        dialogo_a = ft.AlertDialog()

        def filtrar_accesorios(filtro):
            columna_resultados_accesorios.controls.clear()
            for a in lista_accesorios_catalogo:
                if filtro and filtro != "Todos":
                    t_acc = str(a.get("tipo_accesorio", "")).lower()
                    if filtro.lower() not in t_acc:
                        continue

                def seleccionar_este_accesorio(evt, prod=a):
                    item_seleccionado_temporal["item"] = prod
                    txt_item_seleccionado_info.value = f"Seleccionado: {prod['label']}"
                    txt_item_seleccionado_info.color = COLOR_TEXT_PRIMARY
                    try:
                        txt_item_seleccionado_info.update()
                    except Exception:
                        pass
                    dialogo_a.open = False
                    page.update()

                fila = ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(a["label"], color=COLOR_TEXT_PRIMARY, style=ft.TextStyle(font_family=FONT_BODY), expand=True),
                            ft.OutlinedButton(
                                "Seleccionar",
                                style=ft.ButtonStyle(
                                    color=COLOR_TEXT_PRIMARY, 
                                    side=ft.BorderSide(1, COLOR_BORDER)
                                ),
                                on_click=seleccionar_este_accesorio,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=10,
                    border_radius=6,
                    bgcolor=COLOR_BG_DARK,
                    border=ft.Border.all(1, COLOR_BORDER),
                )
                columna_resultados_accesorios.controls.append(fila)
            try:
                columna_resultados_accesorios.update()
            except Exception:
                pass

        def btn_fa(f_nombre):
            return ft.ElevatedButton(
                f_nombre,
                style=ft.ButtonStyle(bgcolor=COLOR_BG_CARD, color=COLOR_TEXT_PRIMARY),
                on_click=lambda evt: filtrar_accesorios(f_nombre),
            )

        row_filtros_a = ft.Row(
            [
                btn_fa("Todos"),
                btn_fa("Corbata"),
                btn_fa("Moño"),
                btn_fa("Cinturón"),
                btn_fa("Pañuelo"),
            ],
            wrap=True,
            spacing=8,
        )
        filtrar_accesorios("Todos")

        dialogo_a.title = ft.Text("Filtrar y Seleccionar Accesorio", color=COLOR_GOLD, style=ft.TextStyle(font_family=FOND_BRAND))
        dialogo_a.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Filtra por tipo de accesorio:", size=12, color=COLOR_TEXT_SECONDARY, style=ft.TextStyle(font_family=FONT_BODY)),
                    row_filtros_a,
                    ft.Divider(color=COLOR_BORDER),
                    ft.Container(content=columna_resultados_accesorios, height=300, width=540),
                ],
                spacing=10,
            ),
            bgcolor=COLOR_BG_CARD,
        )
        dialogo_a.bgcolor = COLOR_BG_CARD
        dialogo_a.actions = [ft.TextButton("Cerrar", on_click=lambda evt: setattr(dialogo_a, 'open', False) or page.update())]

        if page:
            page.overlay.append(dialogo_a)
            dialogo_a.open = True
            page.update()

    input_prenda_dropdown = ft.Container(
        content=ft.Row(
            [
                ft.Text("Abrir catálogo de prendas...", color=COLOR_TEXT_SECONDARY, style=ft.TextStyle(font_family=FONT_BODY), expand=True),
                ft.OutlinedButton(
                    "Buscar Prenda",
                    style=ft.ButtonStyle(color=COLOR_TEXT_PRIMARY, side=ft.BorderSide(1, COLOR_BORDER)),
                    on_click=abrir_dialogo_prendas,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=12,
        height=ALTURA_CAMPO,
        bgcolor=COLOR_BG_CARD,
        border=ft.Border.all(1, COLOR_BORDER),
        border_radius=8,
        expand=True,
    )

    input_accesorio_dropdown = ft.Container(
        content=ft.Row(
            [
                ft.Text("Abrir catálogo de accesorios...", color=COLOR_TEXT_SECONDARY, style=ft.TextStyle(font_family=FONT_BODY), expand=True),
                ft.OutlinedButton(
                    "Buscar Accesorio",
                    style=ft.ButtonStyle(color=COLOR_TEXT_PRIMARY, side=ft.BorderSide(1, COLOR_BORDER)),
                    on_click=abrir_dialogo_accesorios,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=12,
        height=ALTURA_CAMPO,
        bgcolor=COLOR_BG_CARD,
        border=ft.Border.all(1, COLOR_BORDER),
        border_radius=8,
        expand=True,
    )

    # COSTOS Y CÁLCULOS
    txt_restante = ft.Text(
        "Restante: $0.00", size=18, weight=ft.FontWeight.BOLD, color=COLOR_GOLD,
        style=ft.TextStyle(font_family=FOND_BRAND),
    )

    def calcular_costos(e=None):
        try:
            total = float(input_precio_total.value) if input_precio_total.value else 0.0
            anticipo = float(input_anticipo.value) if input_anticipo.value else 0.0
            restante = total - anticipo
            txt_restante.value = f"Restante: ${restante:,.2f}"
            txt_restante.color = COLOR_DANGER if restante < 0 else COLOR_GOLD
        except ValueError:
            txt_restante.value = "Restante: $0.00"
        try:
            txt_restante.update()
        except Exception:
            pass

    def recalcular_total_automatico():
        suma_total = sum(item["subtotal"] for item in items_agregados_data)
        input_precio_total.value = f"{suma_total:.2f}"
        try:
            input_precio_total.update()
        except Exception:
            pass
        calcular_costos()

    input_precio_total = ft.TextField(
        label="Precio Total ($)",
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        value="0.00",
        read_only=True,
        width=180,
        height=ALTURA_CAMPO,
        content_padding=PADDING_CAMPO,
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )
    input_precio_total.on_change = calcular_costos

    input_anticipo = ft.TextField(
        label="Anticipo ($)",
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        value="0.00",
        width=180,
        height=ALTURA_CAMPO,
        content_padding=PADDING_CAMPO,
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )
    input_anticipo.on_change = calcular_costos

    input_estado = ft.Dropdown(
        label="Estado del Pedido",
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        value="Pendiente",
        options=[
            ft.dropdown.Option("Pendiente", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
            ft.dropdown.Option("En Proceso", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
            ft.dropdown.Option("En Confección", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
            ft.dropdown.Option("Terminado", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
            ft.dropdown.Option("Entregado", style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY)),
        ],
        width=220,
        height=ALTURA_CAMPO,
        content_padding=PADDING_CAMPO,
        bgcolor=COLOR_BG_CARD,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        color=COLOR_TEXT_PRIMARY,
        text_style=ft.TextStyle(font_family=FONT_BODY, color=COLOR_TEXT_PRIMARY),
    )

    txt_mensaje_guardado = ft.Text(
        "", color=COLOR_SUCCESS, weight=ft.FontWeight.BOLD, size=14,
        style=ft.TextStyle(font_family=FONT_BODY),
    )

    #FUNCIÓN PARA REFRESCAR
    def limpiar_formulario_completo():
        input_cliente.value = None
        input_telefono.value = ""
        if len(opciones_empleados) == 1:
            input_empleado.value = opciones_empleados[0].key
        else:
            input_empleado.value = None
        input_fecha_pedido.value = datetime.now().strftime("%d/%m/%Y")
        input_fecha_entrega.value = ""

        items_agregados_data.clear()
        columna_items_pedido.controls.clear()
        
        item_seleccionado_temporal["item"] = None
        txt_item_seleccionado_info.value = "Ningún artículo seleccionado"
        txt_item_seleccionado_info.color = COLOR_TEXT_SECONDARY
        input_cantidad.value = "1"
        
        input_precio_total.value = "0.00"
        input_anticipo.value = "0.00"
        txt_restante.value = "Restante: $0.00"
        txt_restante.color = COLOR_GOLD
        input_estado.value = "Pendiente"

        try:
            input_cliente.update()
            input_telefono.update()
            input_empleado.update()
            input_fecha_pedido.update()
            input_fecha_entrega.update()
            columna_items_pedido.update()
            txt_item_seleccionado_info.update()
            input_cantidad.update()
            input_precio_total.update()
            input_anticipo.update()
            txt_restante.update()
            input_estado.update()
        except Exception:
            pass

    #GUARDADO EN BASE DE DATOS Y DESCUENTO DE STOCK REAL (AUN NO FUNCIONA)
    def mostrar_error(texto):
        txt_mensaje_guardado.value = f"❌ {texto}"
        txt_mensaje_guardado.color = COLOR_DANGER
        txt_mensaje_guardado.update()

    def guardar_pedido_click(e):
        if not input_cliente.value:
            mostrar_error("Selecciona un cliente primero")
            return
        if not input_empleado.value:
            mostrar_error("Selecciona el empleado que atiende")
            return
        if not items_agregados_data:
            mostrar_error("Agrega al menos un producto")
            return
        if not input_fecha_entrega.value:
            mostrar_error("Indica la fecha de entrega")
            return

        try:
            fecha_pedido_dt = datetime.strptime(input_fecha_pedido.value, "%d/%m/%Y").date()
        except ValueError:
            mostrar_error("La fecha de pedido no es válida")
            return

        try:
            fecha_entrega_dt = datetime.strptime(input_fecha_entrega.value.strip(), "%d/%m/%Y").date()
        except ValueError:
            mostrar_error("La fecha de entrega debe tener formato DD/MM/AAAA")
            return

        estado_actual = input_estado.value

        pedido = Pedido(
            id_cliente=int(input_cliente.value),
            id_empleado=int(input_empleado.value),
            fecha_pedido=fecha_pedido_dt,
            fecha_entrega=fecha_entrega_dt,
            anticipo=float(input_anticipo.value or 0),
            total=float(input_precio_total.value or 0),
            estado=estado_actual,
        )

        try:
            nuevo_id_pedido = PedidoDAO.insertar(pedido)
        except Exception as ex:
            print(f"❌ Error al guardar el pedido: {ex}")
            mostrar_error("No se pudo guardar el pedido, revisa la consola")
            return

        errores_detalle = []

        for item in items_agregados_data:
            try:
                cantidad_comprada = item["cantidad"]
                prod_original = item["objeto_original"]
                
                # Obtenemos el stock real actual directamente de la base de datos para evitar desincronizaciones
                if item["tipo"] == "prenda":
                    prenda_db_obj = PrendaDAO.obtener_por_id(item["id_item"]) if hasattr(PrendaDAO, "obtener_por_id") else None
                    stock_real_actual = int(getattr(prenda_db_obj, "stock", 0)) if prenda_db_obj else prod_original["stock"] + cantidad_comprada
                else:
                    stock_real_actual = prod_original["stock"] + cantidad_comprada
                    try:
                        accs = accesorio_dao.listar()
                        for ac in accs:
                            if ac[0] == item["id_item"]:
                                stock_real_actual = int(ac[4]) if len(ac) > 4 and ac[4] is not None else 0
                                break
                    except Exception:
                        pass

                # DESCUENTO INMEDIATO
                stock_bd_final = max(0, stock_real_actual - cantidad_comprada)

                if item["tipo"] == "prenda":
                    nueva_prenda = Prenda(
                        id_prenda=item["id_item"],
                        id_pedido=nuevo_id_pedido,
                        tipo_prenda=item["tipo_prenda"],
                        modelo=item["modelo"],
                        talla=item["talla"],
                        color=item["color"],
                        precio=item["precio_unitario"],
                        stock=stock_bd_final,
                    )
                    if hasattr(PrendaDAO, "actualizar_stock"):
                        PrendaDAO.actualizar_stock(item["id_item"], stock_bd_final)
                    elif hasattr(PrendaDAO, "modificar"):
                        PrendaDAO.modificar(nueva_prenda)
                    else:
                        PrendaDAO.insertar(nueva_prenda)
                else:
                    detalle = DetalleAccesorio(
                        id_pedido=nuevo_id_pedido,
                        id_accesorio=item["id_item"],
                        cantidad=cantidad_comprada,
                    )
                    DetalleAccesorioDAO.insertar(detalle)
                    if hasattr(accesorio_dao, "actualizar_stock"):
                        accesorio_dao.actualizar_stock(item["id_item"], stock_bd_final)
            except Exception as ex:
                print(f"❌ Error guardando/actualizando stock de '{item['nombre']}': {ex}")
                errores_detalle.append(item["nombre"])

        if errores_detalle:
            mostrar_error(
                f"Pedido #{nuevo_id_pedido} guardado, pero fallaron: {', '.join(errores_detalle)}"
            )
            return

        # MENSAJE 
        txt_mensaje_guardado.value = f"✅ ¡Pedido #{nuevo_id_pedido} guardado con éxito!"
        txt_mensaje_guardado.color = COLOR_SUCCESS
        txt_mensaje_guardado.update()

        #Limpiamos los datos locales para dejar el formulario listo para el siguiente pedido
        limpiar_formulario_completo()

        if on_guardar_exito:
            on_guardar_exito()

    # RETORNO DE LA VISTA
    return ft.Container(
        content=ft.ListView(
            controls=[
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=COLOR_GOLD,
                            on_click=lambda _: on_regresar() if on_regresar else None,
                            tooltip="Volver",
                        ),
                        ft.Column([
                            ft.Text(
                                "NUEVO PEDIDO", size=22, weight=ft.FontWeight.BOLD, color=COLOR_GOLD,
                                style=ft.TextStyle(font_family=FOND_BRAND),
                            ),
                            ft.Text(
                                "Cliente, productos y costos del pedido", size=12, color=COLOR_TEXT_SECONDARY,
                                style=ft.TextStyle(font_family=FONT_BODY),
                            ),
                        ], spacing=2),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=10),

                # Contenedor 1: Cliente y Empleado
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Información del Cliente", size=16, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY,
                            style=ft.TextStyle(font_family=FOND_BRAND),
                        ),
                        ft.Row(
                            [
                                ft.Container(content=input_cliente, expand=3),
                                ft.Container(content=input_telefono, expand=2),
                            ], 
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        ft.Row([input_empleado], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Row([input_fecha_pedido, input_fecha_entrega], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ], spacing=12),
                    padding=20,
                    border_radius=10,
                    bgcolor=COLOR_BG_CARD,
                    border=ft.Border.all(1, COLOR_BORDER),
                ),
                ft.Container(height=15),

                # Contenedor 2: Productos
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Información de los Artículos", size=16, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY,
                            style=ft.TextStyle(font_family=FOND_BRAND),
                        ),
                        
                        ft.Row([
                            ft.Column([
                                ft.Text("👔 Catálogo de Prendas", color=COLOR_GOLD, weight=ft.FontWeight.BOLD, style=ft.TextStyle(font_family=FONT_BODY)),
                                input_prenda_dropdown,
                            ], expand=1),
                            
                            ft.VerticalDivider(width=20, color=COLOR_BORDER),
                            
                            ft.Column([
                                ft.Text("⌚ Catálogo de Accesorios", color=COLOR_GOLD, weight=ft.FontWeight.BOLD, style=ft.TextStyle(font_family=FONT_BODY)),
                                input_accesorio_dropdown,
                            ], expand=1),
                        ]),
                        
                        # Panel de selección activa, cantidad y botón de añadir
                        ft.Container(
                            content=ft.Row(
                                [
                                    txt_item_seleccionado_info,
                                    input_cantidad,
                                    ft.ElevatedButton(
                                        "Añadir al Pedido",
                                        style=ft.ButtonStyle(bgcolor=COLOR_GOLD, color="#000000"),
                                        on_click=agregar_item_oficial,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=12,
                            border=ft.Border.all(1, COLOR_BORDER),
                            border_radius=8,
                            bgcolor=COLOR_BG_DARK,
                        ),
                        
                        ft.Divider(color=COLOR_BORDER),
                        ft.Text(
                            "Artículos en el pedido:", size=13, weight=ft.FontWeight.W_500, color=COLOR_TEXT_PRIMARY,
                            style=ft.TextStyle(font_family=FONT_BODY),
                        ),
                        columna_items_pedido,
                    ], spacing=12),
                    padding=20,
                    border_radius=10,
                    bgcolor=COLOR_BG_CARD,
                    border=ft.Border.all(1, COLOR_BORDER),
                ),
                ft.Container(height=15),

                # Contenedor 3: Costos y Estado
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Costos y Estado", size=16, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY,
                            style=ft.TextStyle(font_family=FOND_BRAND),
                        ),
                        ft.Row(
                            [input_precio_total, input_anticipo, txt_restante],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Row([input_estado], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ], spacing=12),
                    padding=20,
                    border_radius=10,
                    bgcolor=COLOR_BG_CARD,
                    border=ft.Border.all(1, COLOR_BORDER),
                ),
                ft.Container(height=20),

                ft.Row(
                    [
                        txt_mensaje_guardado,
                        ft.ElevatedButton(
                            "Guardar Pedido",
                            style=ft.ButtonStyle(bgcolor=COLOR_GOLD, color="#000000"),
                            on_click=guardar_pedido_click,
                        ),
                        ft.OutlinedButton(
                            "Cancelar",
                            style=ft.ButtonStyle(color=COLOR_TEXT_PRIMARY),
                            on_click=lambda _: on_regresar() if on_regresar else None,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            padding=20,
            spacing=10,
        ),
        expand=True,
        bgcolor=COLOR_BG_DARK,
    )