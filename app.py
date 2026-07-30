

import flet as ft
from ui.styles import COLOR_BG_DARK
from ui.login_view import LoginView

def main(page: ft.Page):
    page.title = "The Gentleman's Tailor - Admin"
    page.bgcolor = COLOR_BG_DARK
    page.padding = 0

    page.fonts = {
        "Cinzel": "https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap",
        "Cormorant": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&display=swap",
        "Montserrat": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap",
    }

    def ir_al_dashboard():
        page.controls.clear()
       
        page.add(ft.Text("¡Bienvenido al Dashboard!", color="#F5F2E9", size=30))
        page.update()

    # Pantalla 1: Iniciar Sesión
    page.add(LoginView(page, on_login_success=ir_al_dashboard))

if __name__ == "__main__":
    ft.run(main)

import dao.accesorio_dao as AccesorioDAO
from models.accesorio import Accesorio

def mostrar_menu_accesorios():
    print("\n==================================")
    print("   SISTEMA DE CONTROL DE ACCESORIOS")
    print("==================================")
    print("1. Insertar nuevo accesorio")
    print("2. Consultar todos los accesorios")
    print("3. Actualizar un accesorio")
    print("4. Eliminar un accesorio")
    print("5. Salir del sistema")
    print("==================================")

while True:
    mostrar_menu_accesorios()
    opcion = input("Selecciona una opción (1-5): ").strip()

    if opcion == "1":
        print("\n--- REGISTRAR NUEVO ACCESORIO ---")
        nombre = input("Nombre del accesorio (ej. Corbata de Seda): ")
        tipo = input("Categoría / Tipo (ej. Formal): ")
        try:
            precio = float(input("Precio del producto (ej. 250.50): "))
            
            
            nuevo_acc = Accesorio(nombre=nombre, tipo=tipo, precio=precio)
            AccesorioDAO.insertar(nuevo_acc)
            print("¡Accesorio guardado exitosamente en la base de datos!")
        except ValueError:
            print("Error: El precio debe ser un número válido.")

    elif opcion == "2":
        print("\n--- INVENTARIO DE ACCESORIOS ---")
        inventario = AccesorioDAO.listar()
        if inventario:
            print(f"{'ID':<5} | {'PRODUCTO':<30} | {'CATEGORÍA':<15} | {'PRECIO':<10}")
            print("-" * 70)
            for fila in inventario:
                print(f"{fila[0]:<5} | {fila[1]:<30} | {fila[2]:<15} | ${fila[3]:.2f}")
        else:
            print("La base de datos está vacía. No hay accesorios registrados.")

    elif opcion == "3":
        print("\n--- ACTUALIZAR ACCESORIO EXISTENTE ---")
        try:
            id_modificar = int(input("Introduce el ID del accesorio que deseas actualizar: "))
            nombre = input("Nuevo nombre del accesorio: ")
            tipo = input("Nueva categoría / tipo: ")
            precio = float(input("Nuevo precio: "))
            
            
            acc_modificado = Accesorio(id_accesorio=id_modificar, nombre=nombre, tipo=tipo, precio=precio)
            AccesorioDAO.actualizar(acc_modificado)
            print(f"¡El accesorio con ID {id_modificar} ha sido actualizado!")
        except ValueError:
            print("Error: Asegúrate de ingresar números válidos para el ID y el Precio.")

    elif opcion == "4":
        print("\n--- ELIMINAR ACCESORIO ---")
        try:
            id_eliminar = int(input("Introduce el ID del accesorio que deseas borrar: "))

            
            confirmacion = input(f"¿Estás seguro de eliminar el ID {id_eliminar}? (s/n): ").strip().lower()
            if confirmacion == 's':
                AccesorioDAO.eliminar(id_eliminar)
                print(f"¡El accesorio con ID {id_eliminar} ha sido borrado permanentemente!")
            else:
                print("Operación cancelada.")
        except ValueError:
            print("Error: El ID debe ser un número entero.")

    elif opcion == "5":
        print("\n Saliendo...")
        break

    else:
        print("\nOpción no válida. Por favor, selecciona un número del 1 al 5.")
