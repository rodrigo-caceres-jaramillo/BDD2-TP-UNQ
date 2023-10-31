import os
from arbol.nodo_hoja import NodoHoja
from arbol.nodo_interno import NodoInterno
from manager.codificador import Codificador
import json
from arbol.registro import Registro

class Paginador:
    def __init__(self, nombre_carpeta):
        self.nombre_carpeta = nombre_carpeta
        self.cargar_formato()
        
    def cargar_formato(self):
        ruta = os.path.join(self.nombre_carpeta, "metadata.json")
        if not os.path.exists(self.nombre_carpeta):
            os.makedirs(self.nombre_carpeta)
        if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
            self.formato = None
        else:
            with open(ruta, 'r') as archivo_formato:
                contenido = json.loads(archivo_formato.read())
                self.tamaño_pagina = contenido.pop("page_size", 0)
                self.formato = contenido
                self.tamaño_registro = sum(info['size'] for info in self.formato.values())
                self.codificador = Codificador(self.tamaño_pagina, self.formato)
                self.paginas = {0: self.cargar_pagina(0)}
        
    def create(self, meta, tamaño_pagina):
        self.formato = meta
        self.tamaño_pagina = tamaño_pagina
        self.formato["page_size"] = tamaño_pagina
        ruta = os.path.join(self.nombre_carpeta, "metadata.json")
        with open(ruta, 'w') as archivo_formato:
            archivo_formato.write(json.dumps(self.formato))
        self.formato.pop("page_size", 0)
        self.tamaño_registro = sum(info['size'] for info in self.formato.values())
        self.codificador = Codificador(self.tamaño_pagina, self.formato)
        self.paginas = {0: self.cargar_pagina(0)}
                   
    def cargar_pagina(self, numPag):
        ruta = os.path.join(self.nombre_carpeta, "data.db")
        if self.formato is None:
            return None
        else:
            if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
                return NodoHoja(0, self, self.tamaño_pagina, self.tamaño_registro, True, 0, 0, {}, True)
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
        ruta = os.path.join(self.nombre_carpeta, "data.db")
        if self.formato is None:
            print("ERROR: No hay una tabla creada")
        else:
            with open(ruta, "ab+") as archivo:
                for numPag, pagina in self.paginas.items():
                    if pagina.modificado:
                        nodo_bytes = self.codificador.codificar_nodo(pagina)
                        archivo.seek(numPag * self.tamaño_pagina)
                        archivo.write(nodo_bytes)