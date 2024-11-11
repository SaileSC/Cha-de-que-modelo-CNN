# Use uma imagem base do Python com a versão desejada
FROM python:3.11-slim

# Configure o diretório de trabalho
WORKDIR /app

# Copie o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o contêiner
COPY . .

# Exponha a porta na qual o Flask será executado
EXPOSE 80

# Comando para iniciar a aplicação
CMD ["python", "server.py"]
