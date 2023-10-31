class Registro:
    def __init__(self, **atributos):
        self.id = atributos.get('id', None)
        self.atributos = atributos
    
    @classmethod  
    def from_bytes(cls, data, campos):
        atributos = {}
        for nombre, info in campos.items():
            tipo = info['type']
            tamaño = info['size']
            valor_data = data[:tamaño]
            if tipo == 'int':
                valor = int.from_bytes(valor_data, byteorder='big')
            elif tipo == 'str':
                valor = valor_data.decode('utf-8').rstrip('\x00')
            else:
                valor = None                
            data = data[tamaño:]
            atributos[nombre] = valor
        return cls(**atributos)
    
    def to_bytes(self, campos):
        atributos_codificados = b""
        for nombre, info in campos.items():
            valor = self.atributos[nombre]
            tipo = info['type']
            tamaño = info['size']
            if tipo == 'int':
                valor_codificado = int(valor).to_bytes(tamaño, byteorder='big')
            elif tipo == 'str':
                valor_codificado = valor.encode('utf-8') + b"\x00" * (tamaño - len(valor.encode('utf-8')))
            else:
                valor_codificado = b""
            atributos_codificados += valor_codificado
        print(len(atributos_codificados))
        return atributos_codificados
    
    def contenido(self):
        print(f"{self.id}{self.atributos}")