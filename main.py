from elementos import MaquinaVirtual
import sys

if len(sys.argv) < 2:
   print("ERROR: Introducir un archivo valido")
   sys.exit()

archivo = sys.argv[1]

maquinaVirtual = MaquinaVirtual(archivo)
maquinaVirtual.iniciar()