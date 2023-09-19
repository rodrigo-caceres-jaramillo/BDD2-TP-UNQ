from .pagina import Pagina
import os

class Paginador:
    def __init__(self, nombre_archivo):
        self.cache = {}
        self.nombre_archivo = nombre_archivo
        if not os.path.exists(nombre_archivo):
            self.tamaño = 0
            self.paginas = 1
            self.registros = 0
            self.crear_archivo()
        else:
            self.obtener_atributos()
        print(self.tamaño)
        print(self.paginas - 1)
        self.pagina_actual = self.get_pagina(self.paginas - 1)
    
    def obtener_atributos(self):
        self.tamaño = os.path.getsize(self.nombre_archivo)
        if self.tamaño == 0:
            self.paginas = 1
        else:
            self.paginas = self.tamaño // 4096
        self.registros = (self.tamaño % 4096) // 291
    
    def crear_archivo(self):
        with open(self.nombre_archivo, "ab+") as file:
            print("Archivo creado")
        
    def get_pagina_actual(self):
        if self.pagina_actual.cantidad_registros >= 14:
            nueva_pagina = Pagina(b'\x00' * 4096)
            self.cache[self.paginas] = nueva_pagina
            self.paginas += 1
            self.pagina_actual = nueva_pagina
        return self.pagina_actual
    
    def get_pagina(self, numero):
        pagina = self.cache.get(numero)
        if (pagina) is None:
            self.cargar_pagina(numero)
            return self.cache.get(numero)
        else:
            return pagina

    def cargar_pagina(self, numero):
        with open(self.nombre_archivo, "rb") as archivo:
            archivo.seek(numero * 4096)
            bytes_pagina = archivo.read(4096)
            self.cache[numero] = Pagina(bytes_pagina)
    
    def getRegistros(self):
        with open(self.nombre_archivo, "rb") as baseDeDatos:
            return baseDeDatos.read()
     
    def commit(self):
        pass
    
    def todas(self):
        self.cargar_todas_las_paginas()
        return self.cache.values()
    
    def cargar_todas_las_paginas(self):
        cont = 0
        while cont < self.paginas:
            pagina = self.cache.get(cont)
            if pagina is None:
                self.cargar_pagina(cont)
            cont += 1
        
    def metadata(self):
        return (self.paginas, self.registros)