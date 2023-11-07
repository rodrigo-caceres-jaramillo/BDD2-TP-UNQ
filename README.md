# BDD2-TP-UNQ
Trabajo Practico de Base de Datos 2 UNQ

## Guia de Uso
1. Ejecutar el programa con: 

    `./run.sh <nombre_de_carpeta>`

2. Si ya existe un archivo metadata.json correcto proseguir al paso 4.
3. Crear el formato de la tabla con el siguiente comando: 

    `create <tamaño_de_pagina> (id int(<tamaño_de_id>), <nombre_del_campo> <int/string>(<tamaño_del_campo>))`

    Ejemplo:

    `create 200 (id int(4), nombre string(32))`

4. Utilizar los comandos:
  
      Para insertar nuevos registros:
      `insert <id> <primer_campo>`
   
      Para ver todos los registros:
      `select`

   Para ver la cantidad de registros y paginas:
   `.table-metadata`

   Para salir y guardar los cambios en un archivo:
   `.exit`

