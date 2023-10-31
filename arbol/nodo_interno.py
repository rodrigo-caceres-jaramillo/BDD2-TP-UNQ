class NodoInterno():
    def __init__(self, numero, paginador, tamaño_pagina, tamaño_registro, root:bool, padre:int, cantidad_claves:int, hijo_derecho: int, punteros={}, modificado=False):
        self.numero = numero
        self.paginador = paginador
        self.tamaño_pagina = tamaño_pagina
        self.tamaño_registro= tamaño_registro
        self.root = root
        self.padre = padre
        self.cantidad_claves = cantidad_claves
        self.hijo_derecho = hijo_derecho
        self.punteros = punteros
        self.modificado = modificado
        
    @classmethod  
    def from_bytes(cls, data:bytearray, numero, paginador, tamaño_pagina, tamaño_registro):    
        root = data[1]
        padre = int.from_bytes(data[2:6], byteorder='big')
        cantidad_claves = int.from_bytes(data[6:10], byteorder='big')
        hijo_derecho = int.from_bytes(data[10:14], byteorder='big')
        data_punteros = data[14:]
        punteros = {}
        count = 0
        for i in range(cantidad_claves):
            clave = int.from_bytes(data_punteros[count:count+4])
            puntero = data_punteros[count+4:count+8]
            punteros[clave] = puntero
            count= count + 8
        return cls(numero, paginador, tamaño_pagina, tamaño_registro, root, padre, cantidad_claves, hijo_derecho, punteros)   
         
    def insert(self, key, registro):
        if self.cantidad_claves == ((self.tamaño_pagina - 14) // 8):
            print("nodo interno lleno")
        else:
            if(key > self.punteros[0]):
                pagina=self.paginador.get_page(self.punteros[0])
            
            else:
                pagina=self.paginador.get_page(self.hijo_derecho)
            
    def select(self):
        hijos = list(self.punteros.values())
        for hijo in hijos.append(self.hijo_derecho):
            self.paginador.select(hijo)
            
    def metadata(self):
        paginas, registros= 1, 0
        hijos = list(self.punteros.values())
        for hijo in hijos.append(self.hijo_derecho):
            h_pagina, h_registros= self.paginador.metadata(hijo)
            paginas += h_pagina
            registros += h_registros
        return (paginas, registros)