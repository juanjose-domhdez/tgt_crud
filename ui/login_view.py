import flet as ft
from ui.styles import (COLOR_BG_DARK, COLOR_BG_CARD, COLOR_GOLD, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_BORDER,FOND_BRAND, FONT_BODY, FONT_HEADING)

USUARIOS_VALIDOS = {
    "sastre1": "1234",
    "sastre2": "9876",
}


def LoginView(page: ft.page, on_login_success):
    usuario_input = ft.TextField(
        label = "Usuario / Correo",
        border_color = COLOR_BORDER,
        focused_border_color = COLOR_GOLD,
        label_style = ft.TextStyle(color = COLOR_TEXT_SECONDARY),
        text_style = ft.TextStyle(color = COLOR_TEXT_PRIMARY),
        cursor_color = COLOR_GOLD,
        width = 300,
    )

    contraseña_input = ft.TextField(
        label = "Contraseña",
        password = True,
        can_reveal_password = True,
        border_color = COLOR_BORDER,
        focused_border_color = COLOR_GOLD,
        label_style = ft.TextStyle(color = COLOR_TEXT_SECONDARY),
        text_style = ft.TextStyle(color = COLOR_TEXT_PRIMARY),
        cursor_color = COLOR_GOLD,
        width = 300,
    )

    def iniciar_sesion_click (e):
        user = usuario_input.value.strip() if usuario_input.value else ""
        password = contraseña_input.value.strip() if contraseña_input.value else ""

        if not user or not password:
            snack = ft.SnackBar(
            content = ft.Text("Ingresa usuario y contraseña"),
            bgcolor = ft.Colors.RED_900,
            open = True,
            )
            page.overlay.append(snack)
            page.update()
            return

        if user in USUARIOS_VALIDOS and USUARIOS_VALIDOS[user] == password:
            on_login_success ()
        else:
            snack = ft.SnackBar(
                content = ft.Text("Usuario o contraseña incorrectos"),
                bgcolor = ft.Colors.RED_900,
                open = True,
            )
            page.overlay.append(snack)
            page.update()

    car_login = ft.Container(
        content = ft.Column(
            controls = [
                ft.Icon(ft.Icons.SHIELD_OUTLINED, color = COLOR_GOLD, size = 48),
                ft.Text(
                    "THE GENTLEMAN'S TAILOR",
                    font_family = FOND_BRAND,
                    size = 18,
                    color = COLOR_GOLD,
                    weight = ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "INICIO DE SESIÓN",
                    font_family = FOND_BRAND,
                    size = 22,
                    color = COLOR_TEXT_PRIMARY,
                    weight = ft.FontWeight.BOLD,
                ),
                ft.Text("Panel de administración", color= COLOR_TEXT_SECONDARY, size = 12),
                ft.Container(height = 10),
                usuario_input,
                contraseña_input,
                ft.Container(height = 10),
                ft.ElevatedButton(
                    content = ft.Text("INICIAR SESIÓN", color = COLOR_BG_DARK, weight = ft.FontWeight.BOLD),
                    bgcolor = COLOR_GOLD,
                    width = 300,
                    style = ft.ButtonStyle(
                        shape = ft.RoundedRectangleBorder(radius=4),
                        padding = 15,
                    ),
                    on_click = iniciar_sesion_click, 
                ),
               
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 10,
        ),
        bgcolor = COLOR_BG_CARD,
        padding = 40,
        border_radius = 10,
        border = ft.Border.all(1, COLOR_BORDER),
    )
    return ft.Container(
        content = car_login,
        alignment = ft.Alignment(0,0),
        expand = True,
        )
