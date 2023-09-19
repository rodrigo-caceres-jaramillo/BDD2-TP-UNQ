from .compilador import Compilador
from .tabla import Tabla

class MaquinaVirtual:
    def __init__(self, nombre_archivo):
        self.compilador = Compilador(self)
        self.tabla = Tabla(nombre_archivo)
        
    def iniciar(self):
        while True:
            entrada = input("sql>").split()
            self.compilador.interpretar(entrada)
    
    def insert(self, registro):
        self.tabla.insert(registro)

    def select(self):
        self.tabla.select()
            
    def exit(self):
        self.tabla.commit()
        print("Termindado")
        exit()

    def metadata(self):
        metadata = self.tabla.metadata()
        print("Paginas: "+ str(metadata[0]) + "\n" + "Registros: " + str(metadata[1]))
