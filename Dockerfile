# Use a imagem Python oficial como base
FROM python:latest

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo "teste.py" para o diretório de trabalho no contêiner
COPY teste.py .

# Comando a ser executado quando o contêiner for iniciado
CMD ["python", "teste.py"]