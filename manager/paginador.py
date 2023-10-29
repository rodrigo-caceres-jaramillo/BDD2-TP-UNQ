import os
from arbol.nodo_hoja import NodoHoja
from arbol.nodo_interno import NodoInterno
from manager.codificador import Codificador

class Paginador:
    def __init__(self, nombre_archivo, pagina_t):
        self.nombre_archivo = nombre_archivo
        self.pagina_t = pagina_t
        self.paginas= {0:self.cargar_pagina(0)}
        self.codificador= Codificador(pagina_t)
        
    def cargar_pagina(self, numPag):
        if not os.path.exists(self.nombre_archivo) or os.path.getsize(self.nombre_archivo) == 0:
            return NodoHoja(0, self, self.pagina_t ,True, 0, 0, {})
        else:
            with open(self.nombre_archivo, 'rb') as archivo:
                posicionInicial = self.pagina_t * (numPag)
                data = archivo.read()[posicionInicial: posicionInicial + self.pagina_t]
                if data[0] == 1:
                    return NodoHoja.from_bytes(data, 0, self, self.pagina_t)
                else:
                    return NodoInterno.from_bytes(data, 0, self, self.pagina_t)
                
    def get_page(self, numPag):
        pagina = self.paginas.get(numPag)
        if (pagina) is None:
            self.paginas[numPag] = self.cargar_pagina(numPag)
            return self.paginas.get(numPag)
        else:
            return pagina
                
    def insert(self, key, registro, numPag=0):
        pagina = self.get_page(numPag)
        pagina.insert(key, registro)
     
    def select(self, numPag=0):
        pagina = self.get_page(numPag)
        pagina.select()
        
    def metadata(self, numPag=0):
        pagina = self.get_page(numPag)
        return pagina.metadata()

    def commit(self):
        with open(self.nombre_archivo, "ab+") as archivo:
            archivo.write(self.codificador.codificar_nodo(self.paginas.get(0)))