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
         
    def insert(self, registro):
        nodo = self.buscarRamaPara(registro)
        nodo.insert(registro)

    def buscarRamaPara(self, registro):
        keys = list(self.punteros.keys())
        keys.sort()

        for key in keys:
            if int(registro.id) <= int(self.punteros[key]):
                numero_pagina = self.punteros[key]
                return self.paginador.get_page(numero_pagina)
        return self.paginador.get_page(self.hijo_derecho)
    
    def agregar_puntero(self, num_original, num_der, num_izq, ultima_clave):
        self.punteros[num_izq] = ultima_clave
        self.cantidad_claves += 1
        if(self.hijo_derecho == num_original):
            self.hijo_derecho = num_der
        if(self.cantidad_claves > ((self.tamaño_pagina - 14) // 8)):
            self.split()
            
    def split(self):
        cant_punteros_izq = self.cantidad_claves // 2
        cant_punteros_der = self.cantidad_claves - cant_punteros_izq
        punteros_izq = {k: self.punteros[k] for k in list(self.punteros)[:cant_punteros_izq]}
        print(punteros_izq)
        punteros_der = {k: self.punteros[k] for k in list(self.punteros)[cant_punteros_der:]}
        print(punteros_der)
        
        if(self.root):
            numero_izq = self.paginador.siguiente_numero()
            numero_der = self.paginador.siguiente_numero()  
            nodo_izq = self.crear_interno(numero_izq, self.numero,cant_punteros_izq, punteros_izq, numero_der)
            nodo_der = self.crear_interno(numero_der, self.numero,cant_punteros_der, punteros_der, self.hijo_derecho)
            self.crear_root(nodo_izq, nodo_der)
        else:
            print("caso 2 de split")
            numero_der = self.paginador.siguiente_numero() 
            nodo_izq = self.crear_interno(self.numero, self.padre, cant_punteros_izq, punteros_izq, numero_der)
            nodo_der = self.crear_interno(numero_der, self.padre, cant_punteros_der, punteros_der, self.hijo_derecho)
            nodo_der.actualizar_hijos()
            nodo_interno = self.paginador.get_page(self.padre)
            nodo_interno.agregar_puntero(self.numero, nodo_der.numero, nodo_izq.numero, nodo_izq.ultima_clave())
            
    def crear_interno(self, numero, padre, cantidad_claves, punteros, hijo_derecho):
        nodo = NodoInterno(numero, self.paginador, self.tamaño_pagina, self.tamaño_registro, 
                           False, padre, cantidad_claves, hijo_derecho, punteros, True)
        self.paginador.paginas[numero] = nodo
        nodo.actualizar_hijos()
        nodo.select()
        return nodo 
    
    def actualizar_hijos(self):
        hijos = list(self.punteros.keys())
        hijos.append(self.hijo_derecho)
        for key in hijos:
            hijo = self.paginador.get_page(key)
            hijo.padre = self.numero
            hijo.modificado = True
            
    def ultima_clave(self):
        nodo = self.paginador.get_page(self.hijo_derecho)
        return nodo.ultima_clave()
          
    def crear_root(self, nodo_izq, nodo_der):
        root = NodoInterno(self.numero, self.paginador, self.tamaño_pagina, self.tamaño_registro, 
                           True, 0, 1, nodo_der.numero, {nodo_izq.numero : nodo_izq.ultima_clave()})
        self.paginador.paginas[self.numero] = root
          
    def select(self):
        hijos = list(self.punteros.keys())
        hijos.append(self.hijo_derecho)
        for hijo in hijos:
            self.paginador.select(hijo)
            
    def metadata(self):
        paginas, registros= 1, 0
        hijos = list(self.punteros.keys())
        hijos.append(self.hijo_derecho)
        for hijo in hijos:
            h_pagina, h_registros= self.paginador.metadata(hijo)
            paginas += h_pagina
            registros += h_registros
        return (paginas, registros)