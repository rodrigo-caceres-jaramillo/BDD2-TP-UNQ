from arbol.registro import Registro
from arbol.nodo_interno import NodoInterno

class NodoHoja(): 
    def __init__(self, numero, paginador, tamaño, root, padre:int, cantidad_registros:int, registros):
        self.numero = numero
        self.paginador = paginador
        self.tamaño = tamaño
        self.root = root
        self.padre = padre
        self.cantidad_registros = cantidad_registros
        self.registros = registros   
        
    @classmethod  
    def from_bytes(cls, data:bytearray, numero, paginador, tamaño):
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
        return cls(numero, paginador, tamaño, root, padre, cantidad_registros, registros)
             
    def insert(self, key, registro):
        if key in self.registros:
            print("Clave repetida")
        else:
            print(key)
            if self.cantidad_registros < ((self.tamaño - 10) // 295):
                self.registros[key] = registro
                self.cantidad_registros += 1
            else:
                self.registros[key] = registro
                self.cantidad_registros += 1
                self.split()
                
    def split(self):
        cant_registros = (self.cantidad_registros + 1) // 2
        nodo_izq = NodoHoja(1, self.paginador, False, self.numero, cant_registros, 
                            {k: self.registros[k] for k in list(self.registros)[:cant_registros]})
        nodo_der = NodoHoja(2, self.paginador, False, self.numero, cant_registros, 
                            {k: self.registros[k] for k in list(self.registros)[cant_registros:]})
        nodo_interno = NodoInterno(self.numero, self.paginador, True, 0, 1, nodo_der.numero,
                                   {nodo_izq.ultima_clave() : nodo_izq.numero})
        self.paginador.paginas[0] = nodo_interno
        self.paginador.paginas[1] = nodo_izq
        self.paginador.paginas[2] = nodo_der
        
    def ultima_clave(self):
        return self.registros[self.cantidad_registros] 
                              
    def select(self):
        for registro in self.registros.values():
            registro.contenido()
    
    def metadata(self):
        return (1, self.cantidad_registros)
