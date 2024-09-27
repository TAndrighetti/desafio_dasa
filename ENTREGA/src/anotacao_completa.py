import argparse
from modulo_ImportaVCF import ImportaVCF
from modulo_AnotaVCF import AnotaVCF 
from modulo_ProcessaAnotacao import ProcessaAnotacao

#python anotacao_completa.py --vcf_file "./dados/NIST_teste.vcf" --output "./dados/NIST_teste_annotation_complete.csv"

#vcf_file = "./dados/NIST_teste.vcf"
#output = "./dados/NIST_teste_annotation_complete.csv"

# Obtem os argumentos da linha de comando
parser = argparse.ArgumentParser()
parser.add_argument('-vf','--vcf_file', help='Caminho e nome do arquivo VCF para anotar')
parser.add_argument('-o','--output', help='Caminho e nome do arquivo de saida; .csv de anotacao')
args = parser.parse_args()

vcf_file = args.vcf_file
output = args.output

########## 01. Importa o VCF
## Output: DataFrame com as colunas 'ID','REF','ALT' e 'DEPTH'do VCF
vcf_df = ImportaVCF(vcf_file)

######### Determinando o nome do arquivo cru de anotacao
#raw_annotation_name = vcf_file.rsplit('.',1)[0]+"_raw.csv"

########### 02. Anota o arquivo vcf inteiro
## Input: DataFrame do VCF (output do ImportaVCF)
## Output: Arquivo com o nome raw_annotation_name
output = output.replace('_complete','') # modifica o nome de saida para este porque ainda nao esta completo
AnotaVCF(vcf_df, output)

########### 03. Processamento do arquivo de anotacao
## Input: Arquivo de anotacao "cru" (output do AnotaVCF)
## Output: Arquivo de anotacao processado raw_annotation_name + '_complete.csv'
ProcessaAnotacao(output)
