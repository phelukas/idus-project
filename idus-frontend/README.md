## **Descrição**

Este é o frontend do projeto **idus**, desenvolvido com **Next.js**. Ele se conecta a uma API backend para oferecer uma interface rica e interativa ao usuário.

## **Requisitos**

- **Node.js** (versão 18 ou superior)
- **Docker** (opcional, para rodar com container)

## **Variáveis de Ambiente**

Copie o arquivo `.env.example` para `.env` e ajuste o valor abaixo, caso
necessário:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

Essa variável define a URL base utilizada pelo frontend para se comunicar com a
API backend.

## **Como Rodar o Projeto**

### **1. Usando Docker (Recomendado)**

1. Certifique-se de estar no diretório do projeto:

   ```bash
   cd idus-frontend
   ```

2. Construa e inicie o container:

   ```bash
   docker-compose up --build
   ```

3. Acesse o frontend:
   - Local: [http://localhost:3000](http://localhost:3000)

---

### **2. Rodando Localmente (Sem Docker)**

1. **Instale as Dependências**  
   Certifique-se de que o Node.js e o npm estão instalados. Instale as dependências do projeto:

   ```bash
   npm install
   ```

2. **Execute o Projeto em Modo de Desenvolvimento**  
   Inicie o servidor de desenvolvimento:

   ```bash
   npm run dev
   ```

3. **Acesse o Frontend**

   - Local: [http://localhost:3000](http://localhost:3000)

4. **Gerar Build de Produção**  
   Para criar uma build de produção:

   ```bash
   npm run build
   ```

5. **Inicie o Servidor de Produção**  
   Após gerar a build:
   ```bash
   npm start
   ```

## **Scripts Disponíveis**

Os seguintes scripts podem ser usados com `npm run`:

- `dev`: Inicia o servidor de desenvolvimento.
- `build`: Gera uma build de produção.
- `start`: Inicia o servidor em modo de produção.
- `lint`: Verifica o código com ESLint.
- `test`: Executa a suíte de testes automatizados.

## **Rodando os Testes**

Para executar os testes unitários, utilize o seguinte comando:

```bash
npm test
```
