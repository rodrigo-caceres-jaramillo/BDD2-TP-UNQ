import struct
from .paginador import Paginador

class Tabla:
    def __init__(self, nombre_archivo):
        self.paginador = Paginador(nombre_archivo)
    
    def insert(self, id, nombre, mail):
        registro = self.codificar_registro(id, nombre, mail)
        pagina = self.paginador.get_pagina_actual()
        if (pagina.insert(bytes(registro))):
            self.paginador.sumar_registro()
            print("INSERT exitoso")
        
    def select(self):
        for pagina in self.paginador.todas():
            pagina.contenido()
            
    def commit(self):
        self.paginador.commit()
        self.paginador.cerrar_archivo()
            
    def metadata(self):
        return self.paginador.metadata()
    
    def codificar_registro(self, id, nombre, mail):
        id_codificado = int(id).to_bytes(4, byteorder="big")
        nombre_bytes = bytes(nombre, "ascii")
        nombre_codificado = nombre_bytes + b"\00"* (32 - len(nombre_bytes))
        mail_bytes = bytes(mail, "ascii")
        mail_codificado = mail_bytes + b"\00"* (255 - len(mail_bytes))
        
        return id_codificado + nombre_codificado + mail_codificado