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
            key = int.from_bytes(data_registros[count:count+4], byteorder='big')
            registro_data = data_registros[count+4: (count + 4 + tamaño_registro)]
            registro = Registro.from_bytes(registro_data, paginador.formato)
            registros[key] = registro
            count += 4 + tamaño_registro
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
        cant_registros_izq = self.cantidad_registros // 2
        cant_registros_der = self.cantidad_registros - cant_registros_izq
        registros_izq = {k: self.registros[k] for k in list(self.registros)[:cant_registros_izq]}
        registros_der = {k: self.registros[k] for k in list(self.registros)[cant_registros_izq:]}
        
        if(self.root): 
            numero_izq = self.paginador.siguiente_numero() 
            nodo_izq = self.crear_hoja(numero_izq, self.numero, cant_registros_izq, registros_izq)
            numero_der = self.paginador.siguiente_numero() 
            nodo_der = self.crear_hoja(numero_der, self.numero, cant_registros_der, registros_der)
            root = NodoInterno(self.numero, self.paginador, self.tamaño_pagina, self.tamaño_registro, 
                           True, 0, 1, nodo_der.numero,
                           {nodo_izq.numero : nodo_izq.ultima_clave()}, True)
            self.paginador.paginas[self.numero] = root
        else:
            nodo_izq = self.crear_hoja(self.numero, self.padre, cant_registros_izq, registros_izq)
            numero_der = self.paginador.siguiente_numero() 
            nodo_der = self.crear_hoja(numero_der, self.padre, cant_registros_der, registros_der)
            nodo_interno = self.paginador.get_page(self.padre)
            nodo_interno.agregar_puntero(self.numero, nodo_der.numero, nodo_izq.numero, nodo_izq.ultima_clave())
        print("INSERT exitoso con split")
        
    def crear_hoja(self, numero, padre, cant_registros, registros):
        nodo = NodoHoja(numero, self.paginador, self.tamaño_pagina, self.tamaño_registro, 
                    False, padre, cant_registros, registros, True)
        self.paginador.paginas[numero] = nodo
        return nodo 
        
    def ultima_clave(self):
        if self.cantidad_registros > 0:
            return max(self.registros.keys())
        else:
            print("No hay registros en el nodo.")
            return None
                              
    def select(self):
        print(self.numero)
        for registro in self.registros.values():
            registro.contenido()
    
    def metadata(self):
        return (1, self.cantidad_registros)
