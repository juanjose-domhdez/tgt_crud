# ui/registro_cliente_view.py
import flet as ft
from datetime import datetime
from models.cliente import Cliente
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

def RegistrosClienteView(page: ft.Page, on_regresar, db_connection=None):
    cliente_dao = ClienteDAO(db_connection) if db_connection else None

    # Función para obtener o calcular el siguiente ID
    def obtener_siguiente_id():
        if cliente_dao and hasattr(cliente_dao, "obtener_ultimo_id"):
            ultimo_id = cliente_dao.obtener_ultimo_id()
            return str(ultimo_id + 1) if ultimo_id else "1"
        return "Autogenerado"

    # Campos del formulario de acuerdo a la tabla
    txt_id = ft.TextField(
        label="ID Cliente",
        value=obtener_siguiente_id(),
        read_only=True,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        text_style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY),
    )

    txt_nombre = ft.TextField(
        label="Nombre Completo",
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        text_style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY),
    )

    txt_telefono = ft.TextField(
        label="Teléfono",
        max_length=10,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        text_style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY),
    )

    txt_fecha = ft.TextField(
        label="Fecha de Registro",
        value=datetime.now().strftime("%Y-%m-%d"),
        read_only=True,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_GOLD,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, font_family=FONT_BODY),
        text_style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, font_family=FONT_BODY),
    )

    lbl_mensaje = ft.Text("", size=12, color=COLOR_GOLD, font_family=FONT_BODY)

    def guardar_cliente(e):
        if not txt_nombre.value or not txt_telefono.value:
            lbl_mensaje.value = "Por favor completa todos los campos."
            lbl_mensaje.color = ft.Colors.RED_400
            lbl_mensaje.update()
            return

        if len(txt_telefono.value) != 10:
            lbl_mensaje.value = "El teléfono debe contener exactamente 10 dígitos."
            lbl_mensaje.color = ft.Colors.RED_400
            lbl_mensaje.update()
            return

        nuevo_cliente = Cliente(
            nombre_completo=txt_nombre.value,
            telefono=txt_telefono.value,
            fecha_registro=txt_fecha.value
        )

        if cliente_dao:
            cliente_dao.insertar_cliente(nuevo_cliente)

        lbl_mensaje.value = "¡Cliente registrado con éxito!"
        lbl_mensaje.color = COLOR_GOLD
        txt_nombre.value = ""
        txt_telefono.value = ""
        txt_id.value = obtener_siguiente_id()
        
        lbl_mensaje.update()
        txt_nombre.update()
        txt_telefono.update()
        txt_id.update()

    return ft.Container(
        expand=True,
        bgcolor=COLOR_BG_DARK,
        padding=30,
        content=ft.Column(
            controls=[
                # Encabezado con botón para regresar
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=COLOR_GOLD,
                            on_click=lambda _: on_regresar(),
                        ),
                        ft.Text(
                            "REGISTRO DE NUEVO CLIENTE",
                            font_family=FOND_BRAND,
                            size=22,
                            color=COLOR_GOLD,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(height=10),
                # Formulario dentro de una tarjeta
                ft.Container(
                    bgcolor=COLOR_BG_CARD,
                    padding=25,
                    border_radius=10,
                    border=ft.Border.all(1, COLOR_BORDER),
                    content=ft.Column(
                        controls=[
                            txt_id,
                            txt_nombre,
                            txt_telefono,
                            txt_fecha,
                            lbl_mensaje,
                            ft.Container(height=10),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        content=ft.Text("Guardar Cliente", color="black", weight="bold", font_family=FONT_BODY),
                                        icon=ft.Icons.SAVE,
                                        bgcolor=COLOR_GOLD,
                                        style=ft.ButtonStyle(
                                            padding=15,    
                                        ),
                                        on_click=guardar_cliente,
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            )
                        ],
                        spacing=15,
                    )
                )
            ],
            spacing=15,
        )
    )