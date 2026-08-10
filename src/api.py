import requests
from configuracion import API_KEY_GEOAPIFY
from logica import limpiar_tipo_via, obtener_coordenadas_validas

def leer_coordenadas_actual():
    try:
        # Obtener IP pública
        url = "https://api.ipify.org/?format=json"
        data = requests.get(url).json()
        ip = data.get("ip")
        if not ip:
            return None, None

        # Obtener ubicación aproximada por IP
        url = f"https://ipinfo.io/{ip}/json"
        data = requests.get(url).json()

        # Coordenadas vienen como "lat,lon"
        loc = data.get("loc")
        if not loc:
            return None, None
        lat, lon = loc.split(",")
        return float(lat), float(lon)

    except Exception:
        return None, None

def coordenadas_a_direccion(lat, lon):
    try:
        url = (
            f"https://api.geoapify.com/v1/geocode/reverse?"
            f"lat={lat}&lon={lon}&apiKey={API_KEY_GEOAPIFY}"
        )

        data = requests.get(url).json()

        resultados = data.get("features")
        if not resultados:
            return None

        propiedades = resultados[0].get("properties", {})

        street = propiedades.get("street")
        housenumber = propiedades.get("housenumber")
        city = propiedades.get("city")
        state = propiedades.get("state")
        country = propiedades.get("country")

        # Limpiar tipo de vía
        street = limpiar_tipo_via(street)

        # Construir dirección final neutral
        direccion = f"{street} {housenumber}, {city}, {state}, {country}"

        return direccion

    except Exception:
        return None

def direccion_a_coordenadas(direccion):
    if direccion.strip() == "":
        return None, None

    try:
        url = (
            f"https://api.geoapify.com/v1/geocode/search?"
            f"text={direccion}&"
            f"format=json&"
            f"apiKey={API_KEY_GEOAPIFY}"
        )

        data = requests.get(url).json()
        resultados = data.get("results")
        if not resultados:
            return None, None

        lat, lon = obtener_coordenadas_validas(data)
        if lat is None or lon is None:
            return None, None

        return lat, lon

    except Exception:
        return None, None