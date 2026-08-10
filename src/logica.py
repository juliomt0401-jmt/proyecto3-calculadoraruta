from decimal import Decimal

def limpiar_tipo_via(street):
    if street is None:
        return None

    # Sufijos que queremos eliminar
    sufijos = [
        " Street", " Avenue", " Road", " Lane",
        " Boulevard", " Drive", " Alley"
    ]

    for sufijo in sufijos:
        if street.endswith(sufijo):
            return street.replace(sufijo, "").strip()

    return street

def obtener_coordenadas_validas(datajson):
    # 1. Obtener datos de la direccion buscada
    parsed = datajson.get("query", {}).get("parsed", {})
    numero_buscado = parsed.get("housenumber")
    ciudad_esperada = parsed.get("city")
    estado_esperado = parsed.get("state")
    pais_esperado = parsed.get("country")

    # 2. Recorrer las entradas de "resultados" y descartar segun la direccion de entrada
    resultados = datajson.get("results")
    validos = []
    for r in resultados:
        if r.get("result_type").lower() not in ["building", "amenity"]:
            continue
        if r.get("housenumber") != numero_buscado:
            continue
        if r.get("city").lower() != ciudad_esperada.lower():
            continue
        if r.get("state").lower() != estado_esperado.lower():
            continue
        if r.get("country").lower() != pais_esperado.lower():
            continue
        validos.append(r)

    if not validos:
           return None, None

    # 3. Recorrer las entradas  "validas" y quedarse con la mas exacta
    menor_area = float("inf")
    r_menor = None
    for r in validos:
        bbox = r.get("bbox", {})
        lon1 = bbox.get("lon1")
        lat1 = bbox.get("lat1")
        lon2 = bbox.get("lon2")
        lat2 = bbox.get("lat2")
        area = abs(lon2 - lon1) * abs(lat2 - lat1)
        if area < menor_area:
            menor_area = area
            r_menor = r

    # 4. Extraer coordenadas finales
    lat = r_menor.get("lat")
    lon = r_menor.get("lon")

    return lat, lon

def calcula_tiempo_distancia(tiempo_s, distancia_m):
    if tiempo_s is None or distancia_m is None:
        return None, None, None

    # Convertir a minutos y kilómetros
    tiempo_min = tiempo_s / 60
    distancia_km = float(distancia_m / 1000)

    # Calcular horas y minutos
    horas = int(tiempo_min // 60)
    minutos = int(tiempo_min % 60)

    return horas, minutos, distancia_km

def calcular_tarifa(hora, minutos, km, precio_hora, precio_km):
    if hora is None or minutos is None or km is None:
        return None, None

    # Calcular tarifa
    tarifa_hora = Decimal((hora * precio_hora) + (minutos / 60 * precio_hora))
    tarifa_distancia = Decimal(km * precio_km)
    return tarifa_hora, tarifa_distancia