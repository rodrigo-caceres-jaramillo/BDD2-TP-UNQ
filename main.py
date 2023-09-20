from elementos import MaquinaVirtual
import sys

if len(sys.argv) < 2:
   print("ERROR: Introducir un archivo valido")
   sys.exit()
   
nombre_archivo = sys.argv[1]

maquinaVirtual = MaquinaVirtual(nombre_archivo)
maquinaVirtual.iniciar()