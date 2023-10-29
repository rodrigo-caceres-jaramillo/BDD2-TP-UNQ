from .paginador import Paginador
from arbol.registro import Registro

class Tabla:
    def __init__(self, nombre_archivo):
        self.paginador = Paginador(nombre_archivo, 1000)
    
    def insert(self, id, nombre, mail):
        return self.paginador.insert(id, Registro(id, nombre, mail))
                
    def select(self):
        self.paginador.select()
            
    def commit(self):
        self.paginador.commit()
            
    def metadata(self):
        return self.paginador.metadata()