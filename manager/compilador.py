class Compilador:
    def __init__(self, maquinaVirtual):
        self.maquinaVirtual = maquinaVirtual
        
    def interpretar(self, entrada):
        comando = entrada[0]
        argumentos = entrada[1:]
        match comando:
            case "insert":
                if len(argumentos) == 3:
                    if(argumentos[0].isdigit()):
                        self.maquinaVirtual.insert(int(argumentos[0]), argumentos[1], argumentos[2])
                    else:
                        print("Operación inválida")
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