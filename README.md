# Calculadora de Ruta

## Resumen

**Calculadora de Ruta** es una aplicación de escritorio desarrollada en Python con la librería Flet. Permite consultar el costo estimado de un servicio de transporte calculando la tarifa por tiempo y por distancia entre dos puntos geográficos, además de visualizar el trazado vial sobre un mapa interactivo.

## Finalidad

El proyecto tiene como objetivo estimar costos de traslado y mostrar la ruta óptima entre dos ubicaciones utilizando servicios REST de geocodificación y ruteo, integrando una interfaz gráfica moderna y responsiva orientada al entorno de escritorio en Windows.

## ¿Qué hace la aplicación?

* **Gestión de Pasos (Paso 1 a Paso 3):** Permite ingresar origen y destino, validar coordenadas y procesar los resultados financieros del viaje.
* **Cálculo de Tarifas:** Procesa la distancia métrica y el tiempo del recorrido obtenidos mediante la API para calcular las tarifas correspondientes por hora y por distancia en soles (`S/`).
* **Visualización Geográfica:** Despliega un mapa interactivo con marcadores de inicio/fin y traza la ruta vial completa (`PolylineLayer`) utilizando mosaicos base.
* **Manejo de Errores y Validaciones:** Controla entradas nulas, fallos de red o datos geográficos inválidos durante las peticiones a la API.

## Arquitectura del Proyecto

El código sigue una estructura modular para separar la interfaz gráfica, la lógica de negocio y las llamadas a servicios externos:

CalculadoraRuta/
│
├── src/
│   ├── calculadora_ruta_main.py   # Punto de entrada de la aplicación
│   ├── ui.py                      # Interfaz de usuario (Flet / Flet-Map)
│   ├── logica.py                  # Cálculos de tarifas y tiempos
│   ├── api.py                     # Consumo de la API de Geoapify (Routing)
│   └── configuracion.py           # Variables globales y credenciales
│
└── venv/                          # Entorno virtual de Python


* **`ui.py`:** Define los controles de la interfaz de usuario, eventos (`ver_ruta_click`, `nueva_consulta`) y componentes del mapa (`map.Map`, `map.TileLayer`, `map.PolylineLayer`, `map.MarkerLayer`).
* **`api.py`:** Administra las solicitudes HTTP `requests.get()` a Geoapify Routing API y extrae la información métrica (`distance`, `time`) y la geometría (`MultiLineString`).
* **`logica.py`:** Realiza las conversiones métricas (metros a kilómetros, segundos a minutos/horas) y aplica las fórmulas matemáticas para el costo total.

## Políticas de Integridad y Manejo de Datos

1. **Control de Parámetros Geográficos:** La función `evaluar_coordenadas` valida que las coordenadas no contengan valores `None` antes de despachar solicitudes HTTP.
2. **Consumo de Servicios de Mapas:** Utiliza proveedores de capas base que permiten consumo directo sin requerir encabezados restringidos de red (`TileLayer` orientado a proveedores abiertos como CartoDB).
3. **Manejo de Excepciones:** Todas las llamadas externas a la API están encapsuladas en bloques `try/except Exception` para evitar el colapso de la aplicación en caso de pérdida de conexión o respuestas inválidas (`statusCode 400`).
4. **Resguardo de API Keys:** Credenciales centralizadas en `configuracion.py` para desacoplar las llaves privadas del código fuente visual y de la lógica.

## Forma de Uso

1. **Paso 1:** Iniciar la aplicación y definir los puntos de origen y destino.
2. **Paso 2:** Confirmar la geocodificación de las ubicaciones ingresadas.
3. **Paso 3:** Revisar el desglose de resultados ("Tarifa por hora" y "Tarifa por distancia").
4. **Ver Ruta:** Presionar el botón **Ver ruta** para desplegar el mapa interactivo con la línea del recorrido y los marcadores.
5. **Nueva Consulta:** Reiniciar el formulario para realizar un nuevo cálculo.

## Requisitos Técnicos y Entorno de Desarrollo

### Requisitos de Software

* **Sistema Operativo:** Windows 11 Home (64 bits).
* **Entorno de Desarrollo:** Visual Studio Code configurado para usar la terminal `cmd` (`Command Prompt`).
* **Lenguaje:** Python 3.14+ instalado en el entorno virtual (`venv`).

### Librerías y Dependencias Python

* **`flet`** (v0.86+): Framework para la interfaz de usuario.
* **`flet-map`**: Módulo para la integración de componentes de mapas interactivos.
* **`requests`**: Cliente HTTP para el consumo de servicios REST.

### APIS y servicios web externas y gratuitas
El proyecto se sustenta en una seria de APIS de uso público y gratuito:
https://api.ipify.org
https://ipinfo.io
https://api.geoapify.com
    geoapify requiere que te inscribas para quie obtengas una API_KEY
https://a.basemaps.cartocdn.com/

### Configuración del Proyecto

1. Abrir la carpeta del proyecto en VS Code.
2. Activar el entorno virtual desde la terminal de `cmd`:
.\venv\Scripts\activate
3. Ejecutar la aplicación principal:
python src/calculadora_ruta_main.py
