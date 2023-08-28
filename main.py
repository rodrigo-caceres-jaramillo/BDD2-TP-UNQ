while True:
    command = input("sql>")
    match command:
        case "exit":
            print("Terminado")
            exit()
        case "insert":
            print("INSERT no implementado")
        case "select":
            print("SELECT no implementado")
        case other:
            print("No se reconoce el comando")