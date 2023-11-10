from manager.maquina_virtual import MaquinaVirtual
import sys

carpeta = sys.argv[1]

maquinaVirtual = MaquinaVirtual(carpeta)
maquinaVirtual.iniciar()