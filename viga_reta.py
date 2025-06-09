import matplotlib.pyplot as plt

def calcular_esforcos(viga):
    #calcula os esforços reativos
    viga['reação_esquerda'] = viga['carga_total'] * (viga['distância_carga'] - viga['distância_apoio_direito']) / viga['comprimento']
    viga['reação_direita'] = viga['carga_total'] - viga['reação_esquerda']
    
    #calcula os esforços solicitantes
    viga['cortante'] = [viga['reação_esquerda']]
    viga['momento'] = [0]
    
    for carga in viga['cargas']:
        distância_carga = carga['distância']
        intensidade_carga = carga['intensidade']
        
        #cortante
        viga['cortante'].append(viga['cortante'][-1] - intensidade_carga)
        
        #momento
        momento_anterior = viga['momento'][-1]
        momento = momento_anterior - viga['cortante'][-2] * (distância_carga - viga['cargas'][0]['distância'])
        viga['momento'].append(momento)
    
    return viga

def gerar_diagrama_esforcos(viga):
    #plot do diagrama de esforços solicitantes
    distancia = [0]
    cortante = viga['cortante']
    momento = viga['momento']
    
    for carga in viga['cargas']:
        distancia.append(carga['distância'])
    
    plt.subplot(2, 1, 1)
    plt.plot(distancia, cortante)
    plt.xlabel('Distância (m)')
    plt.ylabel('Cortante (kN)')
    plt.title('Diagrama de Esforços Solicitantes - Cortante')
    
    plt.subplot(2, 1, 2)
    plt.plot(distancia, momento)
    plt.xlabel('Distância (m)')
    plt.ylabel('Momento (kNm)')
    plt.title('Diagrama de Esforços Solicitantes - Momento')
    
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":

    #exemplo de utilização
    viga = {
        'comprimento': 6,  #comprimento total da viga em metros
        'carga_total': 20,  #carga total aplicada na viga em kN
        'distância_apoio_direito': 2,  # distância do apoio direito em metros
        'distância_carga': 4,  #distância da carga do apoio direito em metros
        'cargas': [
            {'distância': 1, 'intensidade': 5},  # exemplo de carga adicional
            {'distância': 3, 'intensidade': 10}  # oitro exemplo de carga adicional
        ]
    }

    viga_calculada = calcular_esforcos(viga)
    gerar_diagrama_esforcos(viga_calculada)
