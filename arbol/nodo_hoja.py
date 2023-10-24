from arbol.registro import Registro
from arbol.nodo_interno import NodoInterno

class NodoHoja(): 
    def __init__(self, tipo, root, padre:int, cantidad_registros:int, registros={}):
        self.tipo = tipo
        self.root = root
        self.padre = padre
        self.cantidad_registros = cantidad_registros
        self.registros = registros
        
    @classmethod  
    def from_bytes(cls, data:bytearray):
        tipo = data[0]
        root = data[1]
        padre = int.from_bytes(data[2:6], byteorder='big')
        cantidad_registros = int.from_bytes(data[6:10])
        data_registros = data[10:]
        registros = {}
        count = 0
        for i in range(cantidad_registros):
            registro = Registro.from_bytes(data_registros[count+4:count+295])
            key = int.from_bytes(data_registros[count:count+4])
            registros[key] = registro
            count= count + 295
        return cls(tipo, root, padre, cantidad_registros, registros)
             
    def insert(self, key, registro):
        if key in self.registros:
            print("Clave repetida")
        else:
            print(key)
            if self.cantidad_registros < 13:
                self.registros[key] = registro
                self.cantidad_registros += 1
            else:
                self.split(key, registro)
                nodo1, key1, nodo2, key2 = self.split()
                nuevo_interno = NodoInterno(1, self.root, self.padre, 1, 1, dict({}))
            
                 
    def select(self):
        for registro in self.registros.values():
            registro.contenido()
    
    def metadata(self):
        return (1, self.cantidad_registros)
    
    def split(self):
        cant_registros= (self.cantidad_registros + 1) // 2
        nodo_izq = NodoHoja(1, 0, 0, 0, self.registros[:cant_registros])
        nodo_der = NodoHoja(1, 0, 0, 0, self.registros[cant_registros:])

        nodo_interno = NodoInterno(0, 1, 0, 1, 2, dict(1:))
        return nuevo_nodo1, nueva_clave, nuevo_nodo2