import matplotlib.pyplot as plt
import numpy as np

def calcular_esforcos_vigas_poligonais(viga):
    #calcula os esforços reativos
    viga['reações'] = np.linalg.solve(viga['matriz_rigidez'], viga['vetor_forças'])
    
    #calcula os esforços solicitantes
    viga['cortantes'] = np.dot(viga['matriz_cortantes'], viga['reações'])
    viga['momentos'] = np.dot(viga['matriz_momentos'], viga['reações'])
    
    return viga

def gerar_diagrama_esforcos_vigas_poligonais(viga):
    #plot do diagrama de esforços solicitantes
    distancia = viga['distancias']
    cortantes = viga['cortantes']
    momentos = viga['momentos']
    
    plt.subplot(2, 1, 1)
    plt.plot(distancia, cortantes)
    plt.xlabel('Distância (m)')
    plt.ylabel('Cortante (kN)')
    plt.title('Diagrama de Esforços Solicitantes - Cortante')
    
    plt.subplot(2, 1, 2)
    plt.plot(distancia, momentos)
    plt.xlabel('Distância (m)')
    plt.ylabel('Momento (kNm)')
    plt.title('Diagrama de Esforços Solicitantes - Momento')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Exemplo de utilização
    viga = {
        'matriz_rigidez': np.array([[6, -2, 0, 0],
                                    [-2, 8, -3, 0],
                                    [0, -3, 10, -4],
                                    [0, 0, -4, 5]]),
        'vetor_forças': np.array([0, 0, 20, 0]),
        'matriz_cortantes': np.array([[0, 0, 0, 1],
                                    [0, 0, 1, 0],
                                    [0, 1, 0, 0],
                                    [1, 0, 0, 0]]),
        'matriz_momentos': np.array([[0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [1, 0, 0, 0]]),  #exemplo de matriz de momentos diferente de zero
        'distancias': [0, 2, 4, 6]
    }

    viga_calculada = calcular_esforcos_vigas_poligonais(viga)
    gerar_diagrama_esforcos_vigas_poligonais(viga_calculada)
