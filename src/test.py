from api import leer_coordenadas_actual, coordenadas_a_direccion

def probar():
    print("Obteniendo coordenadas…")
    lat, lon = leer_coordenadas_actual()
    print("Lat:", lat, "Lon:", lon)

    print("\nConvirtiendo a dirección…")
    direccion = coordenadas_a_direccion(lat, lon)
    print("Dirección:", direccion)

if __name__ == "__main__":
    probar()
