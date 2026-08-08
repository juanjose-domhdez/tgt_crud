import flet as ft
from datetime import datetime, date
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
from dao.clientes_dao import ClienteDAO
from dao.pedido_dao import PedidoDAO
from dao.prenda_dao import PrendaDAO
from dao.empleado_dao import EmpleadoDAO
from models.clientes import Cliente
from models.pedido import Pedido
from models.prenda import Prenda


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

    dd_empleado = campo_dropdown(
        "Atendido por (opcional)",
        width=250,
        options=[]
    )

    def cargar_empleados():
        try:
            dd_empleado.options = [
                ft.dropdown.Option(str(emp.id_empleado), text=f"{emp.nombre} ({emp.puesto})")
                for emp in EmpleadoDAO.seleccionar()
            ]
        except Exception as ex:
            print(f"❌ Error al cargar empleados: {ex}")
            dd_empleado.options = []

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

    fecha_entrega = campo_texto("Fecha Entrega (DD/MM/AAAA)", width=200)

    txt_fecha_pedido = campo_texto(
        "Fecha Pedido",
        value=datetime.now().strftime("%d/%m/%Y"),
        width=200,
        read_only=True,
    )

    dd_estado = campo_dropdown(
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
    )

    txt_observaciones = campo_texto(
        "Observaciones",
        multiline=True,
        min_lines=4,
        max_lines=6
    )


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

    def mostrar_snack(texto, es_error=False):
        snack = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=ft.Colors.RED_400 if es_error else COLOR_GOLD
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def limpiar_formulario():
        cliente.value = ""
        telefono.value = ""
        dd_empleado.value = None
        fecha_entrega.value = ""
        txt_precio.value = ""
        txt_anticipo.value = ""
        restante.value = "Restante: $0.00"
        dd_estado.value = "Pendiente"
        txt_observaciones.value = ""
        for fila in filas_tipo_prenda:
            fila["checkbox"].value = False
            fila["cantidad"].value = "0"

    def guardar_pedido(e):
        prendas_seleccionadas = obtener_prendas_seleccionadas()

        if (
            not cliente.value
            or not prendas_seleccionadas
            or not fecha_entrega.value
            or not txt_precio.value
            or not txt_anticipo.value
        ):
            mostrar_snack("No se guardó. Completa los campos obligatorios (cliente, al menos una prenda, fecha de entrega, precio y anticipo).", es_error=True)
            return

        if telefono.value and len(telefono.value) != 10:
            mostrar_snack("El teléfono debe tener 10 dígitos.", es_error=True)
            return

        try:
            precio = float(txt_precio.value)
            anticipo = float(txt_anticipo.value)
        except ValueError:
            mostrar_snack("Precio y anticipo deben ser números válidos.", es_error=True)
            return

        try:
            fecha_pedido_dt = datetime.strptime(txt_fecha_pedido.value, "%d/%m/%Y").date()
            fecha_entrega_dt = datetime.strptime(fecha_entrega.value.strip(), "%d/%m/%Y").date()
        except ValueError:
            mostrar_snack("La fecha de entrega debe tener el formato DD/MM/AAAA.", es_error=True)
            return

        try:
            # 1) Cliente: si ya existe uno con ese teléfono, se reutiliza.
            #    Si no, se crea uno nuevo con los datos del formulario.
            cliente_encontrado = ClienteDAO.buscar_por_telefono(telefono.value) if telefono.value else None

            if cliente_encontrado:
                id_cliente = cliente_encontrado.id_cliente
                mensaje_cliente = f"cliente existente ({cliente_encontrado.nombre_completo})"
            else:
                id_cliente = ClienteDAO.insertar(Cliente(
                    nombre_completo=cliente.value.strip(),
                    telefono=telefono.value or "",
                    fecha_registro=date.today(),
                ))
                mensaje_cliente = "cliente nuevo"

            # 2) Pedido, ligado a ese cliente.
            id_empleado = int(dd_empleado.value) if dd_empleado.value else None

            id_pedido = PedidoDAO.insertar(Pedido(
                id_cliente=id_cliente,
                id_empleado=id_empleado,
                fecha_pedido=fecha_pedido_dt,
                fecha_entrega=fecha_entrega_dt,
                anticipo=anticipo,
                total=precio,
                estado=dd_estado.value or "Pendiente",
            ))

            # 3) Una fila en "prendas" por cada unidad marcada (tipo + cantidad).
            for nombre_prenda, cantidad in prendas_seleccionadas:
                for _ in range(cantidad):
                    PrendaDAO.insertar(Prenda(
                        id_pedido=id_pedido,
                        tipo_prenda=nombre_prenda,
                        modelo="",
                        talla="",
                        color="",
                        precio=0.0,
                    ))

            mostrar_snack(f"✓ Pedido #{id_pedido} guardado con éxito ({mensaje_cliente}).")
            limpiar_formulario()
            cargar_empleados()
            if page:
                page.update()

        except Exception as ex:
            mostrar_snack(f"Error al guardar el pedido: {ex}", es_error=True)

    cargar_empleados()

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


                                    dd_empleado

                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),



                            ft.Row(
                                [

                                    txt_fecha_pedido,


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



                            dd_estado,



                            txt_observaciones,

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