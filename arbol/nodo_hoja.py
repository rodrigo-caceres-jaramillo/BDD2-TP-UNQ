from arbol.registro import Registro
from arbol.nodo_interno import NodoInterno

class NodoHoja(): 
    def __init__(self, numero, paginador, tamaño_pagina, tamaño_registro, root:bool, padre:int, cantidad_registros:int, registros, modificado=False):
        self.numero = numero
        self.paginador = paginador
        self.tamaño_pagina = tamaño_pagina
        self.tamaño_registro= tamaño_registro
        self.root = root
        self.padre = padre
        self.cantidad_registros = cantidad_registros
        self.registros = registros
        self.modificado = modificado
        
    @classmethod  
    def from_bytes(cls, data:bytearray, numero, paginador, tamaño_pagina, tamaño_registro):
        root = data[1]
        padre = int.from_bytes(data[2:6], byteorder='big')
        cantidad_registros = int.from_bytes(data[6:10], byteorder='big')
        data_registros = data[10:]
        registros = {}
        count = 0
        for i in range(cantidad_registros):
            print(tamaño_registro)
            key = int.from_bytes(data_registros[count:count+4], byteorder='big')
            registro_data = data_registros[count+4: (count + 4 + tamaño_registro)]
            registro = Registro.from_bytes(registro_data, paginador.formato)
            registros[key] = registro
            count += 4 + tamaño_registro
            print(count)
        return cls(numero, paginador, tamaño_pagina, tamaño_registro, root, padre, cantidad_registros, registros)
             
    def insert(self, registro):
        if registro.id in self.registros:
            print("Clave repetida")
        else:
            if self.cantidad_registros < ((self.tamaño_pagina - 10) // (self.tamaño_registro + 4)):
                self.registros[registro.id] = registro
                self.cantidad_registros += 1
                self.modificado = True
                print("INSERT exitoso")
            else:
                self.registros[registro.id] = registro
                self.cantidad_registros += 1
                self.split()
                
    def split(self):
        print("entra en split")
        print("Mis registros:", self.cantidad_registros)
        cant_registros_izq = self.cantidad_registros // 2
        cant_registros_der = self.cantidad_registros - cant_registros_izq
        print("registros para cada hoja:", cant_registros_izq, cant_registros_der)
    
        registros_izq = {k: self.registros[k] for k in list(self.registros)[:cant_registros_izq]}
        registros_der = {k: self.registros[k] for k in list(self.registros)[cant_registros_izq:]}

        nodo_izq = NodoHoja(1, self.paginador, self.tamaño_pagina, self.tamaño_registro, 
                    False, self.numero, cant_registros_izq, registros_izq, True)
        print("cantidad de registros en nodo_izq:", len(nodo_izq.registros))
        nodo_izq.select()

        nodo_der = NodoHoja(2, self.paginador, self.tamaño_pagina, self.tamaño_registro, 
                    False, self.numero, cant_registros_der, registros_der, True)
        print("cantidad de registros en nodo_der:", len(nodo_der.registros))
        nodo_der.select()

        nodo_interno = NodoInterno(self.numero, self.paginador, self.tamaño_pagina, self.tamaño_registro, 
                           True, 0, 1, nodo_der.numero,
                           {nodo_izq.ultima_clave(): nodo_izq.numero}, True)
        self.paginador.paginas[0] = nodo_interno
        self.paginador.paginas[1] = nodo_izq
        self.paginador.paginas[2] = nodo_der
        self.modificado = True
        print("INSERT exitoso con split")
        
    def ultima_clave(self):
        if self.cantidad_registros > 0:
            return max(self.registros.keys())
        else:
            print("No hay registros en el nodo.")
            return None
                              
    def select(self):
        for registro in self.registros.values():
            registro.contenido()
    
    def metadata(self):
        return (1, self.cantidad_registros)
