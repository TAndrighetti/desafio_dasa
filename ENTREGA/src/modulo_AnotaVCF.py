import pandas as pd
from modulo_AnotaVariante import AnotaVariante

########################################################################################################
############################ ANOTANDO VARIANTES A PARTIR DO VCF ########################################
########################################################################################################
########## Esse codigo realiza anotacoes a partir do bando de dados VEP (ENSEMBL).
##########
########## INPUT: dataframe criado a partir do VCF (modulo_importaVCF)
##########
########## OUTPUT: arquivo (input)_annotation_raw.csv contendo as seguintes informacoes:
##########  - ID: dbSNSP id (correspondente ao VCF)
##########  - REF e ALT: nucleotideos Referencia e Alterado (correspondente ao VCF)
##########  - GENE_SYMBOL: gene associado a variante
##########  - GENE_ID: gene id associado a variante no banco de dados ENSEMBL
##########  - FREQUENCIES: frequencias do gene de acordo com diferentes localizacoes e banco de dados
########################################################################################################


########################################################################################################
###### FUNCAO DE ANOTAÇÃO DOS VARIANTES PRESENTES NO VCF DE ENTRADA

def AnotaVCF(vcf_df, output_file_name):

    with open(output_file_name,'w') as output:
        output.write('ID;REF;ALT;GENE_SYMBOL;GENE_ID;DEPTH;FREQUENCIES\n')

        # Itera as linhas do vcf
        for index,row in vcf_df.iterrows():
            try:
                # Realiza a anotacao para aquele variante
                id, gene_symbol, gene_id, freq = AnotaVariante(row['ID'], row['ALT'])

                ## Organiza a string para que fique anotado apropriadamente no arquivo
                # 'gnomadg_amr:0.8811,gnomade:0.8865,gnomade_nfe:0.9059,gnomade_fin:0.9316...
                freq = ','.join([key+':'+str(value) for key, value in freq.items()])
                # ex.: nucleotideo:gene_symbol --> G:AGN
                gene_symbol = ','.join([key+':'+str(value) for key, value in gene_symbol.items()])
                gene_id = ','.join([key+':'+str(value) for key, value in gene_id.items()])

            # Se as anotacoes nao tiverem algum padrao identificado anteriormente, serao anotadas na tabela como ERRO 
            # e o erro sera printado na tela com o respectivo id para conferencia
            except Exception as e:
                print("Erro modulo AnotaVCF", id, row['ALT'], e)
                gene_symbol = gene_id = freq = "ERROR"

            # Escreve a linha de anotacao na tabela de saida
            new_row = [id,row['REF'],row['ALT'],gene_symbol,gene_id,row['DEPTH'],freq+'\n']
            output.write(';'.join(new_row))
            print(id, 'anotado com sucesso')

    print(output_file_name + " exportado com sucesso!")
        

## TESTE DA FUNCAO ANOTACAO
#Anotacao(VCF_to_DF(vcf_file))
##############################################################################################################
