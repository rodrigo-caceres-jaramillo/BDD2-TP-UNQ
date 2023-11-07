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
        ruta_meta = os.path.join(self.nombre_carpeta, "metadata.json")
        ruta_data = os.path.join(self.nombre_carpeta, "data.db")
        if not os.path.exists(self.nombre_carpeta):
            os.makedirs(self.nombre_carpeta)
        if not os.path.exists(ruta_meta) or os.path.getsize(ruta_meta) == 0:
            self.formato = None
        else:
            with open(ruta_meta, 'r') as metadata:
                contenido = json.loads(metadata.read())
                self.formato = contenido["table"]
                self.tamaño_pagina = contenido["meta"]["page_size"]
                self.tamaño_registro = contenido["meta"]["register_size"]
                self.codificador = Codificador(self.tamaño_pagina, self.formato)
                if(not os.path.exists(ruta_data) or os.path.getsize(ruta_data) == 0):
                    self.cantidad_paginas = 1
                else:  
                    self.cantidad_paginas = os.path.getsize(ruta_data) // self.tamaño_pagina
                self.paginas = {0: self.cargar_pagina(0)}
        
    def create(self, metadata):
        self.formato = metadata["table"]
        self.tamaño_pagina = metadata["meta"]["page_size"]
        self.tamaño_registro = sum(info['size'] for info in metadata["table"].values())
        metadata["meta"]["register_size"] = self.tamaño_registro
        ruta = os.path.join(self.nombre_carpeta, "metadata.json") 
        with open(ruta, 'w') as archivo_formato:
            archivo_formato.write(json.dumps(metadata))
        self.codificador = Codificador(self.tamaño_pagina, self.formato)
        self.cantidad_paginas = 1
        self.paginas = {0: self.cargar_pagina(0)}
        print("CREATE exitoso")
                   
    def cargar_pagina(self, numPag):
        ruta = os.path.join(self.nombre_carpeta, "data.db")
        if self.formato is None:
            return None
        else:
            if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
                nodo = NodoHoja(numPag, self, self.tamaño_pagina, self.tamaño_registro, True, 0, 0, {}, True)
                return nodo
            else:
                with open(ruta, 'rb') as archivo:
                    posicionInicial = self.tamaño_pagina * (numPag)
                    data = archivo.read()[posicionInicial: posicionInicial + self.tamaño_pagina]
                    if data[0] == 1:
                        nodo_h = NodoHoja.from_bytes(data, numPag, self, self.tamaño_pagina, self.tamaño_registro)
                        return nodo_h
                    else:
                        nodo_i = NodoInterno.from_bytes(data, numPag, self, self.tamaño_pagina, self.tamaño_registro)
                        return nodo_i
                
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
            
    def siguiente_numero(self):
        numero = self.cantidad_paginas
        self.cantidad_paginas += 1
        return numero
                
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