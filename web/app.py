import os
import sys
import io
import base64
import numpy as np

from flask import Flask, render_template, request
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from viga_reta import calcular_esforcos as calc_viga_reta
from vigas_poligonais_espaciais import calcular_esforcos_vigas_poligonais as calc_viga_poligonal
from trelicas_planas_isostaticas import calcular_forcas_apoio as calc_trelica_reacoes

app = Flask(__name__)

# ----------------------------------------------------------
# Rota única para exibir o formulário dinâmico
# ----------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# ----------------------------------------------------------
# Rota que recebe o POST do formulário e processa os cálculos
# ----------------------------------------------------------
@app.route('/calcular', methods=['POST'])
def calcular():
    tipo = request.form.get('tipo_estrutura')

    # 1) Se for Viga Reta:
    if tipo == 'viga_reta':
        # Lê os campos específicos
        try:
            comprimento = float(request.form.get('comprimento', ''))
            carga_total = float(request.form.get('carga_total', ''))
            dist_apoio_dir = float(request.form.get('dist_apoio_dir', ''))
            dist_carga = float(request.form.get('dist_carga', ''))
        except ValueError:
            return render_template('resultado.html', error="Valores inválidos em Viga Reta.")

        cargas = []
        for i in (1, 2):
            d = request.form.get(f'carga{i}_dist', '').strip()
            inten = request.form.get(f'carga{i}_inten', '').strip()
            if d and inten:
                try:
                    cargas.append({'distância': float(d), 'intensidade': float(inten)})
                except ValueError:
                    return render_template('resultado.html', error="Formato inválido em cargas pontuais.")

        viga_dict = {
            'comprimento': comprimento,
            'carga_total': carga_total,
            'distância_apoio_direito': dist_apoio_dir,
            'distância_carga': dist_carga,
            'cargas': cargas
        }
        viga_calc = calc_viga_reta(viga_dict)
        dist_vals = [0] + [c['distância'] for c in viga_calc['cargas']]
        cortante = viga_calc['cortante']
        momento = viga_calc['momento']

        # Monta  o gráfico Matplotlib
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5), tight_layout=True)
        ax1.plot(dist_vals, cortante, '-o')
        ax1.set_xlabel('Distância (m)')
        ax1.set_ylabel('Cortante (kN)')
        ax1.set_title('Diagrama Cortante (Viga Reta)')
        ax1.grid(True)

        ax2.plot(dist_vals, momento, '-o', color='orange')
        ax2.set_xlabel('Distância (m)')
        ax2.set_ylabel('Momento (kNm)')
        ax2.set_title('Diagrama Momento (Viga Reta)')
        ax2.grid(True)

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode('ascii')
        plt.close(fig)

        return render_template('resultado.html', img_data=img_data,
                               titulo="Viga Reta: Cortante e Momento")


    # 2) Se for Viga Poligonal:
    elif tipo == 'viga_poligonal':
        # --- 1) Ler a Matriz de Rigidez 4×4 ---
        K = np.zeros((4, 4))
        try:
            for i in range(4):
                for j in range(4):
                    campo = request.form.get(f'rigidez_{i}_{j}', '').strip()
                    K[i, j] = float(campo)
        except ValueError:
            return render_template('resultado.html',
                                error="Valores inválidos na Matriz de Rigidez 4×4.")

        # --- 2) Ler o Vetor de Forças (4×1)
        F = np.zeros(4)
        try:
            for i in range(4):
                campo = request.form.get(f'forcas_{i}', '').strip()
                F[i] = float(campo)
        except ValueError:
            return render_template('resultado.html',
                                error="Valores inválidos no Vetor de Forças (4×1).")

        # --- 3) Ler a Matriz de Cortantes 4×4
        C = np.zeros((4, 4))
        try:
            for i in range(4):
                for j in range(4):
                    campo = request.form.get(f'cortantes_{i}_{j}', '').strip()
                    C[i, j] = float(campo)
        except ValueError:
            return render_template('resultado.html',
                                error="Valores inválidos na Matriz de Cortantes 4×4.")

        # --- 4) Ler a Matriz de Momentos 4×4
        M = np.zeros((4, 4))
        try:
            for i in range(4):
                for j in range(4):
                    campo = request.form.get(f'momentos_{i}_{j}', '').strip()
                    M[i, j] = float(campo)
        except ValueError:
            return render_template('resultado.html',
                                error="Valores inválidos na Matriz de Momentos 4×4.")

        # --- 5) Ler Distâncias
        try:
            distancias = list(map(float, request.form.get('distancias', '').split(',')))
        except:
            return render_template('resultado.html',
                                error="Formato de distâncias inválido.")

        # --- 6) Monta o dicionário e chama a função de cálculo
        viga_dict = {
            'matriz_rigidez': K,
            'vetor_forças': F,
            'matriz_cortantes': C,
            'matriz_momentos': M,
            'distancias': distancias
        }
        viga_calc = calc_viga_poligonal(viga_dict)

        # --- 7) Extrai resultados e plota
        V = viga_calc['cortantes']
        M_ = viga_calc['momentos']

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5), tight_layout=True)
        ax1.plot(distancias, V, '-o')
        ax1.set_xlabel('Distância (m)')
        ax1.set_ylabel('Cortante (kN)')
        ax1.set_title('Diagrama Cortante (Viga Poligonal)')
        ax1.grid(True)

        ax2.plot(distancias, M_, '-o', color='green')
        ax2.set_xlabel('Distância (m)')
        ax2.set_ylabel('Momento (kNm)')
        ax2.set_title('Diagrama Momento (Viga Poligonal)')
        ax2.grid(True)

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode('ascii')
        plt.close(fig)

        return render_template('resultado.html',
                            img_data=img_data,
                            titulo="Viga Poligonal: Cortante e Momento")



    # 3) Se for Treliça:
    elif tipo == 'trelica':
        # --- 1) Ler Matriz de Rigidez 6×6
        Kt = np.zeros((6, 6))
        try:
            for i in range(6):
                for j in range(6):
                    campo = request.form.get(f'rigidez_t_{i}_{j}', '').strip()
                    Kt[i, j] = float(campo)
        except ValueError:
            return render_template('resultado.html', error="Valores inválidos na Matriz de Rigidez da Treliça.")

        # --- 2) Ler Vetor de Forças 6×1 
        Ft = np.zeros(6)
        try:
            for i in range(6):
                campo = request.form.get(f'forcas_t_{i}', '').strip()
                Ft[i] = float(campo)
        except ValueError:
            return render_template('resultado.html', error="Valores inválidos no Vetor de Forças da Treliça.")

        # --- 3) Ler Vetor de Deslocamento
        Dt = np.zeros(6)
        try:
            for i in range(6):
                campo = request.form.get(f'deslocamentos_conhecidos_t_{i}', '').strip()
                Dt[i] = float(campo)
        except ValueError:
            return render_template('resultado.html', error="Valores inválidos nos Deslocamentos Conhecidos da Treliça.")

        # --- 4) Chama as funções de treliça 
        reacoes = calc_trelica_reacoes(Ft, Kt)

        return render_template('resultado.html',
                            tabela_reacoes=reacoes.tolist(),
                            titulo="Treliça: Reações de Apoio")

# Rodar o app
if __name__ == '__main__':
    app.run(debug=True)
