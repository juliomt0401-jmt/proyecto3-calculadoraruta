from api import leer_coordenadas_actual, coordenadas_a_direccion, direccion_a_coordenadas

def prueba1():
    print("Obteniendo coordenadas…")
    lat, lon = leer_coordenadas_actual()
    print("Lat:", lat, "Lon:", lon)

    print("\nConvirtiendo a dirección…")
    direccion = coordenadas_a_direccion(lat, lon)
    print("Dirección:", direccion)

def prueba2():
    print("Convirtiendo dirección a coordenadas…")
    direccion = "Avenida General Felipe Santiago Salaverry 3030, San Isidro, Lima, Peru"
    lat, lon = direccion_a_coordenadas(direccion)
    print("Dirección:", direccion)
    print("Lat:", lat, "Lon:", lon)



if __name__ == "__main__":
    prueba1()
    prueba2()

