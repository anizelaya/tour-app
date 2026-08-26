class Cliente:
    def __init__(self, nombre: str, idioma: str = "Español", hospedaje: str = "", telefono: str = ""):
        self.nombre = nombre
        self.idioma = idioma
        self.hospedaje = hospedaje
        self.telefono = telefono