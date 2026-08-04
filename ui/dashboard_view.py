import flet as ft
from ui.styles import (COLOR_BG_DARK, COLOR_BG_CARD, COLOR_GOLD, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_BORDER, FOND_BRAND,)
from ui.catalogo_accesorios_view import CatalogoView
from ui.catalogo_main_view import CatalogoMainView
from ui.citas_medidas_main_view import CitasMedidasMainView

def DashboardView(page: ft.Page, on_navigate):
    opcion_activa = {"actual": "dashboard"}
    #RECUADROS
    def crear_tarjeta_modulo(titulo, subtitulo, icono, ruta):
        return ft.Container(
            content = ft.Column(
                controls = [
                    ft.Icon(icono, color = COLOR_GOLD, size = 36),
                    ft.Text(
                        titulo,
                        font_family = FOND_BRAND,
                        size = 16,
                        color = COLOR_TEXT_PRIMARY,
                        weight = ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        subtitulo,
                        size = 12,
                        color = COLOR_TEXT_SECONDARY,
                    ),
                ],
                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 8,
            ),
            bgcolor = COLOR_BG_CARD,
            padding = 20,
            border_radius = 8,
            border = ft.Border.all(1, COLOR_BORDER),
            ink = True,
            on_click = lambda _: cambiar_panel(ruta),
            width = 220,
            height = 150,
        )

    vista_inicio = ft.Column(
        controls = [
            ft.Text(
                "PANEL DE ADMINISTRACIÓN",
                font_family = FOND_BRAND,
                size = 24,
                color = COLOR_GOLD,
                weight = ft.FontWeight.BOLD,
            ),
            ft.Text(
                "¡Bienvenido de nuevo!",
                size = 14,
                color = COLOR_TEXT_SECONDARY,
            ),
            ft.Container(height = 20),

            ft.Row(
                controls = [
                    crear_tarjeta_modulo("NUEVO PEDIDO", "Registrar traje o prenda", ft.Icons.ADD_SHOPPING_CART, "nuevo_pedido"),
                    crear_tarjeta_modulo("AGENDAR CITA", "Citas de prueba y toma de medidas", ft.Icons.CALENDAR_TODAY, "agendar_cita"),
                    crear_tarjeta_modulo("VER PEDIDOS", "Estatus y entregas pendientes", ft.Icons.ASSIGNMENT, "ver_pedidos"),
                ],
                spacing = 20,
                wrap = True,
            ),
            ft.Container(height = 15),
            ft.Row(
                controls = [
                    crear_tarjeta_modulo("CATÁLOGO", "Prendas, sacos y accesorios", ft.Icons.CHECKROOM, "catalogo"),
                    crear_tarjeta_modulo("BASE DE CLIENTES", "Historial y medidas de clientes", ft.Icons.CONTACTS, "clientes"),
                    crear_tarjeta_modulo("MEDIDAS Y TALLAS", "Fichas técnicas de confección", ft.Icons.STRAIGHTEN, "medidas"),
                ],
                spacing = 20,
                wrap = True,
            ),
        ],
        spacing = 10,
    )

    #CONTENEDOR CENTRAL
    contenido_principal = ft.Container(
        expand = True,
        padding = 30,
        bgcolor = COLOR_BG_DARK,
        content = vista_inicio,
    )
    sidebar_container = ft.Container (
        width = 250,
        bgcolor = COLOR_BG_CARD,
        padding = 20,
        border = ft.Border(right = ft.BorderSide (1, COLOR_BORDER)),
    )
    def construir_sidebar ():
        actual = opcion_activa["actual"]

        return ft.Column(
            controls = [
                ft.Row(
                    controls = [
                        ft.Icon(ft.Icons.SHIELD_OUTLINED, color = COLOR_GOLD, size = 24),
                        ft.Text(
                            "THE GENTLEMAN'S TAILOR",
                            font_family = FOND_BRAND,
                            size = 12,
                            color = COLOR_GOLD,
                            weight = ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment = ft.MainAxisAlignment.CENTER,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER
                ),
                ft.Divider(color = COLOR_BORDER, height = 20),

                ft.ListTile(
                    leading = ft.Icon(
                        ft.Icons.DASHBOARD_OUTLINED,
                        color = COLOR_GOLD if actual in ["dashboard", "inicio"] else COLOR_TEXT_SECONDARY
                    ),
                    title = ft.Text(
                        "Inicio",
                        color = COLOR_TEXT_PRIMARY if actual in ["dashboard", "inicio"] else ft.FontWeight.NORMAL
                    ),
                    on_click = lambda _: cambiar_panel("dashboard"),
                ),

                ft.ListTile(
                    leading = ft.Icon(
                        ft.Icons.SHOPPING_BAG_OUTLINED,
                        color = COLOR_GOLD if actual == "pedidos" else COLOR_TEXT_SECONDARY
                    ),
                    title = ft.Text(
                        "Pedidos",
                        color = COLOR_TEXT_PRIMARY if actual == "pedidos" else COLOR_TEXT_SECONDARY,
                        weight = ft.FontWeight.BOLD if actual == "pedidos" else ft.FontWeight.NORMAL
                    ),
                    on_click = lambda _: cambiar_panel("pedidos"),
                ),

                ft.ListTile(
                    leading = ft.Icon(
                        ft.Icons.CALENDAR_MONTH_OUTLINED,
                        color = COLOR_GOLD if actual == "citas" else COLOR_TEXT_SECONDARY
                    ),
                    title = ft.Text(
                        "Citas y Medidas",
                        color = COLOR_TEXT_PRIMARY if actual == "citas" else COLOR_TEXT_SECONDARY,
                        weight = ft.FontWeight.BOLD if actual == "citas" else ft.FontWeight.NORMAL
                    ),
                    on_click = lambda _: cambiar_panel("citas"),
                ),

                ft.ListTile(
                    leading = ft.Icon(
                        ft.Icons.PEOPLE_OUTLINE,
                        color = COLOR_GOLD if actual == "clientes" else COLOR_TEXT_SECONDARY
                    ),
                    title = ft.Text(
                        "Clientes",
                        color = COLOR_TEXT_PRIMARY if actual == "clientes" else COLOR_TEXT_SECONDARY,
                        weight = ft.FontWeight.BOLD if actual == "clientes" else ft.FontWeight.NORMAL
                    ),
                    on_click = lambda _: cambiar_panel("clientes"),
                ),

                ft.ListTile(
                    leading = ft.Icon(
                        ft.Icons.INVENTORY_2_OUTLINED,
                        color = COLOR_GOLD if actual == "catalogo" else COLOR_TEXT_SECONDARY
                    ),
                    title = ft.Text(
                        "Catálogo",
                        color = COLOR_TEXT_PRIMARY if actual == "catalogo" else COLOR_TEXT_SECONDARY,
                        weight = ft.FontWeight.BOLD if actual == "catalogo" else ft.FontWeight.NORMAL
                    ),
                    on_click = lambda _: cambiar_panel("catalogo"),
                ),
                ft.Container(expand = True),
                ft.Divider (color = COLOR_BORDER, height = 20),
                ft.ListTile(
                    leading = ft.Icon(ft.Icons.LOGOUT, color = ft.Colors.RED_400),
                    title = ft.Text("Cerrar Sesión", color = ft.Colors.RED_400),
                    on_click = lambda _: on_navigate("login"),
                ),
                
            ],
            spacing = 5,
        )

    def cambiar_panel(vista):
        opcion_activa["actual"] = vista
        if vista in ["dashboard", "inicio"]:
            contenido_principal.content = vista_inicio
        elif vista == "catalogo":
            contenido_principal.content = CatalogoMainView(page)
        elif vista in ["citas", "agendar_cita"]:
            opcion_activa["actual"] = "citas"
            contenido_principal.content = CitasMedidasMainView(page)
        else:
            contenido_principal.content = ft.Text(
                f"MÓDULO: {vista.upper()}", 
                size=24, 
                color=COLOR_GOLD, 
                font_family=FOND_BRAND
            )

        sidebar_container.content = construir_sidebar()
        contenido_principal.update()
        sidebar_container.update()
        page.update()

    sidebar_container.content = construir_sidebar()

    return ft.Row(
        controls = [
            sidebar_container,
            contenido_principal,
        ],
        expand = True,
        spacing = 0,
    )

    #MENU LATERAL
    sidebar = ft.Container(
        width = 250,
        bgcolor = COLOR_BG_CARD,
        padding = 20,
        border = ft.Border(right = ft.BorderSide(1, COLOR_BORDER)),
        content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SHIELD_OUTLINED, color=COLOR_GOLD, size=24),
                        ft.Text(
                            " THE GENTLEMAN'S TAILOR",
                            font_family = FOND_BRAND,
                            size = 12,
                            color = COLOR_GOLD,
                            weight = ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment = ft.MainAxisAlignment.CENTER,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER
                ),
                ft.Divider(color = COLOR_BORDER, height = 20),
                
                ft.ListTile(
                    leading = ft.Icon(ft.Icons.DASHBOARD_OUTLINED, color=COLOR_GOLD),
                    title = ft.Text("Inicio", color=COLOR_TEXT_PRIMARY),
                    on_click = lambda _: cambiar_panel("dashboard"),
                ),
                ft.ListTile(
                    leading = ft.Icon(ft.Icons.SHOPPING_BAG_OUTLINED, color = COLOR_TEXT_SECONDARY),
                    title = ft.Text("Pedidos", color = COLOR_TEXT_SECONDARY),
                    on_click = lambda _: cambiar_panel("pedidos"),
                ),
                ft.ListTile(
                    leading = ft.Icon(ft.Icons.CALENDAR_MONTH_OUTLINED, color = COLOR_TEXT_SECONDARY),
                    title = ft.Text("Citas y Medidas", color = COLOR_TEXT_SECONDARY),
                    on_click = lambda _: cambiar_panel("citas"),
                ),
                ft.ListTile(
                    leading = ft.Icon(ft.Icons.PEOPLE_OUTLINE, color = COLOR_TEXT_SECONDARY),
                    title = ft.Text("Clientes", color = COLOR_TEXT_SECONDARY),
                    on_click = lambda _: cambiar_panel("clientes"),
                ),
                ft.ListTile(
                    leading = ft.Icon(ft.Icons.INVENTORY_2_OUTLINED, color = COLOR_TEXT_SECONDARY),
                    title = ft.Text("Catálogo", color = COLOR_TEXT_SECONDARY),
                    on_click = lambda _: cambiar_panel("catalogo"),
                ),
                
                ft.Container(expand = True),
                ft.Divider(color = COLOR_BORDER, height = 20),
                ft.ListTile(
                    leading = ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED_400),
                    title = ft.Text("Cerrar Sesión", color=ft.Colors.RED_400),
                    on_click = lambda _: on_navigate("login"),
                ),
            ],
            spacing = 5,
        ),
    )

    return ft.Row(
        controls = [
            sidebar,
            contenido_principal,
        ],
        expand = True,
        spacing = 0,
    )