import struct


class Pagina:
    def __init__(self, bytes):
        self.registros = []
        self.cantidad_registros = len(bytes) // 291
        for i in range(0, len(bytes), 291):
            registro_bytes = bytes[i:i+291]
            self.registros.append(registro_bytes)
            
    def insert(self, registro):
        self.registros.append(registro)
        self.cantidad_registros= self.cantidad_registros + 1
        print(self.cantidad_registros)
        return True
        
    def contenido(self):
         for registro in self.registros:
            id, nombre, email = struct.unpack('>I32s255s', registro)
            nombre = nombre.decode('utf-8').rstrip('\x00')
            email = email.decode('utf-8').rstrip('\x00')
            print(f"{id} {nombre} {email}")