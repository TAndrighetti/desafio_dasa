

#./RUN_WORKFLOW.sh ANOT NIST_teste.vcf NIST_teste_annotation_complete.csv

OPCAO=$1
VCF_FILE=$2
OUTPUT_FILE=$3

##### ANOTACAO DOS VARIANTES

if [[ "$OPCAO" == "ANOT" ]]; then
    
    ## Construindo a imagem do docker
    docker build -t vcf_annot_image -f docker/Dockerfile .

    ## Executando a anotacao do VCF de entrada
    docker run -v $(pwd)/docker_output:/app/output vcf_annot_image --vcf_file $VCF_FILE --output /app/output/$OUTPUT_FILE


###### EXECUCAO DO API

elif [[ "$OPCAO" == "API" ]]; then
    cd ./API/

    ## 1. Construindo a imagem do docker

    docker build -t api_anotacao_image -f docker/Dockerfile docker/ .

    ## 2. Executando a anotacao do VCF de entrada
    docker run -p 5000:5000 api_anotacao_image --input_api NIST_annotation_complete.csv

fi
