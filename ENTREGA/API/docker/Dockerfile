# Imagem do Python
FROM python:3.9-slim

# Diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de requisitos do projeto para o conteiner
COPY docker/requirements.txt /app/requirements.txt

# Instala as dependencias do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto para o conteiner
COPY src/ /app/
COPY docker/ /app/

# Expoe a porta em que o Flask vai rodar
EXPOSE 5000

# Define o comando para rodar o aplicativo Flask
ENTRYPOINT ["python", "run.py"]


