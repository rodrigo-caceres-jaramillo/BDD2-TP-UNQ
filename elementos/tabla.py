from .registro import Registro
from .paginador import Paginador

class Tabla:
    def __init__(self, archivo):
        self.paginador = Paginador(archivo)
    
    def insert(self, id, usuario, email):
        registro = Registro(int(id), usuario, email)
        pagina = self.paginador.pagina_actual()
        pagina.insert(bytes(registro))
        
    def select(self):
        for pagina in self.paginador.todas():
            pagina.contenido()
            
    def commit(self):
        self.paginador.commit()
            
    def metadata(self):
        self.paginador.metadata()