# SE IMPORTAN LAS LIBRERÍAS NECESARIAS:
import time
import os
import numpy as np
import multiprocessing as mp

# SE FIJA UNA SEMILLA PARA LA GENERACIÓN DE VALORES ALEATORIOS:
np.random.seed(42)

# SE CREA UNA FUNCIÓN PARA GENERAR LA MATRIZ INICIAL:
def generar_matriz(filas, columnas):
    return np.random.randint(0, 2, size=(filas, columnas)).tolist()

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
def actualizar_bloque(args):
    matriz, fila_inicio, fila_fin = args
    columnas = len(matriz[0])
    bloque_nuevo = [[0 for _ in range(columnas)] for _ in range(fila_fin - fila_inicio)]

    for i in range(fila_inicio, fila_fin):
        for j in range(columnas):
            vivas = contar_entorno(i, j, matriz)
            bloque_nuevo[i - fila_inicio][j] = actualizar_celula(matriz[i][j], vivas)
    return fila_inicio, bloque_nuevo

# FUNCIÓN PRINCIPAL PARA EJECUTAR EL CÓDIGO:
def main():
    filas, columnas = 1500, 1500   # Tamaño del tablero.
    generaciones = 50              # Número fijo de generaciones.
    num_procesos = 8               # Con este parámetro se cambia el número de procesos.

    matriz = generar_matriz(filas, columnas)


    start = time.time()  # Inicio de ejecución.

    for gen in range(generaciones):
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Generación {gen + 1}/{generaciones}")
        #imprimir_matriz(matriz)

        nueva_matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

        # Dividir la matriz por bloques (una parte para cada proceso)
        bloque = filas // num_procesos
        tareas = []

        for p in range(num_procesos):
            inicio = p * bloque
            fin = (p + 1) * bloque if p != num_procesos - 1 else filas
            tareas.append((matriz, inicio, fin))

        # Crear un Pool de procesos y ejecutar los bloques en paralelo
        with mp.Pool(processes=num_procesos) as pool:
            resultados = pool.map(actualizar_bloque, tareas)

        # Combinar los resultados en la nueva matriz
        for inicio, bloque_nuevo in resultados:
            for idx, fila in enumerate(bloque_nuevo):
                nueva_matriz[inicio + idx] = fila

        matriz = nueva_matriz
        # time.sleep(0.1)  # Pausa opcional para ver el avance

    end = time.time()
    print(f"Tiempo total de ejecución paralela1: {end - start:.2f} segundos")


if __name__ == "__main__":
    main()
