import re

class Compilador:
    def __init__(self, maquinaVirtual):
        self.maquinaVirtual = maquinaVirtual
        
    def interpretar(self, entrada):
        entrada_lista = entrada.split()
        comando = entrada_lista[0]
        argumentos = entrada_lista[1:]
        match comando:
            case "create":
                if len(argumentos) >= 1:
                    pattern = r"(\w+)\s+(\w+)\((\w+)\)"
                    matches = re.findall(pattern, entrada)
                    result_dict = {}
                    for match in matches:
                        campo = match[0]
                        tipo = match[1]
                        tamaño = match[2]
                        result_dict[campo] = {"type": tipo, "size": int(tamaño)}
                    formato = {"meta": {"page_size": int(argumentos[0].rstrip('('))}, "table": result_dict}
                    self.maquinaVirtual.create(formato)
                else:
                    print("Operación inválida")
            case "insert":
                if len(argumentos) > 0:
                    campos = argumentos[0:]
                    self.maquinaVirtual.insert(campos)
                else:
                    print("Operación inválida")
            case "select":
                if len(argumentos) == 0:
                    self.maquinaVirtual.select()
                elif len(argumentos) == 1 and argumentos[0].isdigit():
                    self.maquinaVirtual.select_id(argumentos[0])
                else: 
                    print("Operación inválida")
            case ".table-metadata":
                if len(argumentos) == 0:
                    self.maquinaVirtual.metadata()
                else:
                    print("Operación inválida")
            case ".exit":
                if len(argumentos) == 0:
                    self.maquinaVirtual.exit()
                else:
                    print("Operación inválida")
            case default:
                print("Operación inválida")