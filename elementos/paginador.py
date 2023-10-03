from .nodo import Nodo
import os

class Paginador:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        if not os.path.exists(nombre_archivo) or os.path.getsize(nombre_archivo) == 0:
            self.arbol = [Nodo()]
        else:
            with open(nombre_archivo, 'rb') as archivo:
                self.arbol = [Nodo.from_bytes(archivo.read())]
        
    def get_pagina_actual(self):  
        return self.arbol[0]
    
    def get_pagina(self, numero):
        return self.arbol[numero]
     
    def commit(self):
        with open(self.nombre_archivo, "ab+") as archivo:
            archivo.write(self.arbol[0].to_bytes())
        
    def metadata(self):
        return (1, self.arbol[0].cantidad_registros)
