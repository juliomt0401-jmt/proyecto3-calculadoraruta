import requests

def leer_coordenadas_actual():
    try:
        # Obtener IP pública
        url = "https://api.ipify.org/?format=json"
        data = requests.get(url).json()
        ip = data.get("ip")
        if not ip:
            return None, None
        #ip = requests.get("https://api.ipify.org/?format=json").json()["ip"]

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
