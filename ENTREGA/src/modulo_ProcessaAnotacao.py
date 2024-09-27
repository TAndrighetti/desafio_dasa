import pandas as pd

########################################################################################################
############################ PROCESSANDO O ARQUIVO DE ANOTACAO #########################################
########################################################################################################
##########  Os arquivos de anotacao gerados pelo AnotaVCF possuem uma coluna de frequencias com as
########## frequencias de todas as populacoes e bancos de dados concatenadas.
##########  A funcao ProcessaAnotacao faz o processamento dessa coluna, retornando um arquivo onde estas
########## frequencias estao separadas por colunas de acordo com a populacao de origem.
##########
########## INPUT: arquivo de anotacao crua originado do AnotaVCF
##########
########## OUTPUT: arquivo (input)_annotation.csv contendo as seguintes informacoes:
##########  - ID: dbSNSP id (correspondente ao VCF)
##########  - REF e ALT: nucleotideos Referencia e Alterado (correspondente ao VCF)
##########  - GENE_SYMBOL: gene associado a variante
##########  - GENE_ID: gene id associado a variante no banco de dados ENSEMBL
##########  - COLUNAS DE FREQUENCIAS inviduais de acordo com diferentes populacoes e banco de dados
########################################################################################################


##############################################################################################################
###### 3 - FUNCAO DE PROCESSAMENTO DA ANOTACAO - SEPARA OS VARIANTES ANOTADOS EM COLUNAS POR POPULACAO

def ProcessaAnotacao(path_to_annotation_file):

    annotation_file = pd.read_csv(path_to_annotation_file, sep=';')

    ### Monta o novo dataframe - separando as colunas de frequencia por populacao

    # annotation_file['FREQUENCIES'] = gnomadg:0.1077,gnomadg_sas:0.1934,gnomadg_eas:0.305,gnomadg_mid:0.1458,gnomade:0.01338,...
    # transforma em dicionarios {populacao: frequencia}
    annotation_file['FREQUENCIES'] = annotation_file['FREQUENCIES'].apply(
                                        lambda x: dict(item.split(':') 
                                                            for item in x.split(',') 
                                                            if ':' in item))


    ### Cria nova DF com as frequencias em colunas separadas

    # Faz o dicionario {0: {id: rs..., local1: freq1, local2,freq2...}, 1:...}
    new_frequencies= {index: {'ID':row['ID']} | row['FREQUENCIES'] 
                                for index, row in annotation_file.iterrows()}

    # Converte o dicionario gerado em dataframe
    new_frequencies = pd.DataFrame.from_dict(new_frequencies, orient='index')

    # Deleta as colunas extras
    new_frequencies.drop(['Missing information', 'var_id'], inplace=True, axis='columns', errors='ignore')

    ##### Merge com a tabela original

    # Coloca as informações organizadas no annotation_file
    annotation_file = pd.merge(annotation_file, new_frequencies, on='ID', how='outer')

    # Deleta a coluna FREQUENCIES, que tem a informação desorganizada
    annotation_file.drop(['FREQUENCIES'], inplace=True, axis='columns')

    output_name = path_to_annotation_file.replace('.csv','') + '_complete.csv'
    annotation_file.to_csv(output_name, index=False, sep=';', na_rep='NaN')

    print(output_name, "exportado com sucesso!")

    
# TESTE ProcessaAnotacao
#ProcessaAnotacao('NIST_annotation_raw_teste.csv')
##############################################################################################################
