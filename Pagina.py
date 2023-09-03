class Pagina:
    def __init__(self):
        self.capacidad = 4064
        self.registros = []

    def agregar_registro(self, registro):
        if self.capacidad >= registro.tamaño():
            self.registros.append(registro)
            self.capacidad -= registro.tamaño()
            return True
        else:
            return False

    def contenido(self):
        for registro in self.registros:
            registro.contenido()
