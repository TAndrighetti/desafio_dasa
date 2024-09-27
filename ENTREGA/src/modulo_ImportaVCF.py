import pandas as pd

########################################################################################################
##################################### IMPORTANDO O ARQUIVO VCF #########################################
########################################################################################################
########## Esse codigo importa o arquivo VCF e processa ele para que seja submetido a anotacao.
##########
########## INPUT: arquivo VCF com as seguintes colunas obrigatorias: 'ID','REF','ALT' E'INFO'
##########
########## OUTPUT: dataframe contendo as seguintes informacoes:
##########  - ID: dbSNSP id (correspondente ao VCF)
##########  - REF e ALT: nucleotideos Referencia e Alterado (correspondente ao VCF)
##########  - DEPTH: valor de profundidade do variante, obtido pela coluna 'INFO', campo DP
########################################################################################################

########################################################################################################
###### IMPORTACAO DO ARQUIVO DE INPUT - VCF

def ImportaVCF(vcf_file):
    # Importa o arquivo VCF mantendo as colunas 'ID','REF','ALT'. A coluna INFO sera tranformada em 'DEPTH'
    vcf_df = pd.read_csv(vcf_file, sep='\t', 
                        comment='#', 
                        usecols = [2, 3, 4, 7],
                        names=['ID','REF','ALT','DEPTH'], 
                        )

    # Elimina as linhas sem id
    vcf_df = vcf_df.loc[vcf_df["ID"].str.startswith('rs')]

    ### EXTRAINDO INFORMAXAO DE PROFUNDIDADE
    # Entrada: depth_df ['INFO'] = AC=1;AF=0.500;AN=2;BaseQRankSum=-2.489;DB;DP=1.
    # Aqui, separa os elementos primeiro em ;, depois em =. O split em "=" vai gerar 2 elementos (DP, 1), que sao transformados em dicionario
    # No fim, ['DP'] garante que somente a informação DP permaneça
    vcf_df ['DEPTH'] = vcf_df ['DEPTH'].apply(lambda x: dict(item.split('=') 
                                                        for item in x.split(';') 
                                                        if '=' in item)['DP'])

    print(vcf_file, ' importado com sucesso!')

    return vcf_df

# TESTE DA FUNCAO VCF_to_DF
#print(VCF_to_DF(vcf_file))
##############################################################################################################