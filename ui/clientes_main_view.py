import flet as ft
from ui.registro_cliente_view import RegistrosClienteView # Usando el nombre que pusiste en tu ejemplo
from ui.base_clientes_view import BaseClientesView

def ClientesMainView(page: ft.Page, db_connection= None):
    vista_actual = {"opcion": "menu"}

    def cambiar_sub_vista(sub_vista):
        vista_actual["opcion"] = sub_vista

        if sub_vista == "menu":
            contenedor_modulo.content = vista_menu
        elif sub_vista == "nuevo_cliente":
            contenedor_modulo.content = RegistrosClienteView(
                page=page,
                on_regresar=lambda: cambiar_sub_vista("menu"),
                db_connection=db_connection
            )
        elif sub_vista == "base_clientes":
            contenedor_modulo.content = BaseClientesView(
                page=page,
                on_regresar=lambda: cambiar_sub_vista("menu"),
                db_connection= db_connection
            )
        contenedor_modulo.update()

    # --- TARJETA RECUADRO (Estilo Catálogo) ---
    def crear_tarjeta_opcion(titulo, subtitulo, icono, texto_boton, accion_key):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icono, size=55, color=ft.Colors.AMBER_400),
                    ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(
                        subtitulo,
                        color=ft.Colors.WHITE_54,
                        text_align=ft.TextAlign.CENTER,
                        size=13
                    ),
                    ft.ElevatedButton(
                        texto_boton,
                        icon=ft.Icons.ARROW_FORWARD,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.AMBER_500, 
                            color=ft.Colors.BLACK
                        ),
                        on_click=lambda _: cambiar_sub_vista(accion_key)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            padding=25,
            width=320,
            height=280,
            bgcolor="#1E293B",
            border_radius=15,
            border=ft.Border.all(1, ft.Colors.BLUE_GREY_800)
        )

    # --- VISTA MENU PRINCIPAL ---
    vista_menu = ft.Column(
        [
            ft.Text("GESTIÓN DE CLIENTES", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400),
            ft.Text("Selecciona la opción que deseas realizar:", color=ft.Colors.WHITE_70),
            ft.Container(height=20),
            ft.Row(
                [
                    crear_tarjeta_opcion(
                        "NUEVO CLIENTE",
                        "Registrar un nuevo cliente en el sistema",
                        ft.Icons.PERSON_ADD_ALT_1,
                        "Registrar Cliente",
                        "nuevo_cliente"
                    ),
                    crear_tarjeta_opcion(
                        "BASE DE CLIENTES",
                        "Consultar el directorio e historial de clientes",
                        ft.Icons.CONTACTS,
                        "Ver Base Datos",
                        "base_clientes"
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    contenedor_modulo = ft.Container(
        content=vista_menu,
        alignment=ft.Alignment(0, 0),
        expand=True,
    )

    return contenedor_modulo