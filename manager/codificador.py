class Codificador:
    def __init__(self, tamaño_pagina, formato):
        self.tamaño_pagina = tamaño_pagina
        self.formato = formato
      
    def codificar_nodo(self, nodo):
        if (type(nodo).__name__ == "NodoHoja"):
            return self.codificar_hoja(nodo)
        else:
            return self.codificar_interno(nodo)
    
    def codificar_hoja(self, nodo):
        tipo_bytes = int(1).to_bytes(1, byteorder='big')
        root_bytes = int(nodo.root).to_bytes(1, byteorder='big')
        padre_bytes = int(nodo.padre).to_bytes(4, byteorder='big')
        cantidad_registros_bytes = int(nodo.cantidad_registros).to_bytes(4)
        registros_bytes = b''
        for clave, registro in nodo.registros.items():
            registro_bytes = int(clave).to_bytes(4) + registro.to_bytes(self.formato)
            registros_bytes = registros_bytes + registro_bytes

        bytes = tipo_bytes + root_bytes + padre_bytes + cantidad_registros_bytes + registros_bytes
        return bytes + b"\00"* (self.tamaño_pagina - len(bytes))
    
    def codificar_interno(self, nodo):
        tipo_bytes = int(1).to_bytes(1, byteorder='big')
        root_bytes = int(nodo.root).to_bytes(1, byteorder='big')
        padre_bytes = int(nodo.padre).to_bytes(4, byteorder='big')
        cantidad_claves_bytes = int(nodo.cantidad_claves).to_bytes(4, byteorder='big')
        hijo_derecho_bytes = int(nodo.hijo_derecho).to_bytes(4, byteorder='big')
        punteros_bytes = b''
        for clave, puntero in nodo.punteros.items():
            puntero_bytes = int(clave).to_bytes(4, byteorder='big') + int(puntero).to_bytes(4, byteorder='big')
            punteros_bytes = punteros_bytes + puntero_bytes

        bytes = tipo_bytes + root_bytes + padre_bytes + cantidad_claves_bytes + hijo_derecho_bytes + punteros_bytes
        return bytes + b"\00"* (self.tamaño_pagina - len(bytes))