from arbol.registro import Registro
from arbol.nodo_interno import NodoInterno

class NodoHoja(): 
    def __init__(self, numero, paginador, tamaño_pagina, tamaño_registro, root, padre:int, cantidad_registros:int, registros):
        self.numero = numero
        self.paginador = paginador
        self.tamaño_pagina = tamaño_pagina
        self.tamaño_registro= tamaño_registro
        self.root = root
        self.padre = padre
        self.cantidad_registros = cantidad_registros
        self.registros = registros   
        
    @classmethod  
    def from_bytes(cls, data:bytearray, numero, paginador, tamaño_pagina, tamaño_registro):
        root = data[1]
        padre = int.from_bytes(data[2:6], byteorder='big')
        cantidad_registros = int.from_bytes(data[6:10])
        data_registros = data[10:]
        registros = {}
        count = 0
        for i in range(cantidad_registros):
            registro = Registro.from_bytes(data_registros[count+4: (count + tamaño_registro)], paginador.formato)
            key = int.from_bytes(data_registros[count:count+4])
            registros[key] = registro
            count= count + tamaño_registro
        return cls(numero, paginador, tamaño_pagina, tamaño_registro, root, padre, cantidad_registros, registros)
             
    def insert(self, registro):
        if registro.id in self.registros:
            print("Clave repetida")
        else:
            if self.cantidad_registros < ((self.tamaño_pagina - 10) // 295):
                self.registros[registro.id] = registro
                self.cantidad_registros += 1
                print("INSERT exitoso")
            else:
                self.registros[registro.id] = registro
                self.cantidad_registros += 1
                self.split()
                
    def split(self):
        cant_registros = (self.cantidad_registros + 1) // 2
        nodo_izq = NodoHoja(1, self.paginador, self.tamaño_pagina, self.tamaño_registro, 
                            False, self.numero, cant_registros, 
                            {k: self.registros[k] for k in list(self.registros)[:cant_registros]})
        nodo_der = NodoHoja(2, self.paginador, self.tamaño_pagina, self.tamaño_registro, 
                            False, self.numero, cant_registros, 
                            {k: self.registros[k] for k in list(self.registros)[cant_registros:]})
        nodo_interno = NodoInterno(self.numero, self.paginador, True, 0, 1, nodo_der.numero,
                                   {nodo_izq.ultima_clave() : nodo_izq.numero})
        self.paginador.paginas[0] = nodo_interno
        self.paginador.paginas[1] = nodo_izq
        self.paginador.paginas[2] = nodo_der
        print("INSERT exitoso con split")
        
    def ultima_clave(self):
        return self.registros[self.cantidad_registros] 
                              
    def select(self):
        for registro in self.registros.values():
            registro.contenido()
    
    def metadata(self):
        return (1, self.cantidad_registros)
