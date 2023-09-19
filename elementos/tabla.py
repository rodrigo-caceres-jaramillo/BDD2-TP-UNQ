import struct
from .paginador import Paginador

class Tabla:
    def __init__(self, nombre_archivo):
        self.paginador = Paginador(nombre_archivo)
    
    def insert(self, id, nombre, email):
        registro = struct.pack('>I32s255s', id, nombre.encode('utf-8'), email.encode('utf-8'))
        pagina = self.paginador.pagina_actual()
        pagina.insert(bytes(registro))
        
    def select(self):
        for pagina in self.paginador.todas():
            pagina.contenido()
            
    def commit(self):
        self.paginador.commit()
            
    def metadata(self):
        return self.paginador.metadata()