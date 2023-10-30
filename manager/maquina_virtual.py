from .compilador import Compilador
from .tabla import Tabla

class MaquinaVirtual:
    def __init__(self, nombre_carpeta):
        self.compilador = Compilador(self)
        self.tabla = Tabla(nombre_carpeta)
        
    def iniciar(self):
        while True:
            entrada = input("sql>")
            self.compilador.interpretar(entrada)
            
    def create(self, tamaño_pag, formato):
        self.tabla.create(formato, tamaño_pag)
    
    def insert(self, campos):
        self.tabla.insert(campos)

    def select(self):
        self.tabla.select()
            
    def exit(self):
        self.tabla.commit()
        print("Termindado")
        exit()

    def metadata(self):
        metadata = self.tabla.metadata()
        print("Paginas: "+ str(metadata[0]) + "\n" + "Registros: " + str(metadata[1]))
