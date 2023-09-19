from .pagina import Pagina
import os

class Paginador:
    def __init__(self, archivo):
        self.cache = dict
        self.archivo = archivo
        with open(self.archivo, "ab+") as baseDeDatos:
            self.tamanio = self.tamanio = os.path.getsize(self.archivo)
        print(self.tamanio)
        
    def pagina_actual(self):
        pass
    
    def get_page(self, numero):
        pagina = self.cache.get(numero)
        if (pagina) is None:
            self.cache[numero] = self.cargar_pagina(numero)
            return self.cache.get(numero)
        else:
            return pagina

    def cargar_pagina(self, numero):
        posicionInicial = 4096 * (numero - 1)
        with open(self.archivo, "rb") as baseDeDatos:
            pagina = Pagina(baseDeDatos.read()[posicionInicial:posicionInicial+4096])
        self.cache[numero] = pagina
    
    def getRegistros(self):
        with open(self.archivo, "rb") as baseDeDatos:
            return baseDeDatos.read()
     
    def commit(self):
        pass
    
    def todas(self):
        self.cargar_todas_las_paginas()
        return self.cache.values()
    
    def cargar_todas_las_paginas(self):
        cont = 0
        while cont < self.cantidad_de_paginas:
            pagina = self.cache.get(cont)
            if pagina is None:
                self.cargar_pagina(cont)
            cont += 1
    
    def cantidad_de_paginas(self):
        if (self.tamanio % 4096 == 0):
            return int(self.tamanio / 4096)
        else:
            return int(self.tamanio / 4096) + 1
    
    def cantidad_de_registros(self):
        if (self.tamanio % 4096 == 0):
            return self.cantidad_de_paginas() * 14
        else:
            return int(self.tamanio / 4096) * 14 + int((self.tamanio % 4096) / 291)
        
    def metadata(self):
        return self.cantidad_de_paginas, self.cantidad_de_registros