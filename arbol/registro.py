import struct

class Registro:
    def __init__(self, id:int, nombre, email):
        self.id = id
        self.nombre = nombre
        self.email = email
    
    @classmethod  
    def from_bytes(cls, data):
        id, nombre, email = struct.unpack('>I32s255s', data)
        nombre = nombre.decode('utf-8').rstrip('\x00')
        email = email.decode('utf-8').rstrip('\x00')
        return cls(id, nombre, email)
    
    def to_bytes(self):
        id_codificado = self.id.to_bytes(4, byteorder="big")
        nombre_bytes = self.nombre.encode('ascii') + b"\x00" * (32 - len(self.nombre.encode('ascii')))
        email_bytes = self.email.encode('ascii') + b"\x00" * (255 - len(self.email.encode('ascii')))

        return id_codificado + nombre_bytes + email_bytes
    
    def contenido(self):
        print(f"{self.id} {self.nombre} {self.email}")