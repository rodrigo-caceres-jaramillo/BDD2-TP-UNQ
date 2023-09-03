def main():
    paginas= []
    pagina_actual = None
    
    while True:
        comando = input("sql>").split()
        operacion = comando[0]
        argumentos = comando[1:]
        match operacion:
            case "insert": 
                if len(argumentos) == 3:
                    registro = Registro(argumentos[0], argumentos[1], argumentos[2])
                    
                    print("INSERT exitoso")
                else:
                    print("Operación inválida")
            case "select":
                if len(argumentos) == 0:
                    print("SELECT exitoso")
                else:
                    print("Operación inválida")
            case ".table-metada":
                print("Paginas:\nRegistros:")
            case ".exit":
                print("Terminado")
                exit()
                   
if __name__ == "__main__":
    main()
    
    