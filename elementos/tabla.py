import struct
from .paginador import Paginador

class Tabla:
    def __init__(self, nombre_archivo):
        self.paginador = Paginador(nombre_archivo)
    
    def insert(self, id, nombre, mail):
        registro = struct.pack('>I32s255s', id, nombre.encode('utf-8'), mail.encode('utf-8'))
        pagina = self.paginador.get_pagina_actual()
        if (pagina.insert(bytes(registro))):
            self.paginador.sumar_registro()
            print("INSERT exitoso")
        
    def select(self):
        for pagina in self.paginador.todas():
            pagina.contenido()
            
    def commit(self):
        self.paginador.commit()
            
    def metadata(self):
        return self.paginador.metadata()