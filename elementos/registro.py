class Registro:
    def __init__(self, id, nombre, email):
        self.id = id.to_bytes(4, 'big')
        self.nombre = nombre.encode('ascii')
        self.email = email.encode('ascii')

    def __bytes__(self):
        return self.id + self.nombre.ljust(32) + self.email.ljust(255)
