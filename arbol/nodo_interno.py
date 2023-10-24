class NodoInterno():
    def __init__(self, tipo:bool, root:bool, padre:int, cantidad_claves:int, hijo_derecho: int, punteros={}):
        self.tipo = tipo
        self.root = root
        self.padre = padre
        self.cantidad_claves = cantidad_claves
        self.hijo_derecho = hijo_derecho
        self.punteros = punteros
        
    @classmethod  
    def from_bytes(cls, data:bytearray):    
        tipo = data[1]
        root = data[1]
        padre = int.from_bytes(data[2:6])
        cantidad_claves = int.from_bytes(data[6:10])
        hijo_derecho = int.from_bytes(data[10:14])
        data_punteros = data[14:]
        punteros = {}
        count = 0
        for i in range(cantidad_claves):
            clave = int.from_bytes(data_punteros[count:count+4])
            puntero = data_punteros[count+4:count+8]
            punteros[clave] = puntero
            count= count + 8
        return cls(tipo, root, padre, cantidad_claves, hijo_derecho, punteros)   
         
    def insert(self, registro):
        pass
                 
    def select(self):
        pass