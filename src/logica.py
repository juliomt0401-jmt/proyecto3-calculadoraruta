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
