import argparse
import pandas as pd
from flask import Flask, request, render_template,json

app = Flask(__name__)

#python run.py --input_api NIST_annotation_complete.csv

# Obtem os argumentos da linha de comando
parser = argparse.ArgumentParser()
parser.add_argument('-ia','--input_api', help='Arquivo de anotacao a ser utilizado pelo API')
args = parser.parse_args()

dados_de_anotacao = args.input_api
dicionario_de_siglas = 'siglas_populacoes.json'

######### OBTENCAO DOS DADOS DAS ANOTACOES
dados = pd.read_csv(dados_de_anotacao, sep=';', index_col='ID')

# Informacoes sobre as siglas das anotacoes
with open(dicionario_de_siglas, 'r', encoding='utf-8') as json_file:
    siglas_populacoes = json.load(json_file)

######### RENDERIZACAO DO TEMPLATE INICIAL
@app.route("/")
def home():
    # Renderiza o template HTML
    return render_template("index.html")

######### OBTENDO ANOTAÇÃO DE VARIANTES ESPECÍFICAS
@app.route("/submit_variant", methods=["POST"])
def submit_variant():
     
    # Pegando o valor do campo "variant_id" do formulário HTML
    variant_id = request.form['variant_id']

    # Transformando os ids em uma lista
    if ',' in variant_id:
        variant_id = variant_id.split(',')
    else: 
        variant_id = [variant_id]

    # Pegando a informação de anotação nos dados
    anotacao = dados.loc[variant_id]
    # Renomeia os nomes das populações para que fique mais legivel
    anotacao = anotacao.rename(columns=siglas_populacoes)

    # Retornando a tabela com a anotação das variantes:
    return anotacao.to_html()

######### FILTRANDO VARIANTES POR FREQUÊNCIA E PROFUNDIDADE
@app.route("/filter_variants", methods=["POST"])
def filter_variants():
    
    #### ORGANIZANDO OS VALORES DE ENTRADA
    ## Coletando os valores enviados pelo formulário de filtro
    min_freq = request.form['min_freq']
    max_freq = request.form['max_freq']
    min_dp = request.form['min_dp']
    max_dp = request.form['max_dp']
    
    ## Determinando valores padrao em caso de campos serem deixados em branco
    min_freq = float(min_freq) if min_freq else 0.
    max_freq = float(max_freq) if max_freq else 1.
    min_dp = int(min_dp) if min_dp else 0.
    max_dp = int(max_dp) if max_dp else 100.


    ## INFORMAÇÕES SOBRE COLUNAS
    # Coletando as populações selecionadas
    populations = request.form.getlist('populations')
    populations = [population.lower() for population in populations]
    
    # Determinando lista padrão de colunas:
    colunas_padrao = ['REF','ALT','GENE_SYMBOL','GENE_ID','DEPTH']

    ## ARRUMANDO FORMATO DA TABELA
    for col in populations:
        dados[col] = dados[col].astype(str).str.replace(',', '.').astype(float)

    #### FILTRANDO OS VARIANTES
    ## Filtrando por profundidade
    filtro1 = dados[(dados['DEPTH'] >= min_dp) & (dados['DEPTH'] <= max_dp)]
    
    ## Filtrando por frequencia
    filtro2 = filtro1[colunas_padrao + populations]

    
    # So filtra se os campos de filtragem por frequencia nao estiverem vazios
    if min_freq != 0 and max_freq != 1:
        filtro2['MEDIA DE FREQUENCIA'] = filtro2[populations].mean(axis=1)
        filtro2 = filtro2[(filtro2['MEDIA DE FREQUENCIA'] >= min_freq) & (filtro2['MEDIA DE FREQUENCIA'] <= max_freq)]
  

    # Renomeia os nomes das populações para que fique mais legivel
    filtro2 = filtro2.rename(columns=siglas_populacoes)

    return filtro2.to_html()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)