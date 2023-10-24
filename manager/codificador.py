class Codificador:
    def codificar_registro(self, registro):
        id_codificado = int(registro.id).to_bytes(4, byteorder="big")
        nombre_bytes = bytes(registro.nombre, "ascii")
        nombre_codificado = nombre_bytes + b"\00"* (32 - len(nombre_bytes))
        email_bytes = bytes(registro.email, "ascii")
        email_codificado = email_bytes + b"\00"* (255 - len(email_bytes))
        
        return id_codificado + nombre_codificado + email_codificado
      
    def codificar_nodo(self, nodo):
        if nodo.tipo:
            return self.codificar_hoja(nodo)
        else:
            return self.codificar_nodo(nodo)
        
    
    def codificar_hoja(self, nodo):
        tipo_bytes = int(nodo.tipo).to_bytes(1, byteorder='big')
        root_bytes = int(nodo.root).to_bytes(1, byteorder='big')
        padre_bytes = int(nodo.padre).to_bytes(4, byteorder='big')
        cantidad_registros_bytes = int(nodo.cantidad_registros).to_bytes(4)
        registros_bytes = b''
        for clave, registro in nodo.registros.items():
            registro_bytes = int(clave).to_bytes(4) + registro.to_bytes()
            registros_bytes = registros_bytes + registro_bytes

        bytes = tipo_bytes + root_bytes + padre_bytes + cantidad_registros_bytes + registros_bytes
        return bytes + b"\00"* (4096 - len(bytes))