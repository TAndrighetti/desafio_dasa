import requests
import pandas as pd

###########################################################################################################
################################### ANOTANDO VARIANTES (BD VEP) ###########################################
###########################################################################################################
########## Esse codigo realiza anotacoes de variantes individuais a partir do bando de dados VEP (ENSEMBL).
##########
########## INPUT: dbSNP_id, nucleotideo alterado
########## 
########## OUTPUT: retorna as seguintes variaveis:
##########  - id: dbSNSP id (correspondente ao VCF)
##########  - gene_symbol: gene associado a variante
##########  - gene_id: gene id associado a variante no banco de dados ENSEMBL
##########  - frequencias: frequencias do gene de acordo com diferentes localizacoes e banco de dados
##########  -- formato: 'gnomadg_amr:0.8811,gnomade:0.8865,gnomade_nfe:0.9059,gnomade_fin:0.9316
############################################################################################################

############################################################################################################
###### FUNCAO PARA ANOTACAO DOS VARIANTES VIA VEP
def AnotaVariante(id, nucl):

    #######################################################
    #### ACESSO AO BANCO DE DADOS
    # Acessa o API do banco de dados, fornecendo o id como input
    server = "https://rest.ensembl.org"
    ext = f"/vep/human/id/{id}?"
 
    response = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    # Verifica a resposta e, caso tenha tido sucesso, armazena os dados como json na variant_annotation e continua o script
    if response.ok:
        variant_annotation = response.json()
        
        #######################################################
        ############## EXTRAINDO INFORMACOES DE FREQUENCIAS
        # Alguns variantes faltam informacoes. Desse modo, eu testo com "try"
        try:
            # Extrai a tabela que contem a lista de possiveis variantes (colocated_variants)
            # Se existirem para quele variante, as frequencias estarao nessa tabela
            colocated_variants = pd.DataFrame.from_records(variant_annotation[0]['colocated_variants'])
            
            # Se as informacoes de frequencias existirem p/ aquele variante, serao armazenadas na variavel 'frequencia'
            if 'frequencies' in colocated_variants.keys():                
                frequencies = dict(colocated_variants.loc[~colocated_variants['frequencies'].isnull()]['frequencies'])             
                frequencies = [frequencies[n][nucl] for n in frequencies.keys()][0]
                
            # Variantes sem informacoes de frequencia: 
            # Normalmente elas estao relacionadas a outros bancos de dados. 
            # Se esse for o caso, ao inves de ele retornar as frequencias, retornara os ids desses BDs
            else:
                frequencies = {'var_id':" ".join(list(colocated_variants['id']))}
        
        # No caso de 'colocated_variants'nao existir para aquele variante, eu anoto as frequencias como "Missing information"
        except KeyError:
            frequencies = {"Missing information":"Frequency is not available for this alteration"}
      

        #######################################################
        ############# GENE INFORMATION
        try:        
            # Na tabela 'transcript_consequences' estao presentes informacoes de gene
            transcript_consequences = pd.DataFrame.from_records(variant_annotation[0]['transcript_consequences'])
            
            # - Se existirem informacoes para o nucleotideo correspondente determinado no vcf (coluna 'ALT'), 
            # essa informacao sera armazenada na variavel 'transcript_consequences' 
            # - Se nao tiver p/ aquele nucleotideo especifico, ele vai manter o transcript_consequences antigo 
            # e vai anotar informacoes para os outros nucleotideos

            if nucl in set(transcript_consequences['variant_allele']):
                transcript_consequences = transcript_consequences.loc[transcript_consequences['variant_allele'] == nucl]  
                
            gene_symbol = {}
            gene_id = {}

            for variant_allele, gene_symbol_val, gene_id_val in zip(
                    transcript_consequences['variant_allele'],
                    transcript_consequences['gene_symbol'],
                    transcript_consequences['gene_id']):
    
                gene_symbol[variant_allele] = gene_symbol_val
                gene_id[variant_allele] = gene_id_val

        # Se a informacao nao existir na anotacao, sera anotada como "Missing information"
        except KeyError:
            gene_id = gene_symbol = {"Missing": "Information"}

    # Se o gene nao existir no banco de dados VEP, sera anotado como "Missing information"
    else:
        gene_id = gene_symbol = frequencies = {'Missing information':'ID not found on VEP'}
        

    #return variant_annotation, frequencies, colocated_variants
    return id, gene_symbol, gene_id, frequencies

##############################################################################################################

##############################################################################################################
################## TESTES:
# INPUT FILE:
vcf_file = "./teste.vcf"



##### TESTE INDIVIDUAL:
#dbSNP_id, gene_symbol, gene_id, frequencies = RetrieveAnnotation('rs1009155','A')
#print(dbSNP_id, gene_symbol, gene_id, frequencies)
##############################################################################################################