# DESAFIO DASA: API PARA FILTRAGEM DE VARIANTES

Olá, equipe Dasa!

Agradeço pela oportunidade de estar participando deste processo seletivo.

Espero que os resultados que trago cumpram suas expectativas.
 
Por favor, leiam este README para explicações e instruções.
 

## Overview do Workflow

De acordo com a descrição do teste, foi solicitada a construção de uma "API e uma interface interativa web (flask) que interaja com a API para filtrar variantes por frequência e profundidade (DP)" a partir do arquivo .vcf enviado.
Para isso, desenvolvi esse workflow que foi dividido em duas etapas:


### **1. Anotação do VCF**

Nessa etapa, os genes do arquivo foram anotados com o banco de dados VEP a partir de seu API. Para a construção do API, essa etapa é opcional, pois já forneço a anotação completa do arquivo para a sua construção. 

**Banco de dados VEP:** 
banco de dados de variantes oficial do ENSEMBL. Fornece informações completas sobre os genes e frequências dos variantes, incluindo seu valor para cada população.

**Realização de testes:**
Para agilizar os testes, criei um arquivo menor, `NIST_teste.vcf`, e o coloquei na pasta `dados`. É importante ressaltar que a anotação do arquivo completo levou cerca de 24 horas devido à complexidade do processo.

**Execução do código:**
A anotação completa é executada pelo código `anotacao_completa.py`, que é executado na linha de comando da seguinte forma:

```bash

python anotacao_completa.py --vcf_file "../dados/NIST_teste.vcf" --output "../dados/NIST_teste_annotation_complete.csv"

```
sendo que:
> **- - vcf_file** consiste nos dados de entrada, o arquivo .vcf a ser anotado
> **- - output** consiste no nome para arquivo de anotação completa

Anotação é subdividida em 4 etapas, que contém um módulo (função) cada uma. Estes módulos estão presentes na pasta `src/`.

#### 1. Módulo `ImportaVCF`:
Esta função importa e processa o arquivo VCF de entrada para ser submetido à anotação.

A função:
- Filtra as variantes, mantendo somente aquelas que apresentam seu ID disponível; 
- Filtra a estrutura do VCF , mantendo somente as colunas que serão utilizadas;
- Extrai o valor de profundidade (Depth) que está contido na coluna INFO.

> INPUT: arquivo VCF com as seguintes colunas obrigatórias: 'ID', 'REF', 'ALT' e 'INFO'.

> OUTPUT: dataframe contendo as seguintes informações:
> - ID: dbSNSP id (correspondente ao VCF)
>  - REF e ALT: nucleotideos Referencia e Alterado (correspondente ao VCF)
> - DEPTH: valor de profundidade do variante, obtido pela coluna 'INFO', campo DP

#### 2. Módulo AnotaVariante
Esta função realiza anotações de variantes individualmente a partir do banco de dados VEP.

Para isto, ela:
- Acessa o API REST do VEP e obtém as anotações em JSON;
- Extrai as informações de Gene_Symbol e Gene_ID da variante para incluir na tabela;
- Extrai as informações de frequência de todas as populações, caso estejam disponíveis;
- Resolve exceções de variantes:
- - que não possuem informação de frequência
- - que não possuem informações de genes
- - que não estão disponíveis no banco de dados VEP
- - Para isto, ele adiciona a informação de "Missing information" na tabela de anotação.

> INPUT: dbSNP_id, nucleotideo alterado

> OUTPUT: retorna as seguintes variaveis:
> - *id:* dbSNSP id (correspondente ao VCF)
>  - *gene_symbol:* gene associado a variante
> - *gene_id:* gene id associado a variante no banco de dados ENSEMBL
> - *frequencias:* frequencias do gene de acordo com diferentes localizacoes e banco de dados
> - - *formato das frequências:* 'gnomadg_amr:0.8811,gnomade:0.8865,gnomade_nfe:0.9059,gnomade_fin:0.9316

#### 3. Módulo AnotaVCF
Este módulo anota o *dataframe* gerado pela função `ImportaVCF` para anotar o arquivo VCF completo utilizando a função `AnotaVariante`, retornando um arquivo .csv, com as informações de anotação.

> INPUT: dataframe criado a partir do VCF (modulo_importaVCF)

> OUTPUT: arquivo (input)_annotation_raw.csv contendo as seguintes colunas:
> - *ID:* dbSNSP id (correspondente ao VCF)
> - *REF* e *ALT*: nucleotideos Referencia e Alterado (correspondente ao VCF)
> - GENE_SYMBOL: gene associado a variante>
> - GENE_ID: gene id associado a variante no banco de dados ENSEMBL
> - FREQUENCIES: frequencias do gene de acordo com diferentes localizacoes e banco de dados

#### 4. Módulo ProcessaAnotacao
O arquivo anotado gerado pelo módulo `AnotaVCF` contém os dados de frequência em uma única coluna e também mantém as informações de variantes com informações faltantes. Este arquivo é útil para manter a informação dos variantes aos quais estão faltando dados.

No entanto, para submeter ao filtro do API é mais apropriado que estes dados sejam filtrados, excluindo variantes com informação de frequência faltantes e separando as frequências de diferentes populações em colunas. A função `ProcessaAnotacao` realiza essa filtragem, retornando o último arquivo anotado.

> INPUT: arquivo de anotacao crua originado do AnotaVCF

> OUTPUT: arquivo (input)_annotation_raw.csv contendo as seguintes informacoes:
> - ID: dbSNSP id (correspondente ao VCF)
> - REF e ALT: nucleotideos Referencia e Alterado (correspondente ao VCF)
> - GENE_SYMBOL: gene associado a variante
> - GENE_ID: gene id associado a variante no banco de dados ENSEMBL
> - COLUNAS DE FREQUENCIAS inviduais de acordo com diferentes populacoes e banco de dados

### Desenvolvimento do API

A segunda etapa consiste no desenvolvimento do API, utilizando com o pacote Python Flask (como solicitado).

Como entrada, o API utilizará o arquivo de anotação completo (anotado e processado) resultado da etapa n° 1. Para isto, poderão ser usados:

1. o arquivo `NIST_annotation_complete.vcf`, que consiste no arquivo completo de anotação do arquivo .vcf fornecido

2. o arquivo `NIST_teste_annotation_complete.vcf`, que consiste no arquivo de teste gerado pelo `NIST_teste.vcf`.
 
Quando executado, o código do API retorna uma interface interativa que permite:
1. Fornecer ids para obter sua anotação completa
2. Entrar com números mínimos e máximos de frequência e profundidade para a filtragem ser realizada
3. Filtrar os resultados por população e bancos de dados (gnomeDB e 1000Genomes)

Como resultado, o API retorna uma tabela com as anotações dos variantes selecionados.

Todos os arquivos do desenvolvimento do API estão contidos na pasta `API`.

A execução do API está contida no código `run.py` e ocorre a partir do template `template/index.html`.

O arquivo `NIST_anotacao_completa.csv` é o arquivo padrão para executar o API, pois contém a anotação completa do VCF e também está contido na pasta `API`.

## Instruções para execução
As duas etapas estão containerizadas em dockers separados, para que sua execução possa ser flexibilizada.

1. A primeira etapa é fazer o download do diretório pelo git
2. No terminal, acessar o diretório ENTREGA.

3. Agora, execute o código `RUN_WORKFLOW.sh`
```bash
./RUN_WORKFLOW.sh OPCAO INPUT_FILE OUTPUT_FILE
```
utilizando as seguintes opções:
> **OPCAO:**
>  - **ANOT** : para executar somente a parte da anotação
>  -- *Sintaxe:*
>  `./RUN_WORKFLOW.sh ANOT INPUT_FILE OUTPUT_FILE`
>   -- *Teste:*
>  `./RUN_WORKFLOW.sh ANOT NIST_teste.vcf NIST_teste_annotation_complete.csv`
>  
>>  *INPUT_FILE:* arquivo VCF de entrada para a anotação. 
>>
> > *OUTPUT_FILE:* nome do arquivo de saída. Por padrão, os arquivos anotados estarão no diretório `docker_output/` . 
>
>
>  - **API** : para executar somente a API.
>  Por padrão, vai executar a API já com o arquivo de anotações completas.
>  
>  -- *Sintaxe:*
>  `./RUN_WORKFLOW.sh`

O API será disponibilizado na URL http://127.0.0.1:5000/ .
