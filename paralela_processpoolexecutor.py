# SE IMPORTAN LAS LIBRERÍAS NECESARIAS:
import random
import time
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count

# SE FIJA UNA SEMILLA PARA LA GENERACIÓN DE VALORES ALEATORIOS:
random.seed(42) 

# SE CREA UNA FUNCIÓN PARA GENERAR LA MATRIZ INICIAL:
def generar_matriz(filas, columnas):
    return [[random.randint(0, 1) for _ in range(columnas)] for _ in range(filas)]

# SE CREA UNA FUNCIÓN PARA CONTAR VECINOS VIVOS DE UNA CÉLULA SEGÚN SU ENTORNO:
def contar_entorno(fila, columna, matriz):
    vivas = 0
    for i in range(fila - 1, fila + 2):
        for j in range(columna - 1, columna + 2):
            if i == fila and j == columna:
                continue
            if 0 <= i < len(matriz) and 0 <= j < len(matriz[0]):
                if matriz[i][j] == 1:
                    vivas += 1
    return vivas

# SE CREA UNA FUNCIÓN PARA ACTUALIZAR UNA CÉLULA VIVA O MUERTA SEGÚN SU ENTORNO:
def actualizar_celula(celula, vivas):
    if celula == 0:
        return 1 if vivas == 3 else 0
    else:
        if vivas < 2:
            return 0
        elif vivas in (2, 3):
            return 1
        else:
            return 0

# SE CREA UNA FUNCIÓN PARA IMPRIMIR LA MATRIZ ACTUALIZADA:
def imprimir_matriz(matriz):
    for fila in matriz:
        print(" ".join("1" if cel == 1 else "0" for cel in fila))
    print()

# SE CREA UNA FUNCIÓN PARA ACTUALIZAR LOS BLOQUES DE FILAS:
def actualizar_bloque(matriz, nueva_matriz, fila_inicio, fila_fin):
    #filas = len(matriz)
    columnas = len(matriz[0])
    for i in range(fila_inicio, fila_fin):
        for j in range(columnas):
            vivas = contar_entorno(i, j, matriz)
            nueva_matriz[i][j] = actualizar_celula(matriz[i][j], vivas)

# FUNCION PRINCIPAL PARA EJECUTAR EL CÓDIGO:
def main():
    filas, columnas = 1500, 1500   # Tamaño del tablero.
    generaciones = 50          # Número fijo de generaciones.
    num_procesos = cpu_count()  # Con este parámetro se cambia el número de procesos.

    matriz = generar_matriz(filas, columnas)

    start = time.time() # Inicio de ejecución.

    # Crea el pool una sola vez (más eficiente que crear procesos en cada ciclo)
    with ProcessPoolExecutor(max_workers=num_procesos) as executor:
        for gen in range(generaciones):
            os.system("cls" if os.name == "nt" else "clear")
            print(f"Generación {gen + 1}/{generaciones}")

            nueva_matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

            bloque = filas // num_procesos
            tareas = []

            # Enviar bloques a los procesos
            for p in range(num_procesos):
                inicio = p * bloque
                fin = (p + 1) * bloque if p != num_procesos - 1 else filas
                tareas.append(
                    executor.submit(actualizar_bloque, matriz, nueva_matriz, inicio, fin)
                )

            # Esperar resultados (as_completed para mayor eficiencia)
            for tarea in as_completed(tareas):
                tarea.result()

            matriz = nueva_matriz  # Actualizar la matriz para la siguiente generación

    end = time.time()
    print(f"Tiempo total de ejecución: {end - start:.2f} segundos")

if __name__ == "__main__":
    main()