import flet as ft
from logica import (leer_coordenadas_actual, coordenadas_a_direccion,
                    direccion_a_coordenadas, evaluar_coordenadas)


def crear_pantalla_principal(page: ft.Page):
    #
    # --- OBTENER UBICACION ACTUAL ---
    #
    lat, lon = leer_coordenadas_actual()
    direccion_actual = coordenadas_a_direccion(lat, lon)

    #
    # --- OBJETOS PRINCIPALES ---
    #

    # Dirección 1 (inicializada con ubicación actual)
    direccion1 = ft.TextField(
        label="Dirección de origen",
        value=direccion_actual,
        width=400,
        disabled=False,
        visible=True
    )

    # Dirección 2
    direccion2 = ft.TextField(
        label="Dirección de destino",
        value="",
        width=400,
        disabled=False,
        visible=True
    )

    # Botón calcular tiempo/distancia
    boton_calcular_td = ft.ElevatedButton(
        "Calcular tiempo/distancia",
        disabled=False,
        visible=True
    )
    boton_calcular_td.on_click = calcular_td_click












    #
    # --- OBJETOS OCULTOS INICIALMENTE ---
    #

    # Tiempo
    label_tiempo = ft.Text("Tiempo estimado:", visible=True)
    valor_tiempo = ft.Text("", visible=False)

    # Distancia
    label_distancia = ft.Text("Distancia:", visible=True)
    valor_distancia = ft.Text("", visible=False)

    # Precio por hora
    precio_hora = ft.TextField(
        label="Precio por hora (S/)",
        value="0",
        width=200,
        disabled=True,
        visible=False
    )

    # Precio por km
    precio_km = ft.TextField(
        label="Precio por km (S/)",
        value="0",
        width=200,
        disabled=True,
        visible=False
    )

    # Botón calcular tarifa
    boton_calcular_tarifa = ft.ElevatedButton(
        "Calcular tarifa",
        disabled=True,
        visible=False
    )

    # Tarifa por hora
    label_tarifa_hora = ft.Text("Tarifa por hora:", visible=False)
    valor_tarifa_hora = ft.Text("", visible=False)

    # Tarifa por distancia
    label_tarifa_distancia = ft.Text("Tarifa por distancia:", visible=False)
    valor_tarifa_distancia = ft.Text("", visible=False)

    # Botón nueva consulta
    boton_nueva_consulta = ft.ElevatedButton(
        "Nueva consulta",
        disabled=True,
        visible=False
    )

    # Botón ver ruta
    boton_ver_ruta = ft.ElevatedButton(
        "Ver ruta",
        disabled=True,
        visible=False
    )








    #
    # --- EVENTOS ---
    #

    # 1. Evento calcular tiempo/distancia
    def calcular_td_click(e):

        # 1. Obtener direcciones
        origen = direccion1.value
        destino = direccion2.value

        # Validación mínima
        if origen.strip() == "" or destino.strip() == "":
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Debe ingresar ambas direcciones."),
            )
            page.dialog.open = True
            page.update()
            return

        # 2. Convertir direcciones a coordenadas
        lat1, lon1 = direccion_a_coordenadas(origen)
        lat2, lon2 = direccion_a_coordenadas(destino)

        # 3. Calcular distancia real
        tiempo_min, distancia_km = evaluar_coordenadas(lat1, lon1, lat2, lon2)
        if tiempo_min is None or distancia_km is None:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("No se pudo calcular la ruta. Verifique las direcciones."),
            )
            page.dialog.open = True
            page.update()
            return

        # 4. Mostrar resultados
        valor_tiempo.value = f"{tiempo_min} minutos"
        valor_distancia.value = f"{distancia_km:.2f} km"
        label_tiempo.visible = True
        valor_tiempo.visible = True
        label_distancia.visible = True
        valor_distancia.visible = True

        # 5. Habilitar precios
        precio_hora.visible = True
        precio_hora.disabled = False
        precio_km.visible = True
        precio_km.disabled = False

        # 7. Habilitar botón calcular tarifa
        boton_calcular_tarifa.visible = True
        boton_calcular_tarifa.disabled = False

        # 8. Habilitar botón nueva consulta
        boton_nueva_consulta.visible = True
        boton_nueva_consulta.disabled = False

        page.update()



    # 2. Evento calcular tarifa
    def calcular_tarifa_click(e):

        # Simulación temporal
        tarifa_hora = float(precio_hora.value) * 1.5
        tarifa_distancia = float(precio_km.value) * 12.5

        valor_tarifa_hora.value = f"S/ {tarifa_hora:.2f}"
        valor_tarifa_distancia.value = f"S/ {tarifa_distancia:.2f}"

        # Mostrar tarifas
        label_tarifa_hora.visible = True
        valor_tarifa_hora.visible = True
        label_tarifa_distancia.visible = True
        valor_tarifa_distancia.visible = True

        # Mostrar botones finales
        boton_nueva_consulta.visible = True
        boton_nueva_consulta.disabled = False
        boton_ver_ruta.visible = True
        boton_ver_ruta.disabled = False

        page.update()

    boton_calcular_tarifa.on_click = calcular_tarifa_click

    # 3. Evento nueva consulta
    def nueva_consulta_click(e):

        # Reset de todos los objetos
        direccion1.value = "Mi ubicación actual"
        direccion2.value = ""

        # Ocultar todo excepto los 3 objetos iniciales
        for obj in [
            label_tiempo, valor_tiempo,
            label_distancia, valor_distancia,
            precio_hora, precio_km,
            boton_calcular_tarifa,
            label_tarifa_hora, valor_tarifa_hora,
            label_tarifa_distancia, valor_tarifa_distancia,
            boton_nueva_consulta, boton_ver_ruta
        ]:
            obj.visible = False
            if hasattr(obj, "disabled"):
                obj.disabled = True

        page.update()

    boton_nueva_consulta.on_click = nueva_consulta_click

    # 4. Evento ver ruta
    def ver_ruta_click(e):
        # Aquí luego abriremos un mapa real
        page.dialog = ft.AlertDialog(
            title=ft.Text("Ruta"),
            content=ft.Text("Aquí se mostrará el mapa con la ruta."),
        )
        page.dialog.open = True
        page.update()

    boton_ver_ruta.on_click = ver_ruta_click

    #
    # --- LAYOUT ---
    #

    page.add(
        ft.Column(
            controls=[
                direccion1,
                direccion2,
                boton_calcular_td,

                # Tiempo y distancia
                label_tiempo,
                valor_tiempo,
                label_distancia,
                valor_distancia,

                # Precios
                ft.Row([precio_hora, precio_km]),
                boton_calcular_tarifa,

                # Tarifas
                label_tarifa_hora,
                valor_tarifa_hora,
                label_tarifa_distancia,
                valor_tarifa_distancia,

                # Botones finales
                ft.Row([boton_nueva_consulta, boton_ver_ruta])
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
