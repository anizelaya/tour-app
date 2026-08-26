class Experiencia:
    def __init__(self, nombre: str, precio_neto: float, tipo: str):
        self.nombre = nombre
        self.precio_neto = precio_neto
        self.tipo = tipo  # Degustación, Almuerzo, Sunset, Cafetería


class Bodega:
    def __init__(self, nombre: str, zona: str, km_desde_ciudad: int, imagen_url: str = ""):
        self.nombre = nombre
        self.zona = zona
        self.km_desde_ciudad = km_desde_ciudad
        self.imagen_url = imagen_url
        self.experiencias = []

    def agregar_experiencia(self, experiencia: Experiencia):
        self.experiencias.append(experiencia)