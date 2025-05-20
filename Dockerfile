# Usa a imagem oficial do Python
FROM python:3.12.8-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto
COPY . .

# Expõe a porta usada pelo Django
EXPOSE 8000

# Comando padrão: roda o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
