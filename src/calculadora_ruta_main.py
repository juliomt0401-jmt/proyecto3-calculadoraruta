import flet as ft
from ui import crear_pantalla_principal

def main(page: ft.Page):
    page.title = "Calculadora de Ruta"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Cargar la UI principal
    crear_pantalla_principal(page)

# Ejecutar la app
if __name__ == "__main__":
    ft.app(target=main)
