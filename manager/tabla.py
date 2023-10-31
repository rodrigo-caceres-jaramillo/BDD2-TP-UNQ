from .paginador import Paginador

class Tabla:
    def __init__(self, nombre_carpeta):    
        self.paginador = Paginador(nombre_carpeta)
        
    def create(self, formato):
        self.paginador.create(formato)

    def insert(self, campos):
        self.paginador.insert(campos)
                
    def select(self):
        self.paginador.select()
            
    def commit(self):
        self.paginador.commit()
            
    def metadata(self):
        return self.paginador.metadata()