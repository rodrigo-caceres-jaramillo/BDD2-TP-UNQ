import struct

class Nodo:
    def __init__(self, tipo=1, root=1, padre=0, cantidad_registros=0, registros={}):
        self.tipo = tipo
        self.root = root
        self.padre = padre
        self.cantidad_registros = cantidad_registros
        self.registros = registros
        
    @classmethod   
    def from_bytes(cls, data):    
        tipo = data[0]
        root = data[1]
        padre = int.from_bytes(data[2:6])
        cantidad_registros = int.from_bytes(data[6:10])
        data_registros = data[10:]
        registros = {}
        for i in range(cantidad_registros):
            key, registro = struct.unpack('!I291s', data_registros[i:i+295])
            registros[key] = registro
        return cls(tipo, root, padre, cantidad_registros, registros)
    
    def to_bytes(self):
        tipo_bytes = int(self.tipo).to_bytes(1)
        root_bytes = int(self.root).to_bytes(1)
        padre_bytes = int(self.padre).to_bytes(4)
        cantidad_registros_bytes = int(self.cantidad_registros).to_bytes(4)
        registros_bytes = b''
        for clave, valor in self.registros.items():
            registro_bytes = int(clave).to_bytes(4) + valor
            registros_bytes = registros_bytes + registro_bytes

        bytes = tipo_bytes + root_bytes + padre_bytes + cantidad_registros_bytes + registros_bytes
        return bytes + b"\00"* (4096 - len(bytes))
            
    def insert(self, registro):
        if self.cantidad_registros == 13:
            return False
        if self.cantidad_registros == 0:
            key = 0
        else:
            key = self.cantidad_registros
        self.registros[key] = registro
        self.cantidad_registros= self.cantidad_registros + 1
        return True
        
    def select(self):
         for registro in self.registros.values():
            id, nombre, email = struct.unpack('>I32s255s', registro)
            nombre = nombre.decode('utf-8').rstrip('\x00')
            email = email.decode('utf-8').rstrip('\x00')
            print(f"{id} {nombre} {email}")
        