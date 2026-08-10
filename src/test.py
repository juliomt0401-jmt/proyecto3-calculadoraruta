from api import (leer_coordenadas_actual, coordenadas_a_direccion, 
                 direccion_a_coordenadas, evaluar_coordenadas)
from logica import calcula_tiempo_distancia

def prueba1():
    print("Obteniendo coordenadas…")
    lat, lon = leer_coordenadas_actual()
    print("Lat:", lat, "Lon:", lon)
    print("Convirtiendo a dirección…")
    direccion = coordenadas_a_direccion(lat, lon)
    print("Dirección:", direccion)
    print("-----")

def prueba2():
    print("Convirtiendo dirección a coordenadas…")
    direccion = "Chiclayo 105, Rímac, Lima, Peru"
    lat, lon = direccion_a_coordenadas(direccion)
    print("Dirección:", direccion)
    print("Lat:", lat, "Lon:", lon)
    print("-----")

def prueba3():
    print("Convirtiendo dirección a coordenadas…")
    direccion = "Avenida General Felipe Santiago Salaverry 3030, San Isidro, Lima, Peru"
    lat, lon = direccion_a_coordenadas(direccion)
    print("Dirección:", direccion)
    print("Lat:", lat, "Lon:", lon)
    print("-----")

def prueba4():
    print("Calculando tiempo y distancia entre dos coordenadas…")
    lat1, lon1 = -12.0426048, -77.0286914 #Rimac
    lat2, lon2 = -12.0942371, -77.0537614 #San I
    tiempo_seg, distancia_m = evaluar_coordenadas(lat1, lon1, lat2, lon2)
    print("Coordenadas 1:", lat1, lon1)
    print("Coordenadas 2:", lat2, lon2)
    print("Tiempo (s):", tiempo_seg)
    print("Distancia (m):", distancia_m)
    print("-----")
    h, m, k = calcula_tiempo_distancia(tiempo_seg, distancia_m)
    print("Tiempo:", f"{h} horas {m} minutos")
    print("Distancia:", f"{k} km")
    print("-----")

if __name__ == "__main__":
    prueba1()
    prueba2()
    prueba3()
    prueba4()
