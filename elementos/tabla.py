from .registro import Registro
from .pagina import Pagina

class Tabla:
    def __init__(self):
        self.paginas = []
        self.pagina_actual = None
    
    def agregar_registro(self, id, usuario, email):
        registro = Registro(int(id), usuario, email)
        if len(self.paginas) == 0 or not self.pagina_actual.agregar_registro(bytes(registro)):
            nueva_pagina = Pagina()
            self.paginas.append(nueva_pagina)
            self.pagina_actual = nueva_pagina
            self.pagina_actual.agregar_registro(bytes(registro))
        print("INSERT exitoso")
            
    def seleccionar_registros(self):
        for pagina in self.paginas:
            pagina.contenido()
            
    def metadata(self):
        reg = 0
        for pagina in self.paginas:
            for registro in pagina.registros:
                reg = reg + 1
               
        print(f"Paginas:{len(self.paginas)}\nRegistros:{reg}")