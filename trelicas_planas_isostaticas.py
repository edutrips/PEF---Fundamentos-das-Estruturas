import numpy as np

def calcular_forcas_apoio(reacoes, matriz_rigidez):
    forcas_apoio = np.linalg.solve(matriz_rigidez, reacoes)
    return forcas_apoio

def calcular_deslocamentos(forcas_apoio, matriz_rigidez, deslocamentos_conhecidos):
    deslocamentos = np.linalg.solve(matriz_rigidez, forcas_apoio - deslocamentos_conhecidos)
    return deslocamentos

def calcular_reacoes(matriz_rigidez, deslocamentos, deslocamentos_conhecidos):
    reacoes = np.dot(matriz_rigidez, deslocamentos) + deslocamentos_conhecidos
    return reacoes

#exemplo de treliça com 3 nós e 3 barras
#definição das barras: (nó inicial, nó final, comprimento)
if __name__ == "__main__":
    barras = [(0, 1, 5), (0, 2, 4), (1, 2, 3)]
    #número de nós
    num_nos = 3
    #número de barras
    num_barras = 3
    #número de graus de liberdade por nó
    num_graus_liberdade = 2

    #matriz de rigidez global
    matriz_rigidez = np.zeros((num_nos * num_graus_liberdade, num_nos * num_graus_liberdade))

    for barra in barras:
        no_inicial, no_final, comprimento = barra
        dx = (no_final - no_inicial) * comprimento / np.sqrt((no_final - no_inicial) ** 2 + comprimento ** 2)
        dy = comprimento / np.sqrt((no_final - no_inicial) ** 2 + comprimento ** 2)
        matriz_local = np.array([[dx, dy, 0, 0], [0, 0, dx, dy]])
        matriz_rigidez_local = np.dot(matriz_local.T, matriz_local)
        matriz_rigidez[2 * no_inicial:2 * no_inicial + 2, 2 * no_inicial:2 * no_inicial + 2] += matriz_rigidez_local[:2, :2]
        matriz_rigidez[2 * no_inicial:2 * no_inicial + 2, 2 * no_final:2 * no_final + 2] += matriz_rigidez_local[:2, 2:]
        matriz_rigidez[2 * no_final:2 * no_final + 2, 2 * no_inicial:2 * no_inicial + 2] += matriz_rigidez_local[2:, :2]
        matriz_rigidez[2 * no_final:2 * no_final + 2, 2 * no_final:2 * no_final + 2] += matriz_rigidez_local[2:, 2:]

    #definição das forças de apoio conhecidas (condições de contorno)
    #formato: [Fx_nó_1, Fy_nó_1, Fx_nó_2, Fy_nó_2, ..., Fx_nó_n, Fy_nó_n]
    forcas_apoio_conhecidas = np.array([0, 0, 0, -10, 0, 0])

    #definição dos deslocamentos conhecidos (condições de contorno)
    #formato: [dx_nó_1, dy_nó_1, dx_nó_2, dy_nó_2, ..., dx_nó_n, dy_nó_n]
    deslocamentos_conhecidos = np.array([0, 0, 0, 0, 0, 0])

    #cálculo das forças de apoio
    forcas_apoio = calcular_forcas_apoio(forcas_apoio_conhecidas, matriz_rigidez)

    #cálculo dos deslocamentos desconhecidos
    deslocamentos = calcular_deslocamentos(forcas_apoio, matriz_rigidez, deslocamentos_conhecidos)

    #cálculo das reações de apoio
    reacoes = calcular_reacoes(matriz_rigidez, deslocamentos, deslocamentos_conhecidos)

    #saída dos resultados
    print("Forças de apoio:")
    print(forcas_apoio)
    print("Deslocamentos:")
    print(deslocamentos)
    print("Reações de apoio:")
    print(reacoes)
