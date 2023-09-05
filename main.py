from elementos import Tabla

def main():
    tabla = Tabla()
    
    while True:
        comando = input("sql>").split()
        operacion = comando[0]
        argumentos = comando[1:]
        match operacion:
            case "insert": 
                if len(argumentos) == 3:
                    tabla.agregar_registro(argumentos[0], argumentos[1], argumentos[2])
                else:
                    print("Operación inválida")
            case "select":
                if len(argumentos) == 0:
                    tabla.seleccionar_registros()
                else:
                    print("Operación inválida")
            case ".table-metada":
                if len(argumentos) == 0:
                    tabla.metadata()
                else:
                    print("Operación inválida")
            case ".exit":
                if len(argumentos) == 0:
                    print("Terminado")
                    exit()
                else:
                    print("Operación inválida")
                
                   
if __name__ == "__main__":
    main()
 