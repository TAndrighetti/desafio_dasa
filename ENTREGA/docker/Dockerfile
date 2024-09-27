# Python image
FROM python:3.10-slim

# Permite monitorar as saidas do codigo em tempo real
ENV PYTHONUNBUFFERED=1

# Diretorio de trabalho dentro do container
WORKDIR /app

# Copia os arquivos necessarios para dentro do container
COPY docker/ /app/
COPY dados/ /app/
COPY src/ /app/

# Instala os pacotes requisitados
RUN pip install --no-cache-dir -r requirements.txt

# Arruma para que os argumentos de entrada possam ser fonecidos na linha de comando
ENTRYPOINT ["python", "anotacao_completa.py"]
