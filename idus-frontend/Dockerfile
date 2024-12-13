FROM node:20-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copiar arquivos necessários e instalar dependências
COPY package.json package-lock.json /app/
RUN npm install --no-cache --legacy-peer-deps \
    && rm -rf /tmp/* /var/cache/apk/* /root/.npm /root/.cache

# Copiar o restante do código da aplicação
COPY . /app/

# Construir a aplicação (gera arquivos de build)
RUN npm run build \
    && rm -rf /tmp/* /var/cache/apk/* /root/.npm /root/.cache

# Expor a porta da aplicação
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["npm", "run", "start"]
