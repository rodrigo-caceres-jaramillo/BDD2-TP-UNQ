import os
from arbol.nodo_hoja import NodoHoja
from arbol.nodo_interno import NodoInterno
from manager.codificador import Codificador
import json
from arbol.registro import Registro

class Paginador:
    def __init__(self, nombre_carpeta):
        self.nombre_carpeta = nombre_carpeta
        self.formato = self.cargar_formato()
        self.paginas= {0:self.cargar_pagina(0)}
        
    def cargar_formato(self):
        ruta = os.path.join(self.nombre_carpeta, "metadata")
        if not os.path.exists(self.nombre_carpeta):
            os.makedirs(self.nombre_carpeta)
        if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
            return None
        else:
             with open(ruta, 'r') as archivo_formato:
                contenido = archivo_formato.read()
                return json.loads(contenido)
        
    def create(self, formato, tamano_pagina):
        self.formato = formato
        ruta = os.path.join(self.nombre_carpeta, "metadata")
        with open(ruta+".json", 'w') as archivo_formato:
            archivo_formato.write(json.dumps(self.formato))
        self.tamaño_pagina = tamano_pagina
        self.tamaño_registro = sum(info['size'] for info in self.formato.values())
        self.codificador= Codificador(self.tamaño_pagina)
        self.paginas = {0:self.cargar_pagina(0)}
        
              
    def cargar_pagina(self, numPag):
        ruta = os.path.join(self.nombre_carpeta, "data")
        if self.formato is None:
            return None
        else:
            if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
                return NodoHoja(0, self, self.tamaño_pagina, self.tamaño_registro, True, 0, 0, {})
            else:
                with open(ruta, 'rb') as archivo:
                    posicionInicial = self.tamaño_pagina * (numPag)
                    data = archivo.read()[posicionInicial: posicionInicial + self.tamaño_pagina]
                    if data[0] == 1:
                        return NodoHoja.from_bytes(data, 0, self, self.tamaño_pagina, self.tamaño_registro)
                    else:
                        return NodoInterno.from_bytes(data, 0, self, self.tamaño_pagina, self.tamaño_registro)
                
    def get_page(self, numPag):
        if self.formato is None:
            print("ERROR: No hay una tabla creada")
        else:
            pagina = self.paginas.get(numPag)
            if (pagina) is None:
                self.paginas[numPag] = self.cargar_pagina(numPag)
                return self.paginas.get(numPag)
            else:
                return pagina
                
    def insert(self, campos, numPag=0):
        if self.formato is None:
            print("ERROR: No hay una tabla creada")
        else:
            pagina = self.get_page(numPag)
            if(len(campos) == len(self.formato.keys())):
                registro = Registro(**dict(zip(self.formato.keys(), campos)))
                pagina.insert(registro)
            else:
                print("ERROR: Formato incorrecto")
     
    def select(self, numPag=0):
        if self.formato is None:
            print("ERROR: No hay una tabla creada")
        else:
            pagina = self.get_page(numPag)
            pagina.select()
        
    def metadata(self, numPag=0):
        if self.formato is None:
            print("ERROR: No hay una tabla creada")
        else:
            pagina = self.get_page(numPag)
            return pagina.metadata()

    def commit(self):
        ruta = os.path.join(self.nombre_carpeta, "data")
        if self.formato is None:
            print("ERROR: No hay una tabla creada")
        else:
            with open(ruta, "ab+") as archivo:
                archivo.write(self.codificador.codificar_nodo(self.paginas.get(0)))