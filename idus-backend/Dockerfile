FROM python:3.12-slim

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    postgresql-client \
    locales \  
    && rm -rf /var/lib/apt/lists/*

# Configurar e gerar a localidade pt_BR.UTF-8
RUN sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

# Definir variáveis de ambiente para a localidade
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

# Copiar e instalar as dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Adicionar o script de espera pelo banco de dados
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Copiar o restante do código da aplicação
COPY . /app/

# Expor a porta da aplicação
EXPOSE 8000

# Comando para iniciar o servidor Django
CMD ["./wait-for-db.sh", "db", "python", "manage.py", "runserver", "0.0.0.0:8000"]
