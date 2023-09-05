class Pagina:
    def __init__(self):
        self.capacidad = bytearray(4064)
        self.espacio_disponible = 4064
        self.registros = []

    def agregar_registro(self, registro):
        if len(registro) > self.espacio_disponible:
            return False
        else:
            self.capacidad[4064 - self.espacio_disponible:] = registro
            self.espacio_disponible -= len(registro)
            self.registros.append(registro)
            return True
        
    def contenido(self):
         for registro in self.registros:
                print(f"{int.from_bytes(registro[:4], 'big')} {registro[4:36].decode('ascii').strip()} {registro[36:291].decode('ascii').strip()}")