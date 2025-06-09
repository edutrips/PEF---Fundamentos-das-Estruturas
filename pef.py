from viga_reta import calcular_esforcos, gerar_diagrama_esforcos, viga
from vigas_poligonais_espaciais import calcular_esforcos_vigas_poligonais, gerar_diagrama_esforcos_vigas_poligonais, viga
def main():
    #vigas retas
    viga_reta = calcular_esforcos(viga)
    gerar_diagrama_esforcos(viga_reta)

    #vigas poligonais
    viga_poligonal = calcular_esforcos_vigas_poligonais(viga)
    gerar_diagrama_esforcos_vigas_poligonais(viga_poligonal)
