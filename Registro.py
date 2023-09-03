class Registro:
    def __init__(self, id, nombre, email):
        self.tamaño = 291
        self.id = id
        self.nombre = nombre
        self.email = email

    def contenido(self):
        print(f"{self.id} {self.nombre} {self.email}")
