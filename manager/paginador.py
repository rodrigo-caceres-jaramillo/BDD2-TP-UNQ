import os
from arbol.nodo_hoja import NodoHoja
from arbol.nodo_interno import NodoInterno
from manager.codificador import Codificador

class Paginador:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.arbol= [self.crear_arbol()]
        self.codificador= Codificador()
    
    def crear_arbol(self):
        if not os.path.exists(self.nombre_archivo) or os.path.getsize(self.nombre_archivo) == 0:
            return NodoHoja(True, True, 0, 0, {})
        else:
            with open(self.nombre_archivo, 'rb') as archivo:
                data = archivo.read()[0: 4096]
                if data[0] == 1:
                    return NodoHoja.from_bytes(data)
                else:
                    return  NodoInterno.from_bytes(data)
                
    def insert(self, key, registro):
        self.arbol[0].insert(key, registro)
     
    def select(self):
        self.arbol[0].select()
        
    def metadata(self):
        return self.arbol[0].metadata()

    def commit(self):
        with open(self.nombre_archivo, "ab+") as archivo:
            archivo.write(self.codificador.codificar_nodo(self.arbol[0]))