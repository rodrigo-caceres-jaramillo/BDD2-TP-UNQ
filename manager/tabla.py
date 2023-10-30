from .paginador import Paginador

class Tabla:
    def __init__(self, nombre_carpeta):    
        self.paginador = Paginador(nombre_carpeta)
        
    def create(self, formato, tamaño):
        self.paginador.create(formato, tamaño)

    def insert(self, campos):
        self.paginador.insert(campos)
                
    def select(self):
        self.paginador.select()
            
    def commit(self):
        self.paginador.commit()
            
    def metadata(self):
        return self.paginador.metadata()