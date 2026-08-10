import flet as ft
from api import (leer_coordenadas_actual, coordenadas_a_direccion, 
                 direccion_a_coordenadas, evaluar_coordenadas)
from logica import calcula_tiempo_distancia, calcular_tarifa

def mostrar_error(page, mensaje):
    page.dialog = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text(mensaje),
    )
    page.dialog.open = True
    page.update()

def crear_pantalla_principal(page: ft.Page):
    #
    # --- VARIABLES ---
    #
    hora = int(0)
    minutos = int(0)
    km = float(0)

    # --- OBTENER UBICACION ACTUAL ---
    #
    lat, lon = leer_coordenadas_actual()
    if lat is None or lon is None:
        mostrar_error(page, "No se pudo obtener las coordenadas de la ubicación actual, por favor ingresarla.")
        direccion_actual = ""
    else:
        direccion_actual = coordenadas_a_direccion(lat, lon)
        if direccion_actual is None:
            mostrar_error(page, "La dirección actual no se pudo obtener, por favor ingresarla.")
            direccion_actual = ""

    #
    # --- OBJETOS
    #

    # Direcciones
    label_paso_1 = ft.Text("Paso 1:", weight="bold")
    direccion1 = ft.TextField(label="Dirección de origen", value=direccion_actual, width=800)
    direccion2 = ft.TextField(label="Dirección de destino", value="", width=800)

    # Botón calcular tiempo/distancia
    boton_calcular_td = ft.ElevatedButton("Calcular tiempo/distancia")

    # Tiempo y distancia
    label_paso_2 = ft.Text("Paso 2:", weight="bold")
    label_tiempo = ft.Text("Tiempo estimado:")
    valor_tiempo = ft.Text("", weight="bold")
    label_distancia = ft.Text("Distancia:")
    valor_distancia = ft.Text("", weight="bold")
    fila_tiempo = ft.Row([label_tiempo, valor_tiempo])
    fila_distancia = ft.Row([label_distancia, valor_distancia])

    # Precio por hora
    precio_hora = ft.TextField(label="Precio por hora (S/)", value="0", width=200)

    # Precio por km
    precio_km = ft.TextField(label="Precio por km (S/)", value="0", width=200)

    # Botón calcular tarifa
    boton_regresar_paso1 = ft.ElevatedButton("Regresar")
    boton_calcular_tarifa = ft.ElevatedButton("Calcular tarifa")

    # Tarifa por hora y distancia
    label_tarifa_hora = ft.Text("Tarifa por hora:", visible=False)
    valor_tarifa_hora = ft.Text("", weight="bold")
    label_tarifa_distancia = ft.Text("Tarifa por distancia:")
    valor_tarifa_distancia = ft.Text("", weight="bold")
    fila_tarifa_hora = ft.Row([label_tarifa_hora, valor_tarifa_hora])
    fila_tarifa_distancia = ft.Row([label_tarifa_distancia, valor_tarifa_distancia])

    # Botón nueva consulta y ver ruta
    boton_regresar_paso2 = ft.ElevatedButton("Regresar")
    boton_nueva_consulta = ft.ElevatedButton("Nueva consulta")
    boton_ver_ruta = ft.ElevatedButton("Ver ruta")

    loader = ft.ProgressRing(visible=False)

    #
    # --- CONTENEDORES ---
    #

    # --- PASO 1 ---
    paso1 = ft.Column([label_paso_1, direccion1, direccion2, boton_calcular_td, loader],
                      visible=True)

    # --- PASO 2 ---
    paso2 = ft.Column([label_paso_2, fila_tiempo, fila_distancia, 
                       ft.Row([precio_hora, precio_km]),
                       boton_regresar_paso1, boton_calcular_tarifa],
                      visible=False)

    # --- PASO 3 ---
    paso3 = ft.Column([fila_tarifa_hora, fila_tarifa_distancia,
                       boton_regresar_paso2, boton_ver_ruta, boton_nueva_consulta],
                      visible=False)

    #
    # --- EVENTOS ---
    #

    # 1. Evento calcular tiempo/distancia
    def calcular_td_click(e):

        # 0. "pensando"
        boton_calcular_td.disabled = True
        loader.visible = True
        page.update()

        # 1. Obtener direcciones
        origen = direccion1.value
        destino = direccion2.value

        # 2. Convertir direcciones a coordenadas
        lat1, lon1 = direccion_a_coordenadas(origen)
        lat2, lon2 = direccion_a_coordenadas(destino)
        if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
            mostrar_error(page, ("No se pudo calcular la ruta. "
                                "Verifique que las direcciones no estén vacías y "
                                "que tengan un formato correcto."))
            return

        # 3. Calcular distancia real
        tiempo_s, distancia_m = evaluar_coordenadas(lat1, lon1, lat2, lon2)
        if tiempo_s is None or distancia_m is None:
            mostrar_error(page, ("No se pudo calcular la ruta. "
                                "Verifique que las direcciones no estén vacías y "
                                "que tengan un formato correcto."))
            return

        # 4. Mostrar resultados
        hora, minutos, km = calcula_tiempo_distancia(tiempo_s, distancia_m)
        valor_tiempo.value = f"{hora} horas {minutos} minutos"
        valor_distancia.value = f"{km:.2f} km"

        # 5. Finalizar
        boton_calcular_td.disabled = False
        loader.visible = False
        paso1.visible = False
        paso2.visible = True
        page.update()

    boton_calcular_td.on_click = calcular_td_click

    # 2. Regresa al paso 1
    def regresar_paso1_click(e):
        paso1.visible = True
        paso2.visible = False
        page.update()

    boton_regresar_paso1.on_click = regresar_paso1_click


    # 3. Evento calcular tarifa
    def calcular_tarifa_click(e):

        tarifa_hora, tarifa_distancia = calcular_tarifa(hora, minutos, km, 
                                                        float(precio_hora.value), float(precio_km.value))

        valor_tarifa_hora.value = f"S/ {tarifa_hora:.2f}"
        valor_tarifa_distancia.value = f"S/ {tarifa_distancia:.2f}"

        paso2.visible = False
        paso3.visible = True
        
        page.update()

    boton_calcular_tarifa.on_click = calcular_tarifa_click

    # 4. Regresa al paso 2
    def regresar_paso2_click(e):
        paso2.visible = True
        paso3.visible = False
        page.update()

    boton_regresar_paso2.on_click = regresar_paso2_click








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
                paso1,
                paso2,
                paso3
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
