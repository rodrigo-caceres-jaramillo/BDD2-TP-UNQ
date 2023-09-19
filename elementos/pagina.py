class Pagina:
    def __init__(self, datos):
        self.datos = datos
        self.capacidad = 4096

    def insert(self, registro):
        if (len(registro) + len(self.datos)) > self.capacidad: 
            return False
        else:
            self.datos.append(bytes(registro))
            return True
        
    def contenido(self):
         for registro in self.registros:
                print(f"{int.from_bytes(registro[:4], 'big')} {registro[4:36].decode('ascii').strip()} {registro[36:291].decode('ascii').strip()}")