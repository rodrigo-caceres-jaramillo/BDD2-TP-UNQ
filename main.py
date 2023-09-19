from elementos import MaquinaVirtual
import sys
"""
if len(sys.argv) < 2:
   print("ERROR: Introducir un archivo valido")
   sys.exit()
   sys.argv[1]
"""
nombre_archivo = "ejemplo.db"

maquinaVirtual = MaquinaVirtual(nombre_archivo)
maquinaVirtual.iniciar()