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
        self.pagina_actual = self.get_pagina(self.paginas - 1)
    
    def obtener_atributos(self):
        self.tamaño = os.path.getsize(self.nombre_archivo)
        if (self.tamaño % 4096 == 0):
            self.paginas = int(self.tamaño / 4096)
        elif (self.tamaño == 0):
            self.paginas = 0
        else:
            self.paginas = int(self.tamaño / 4096) + 1
        self.registros = (self.tamaño % 4096) // 291
    
    def sumar_registro(self):
        self.tamaño = self.tamaño + 291
        self.registros = self.registros + 1
    
    def crear_archivo(self):
        with open(self.nombre_archivo, "ab+") as file:
            pass
            #print("Archivo creado")
        
    def get_pagina_actual(self):
        if self.pagina_actual.cantidad_registros >= 14:
            nueva_pagina = Pagina(bytearray())
            self.cache[self.paginas] = nueva_pagina
            self.paginas = self.paginas + 1
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
        posicion = 4096*(self.paginas - 1)
        with open(self.nombre_archivo, "rb") as archivo:
            bytes_pagina = archivo.read()[posicion:posicion+4096]
            self.cache[numero] = Pagina(bytes_pagina)
     
    def commit(self):
        if len(self.cache) == 0:
            pass
        else:
            with open(self.nombre_archivo, "ab+") as archivo:
                for numero, pagina in self.cache.items():
                    if pagina.modificado:
                        archivo.seek(numero * 4096)
                        for registro in pagina.registros:
                            archivo.write(registro)
                    pagina.modificado = False
            
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
    
    def abrir_archivo(self):
        self.file = open(self.nombre_archivo, 'rb')

    def cerrar_archivo(self):
        if hasattr(self, 'file') and self.file is not None:
            self.file.close()
            self.file = None
