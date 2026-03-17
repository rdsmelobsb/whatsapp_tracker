```markdown
# 📊 WhatsApp Channels Scraper

Um script em Python para extrair o nome e a quantidade de seguidores de canais do WhatsApp e salvar os dados automaticamente em uma planilha do Google Sheets.

## 🚀 O que o projeto faz?
1. Acessa as URLs de canais do WhatsApp cadastradas no código.
2. Coleta o nome do canal e o número de seguidores em tempo real.
3. Salva esses dados, junto com a data e a hora, em uma aba chamada "SEGUIDORES" no Google Sheets.

## 🛠️ Como usar

### 1. Instale as bibliotecas necessárias
Abra o seu terminal e instale as dependências do projeto com o comando abaixo:
```bash
pip install requests beautifulsoup4 lxml gspread google-auth tenacity pytz
```

### 2. Configure o Google Sheets
1. Crie uma planilha no Google Sheets com uma aba chamada exatamente **SEGUIDORES**.
2. Crie uma **Conta de Serviço (Service Account)** no Google Cloud e baixe o arquivo JSON com as credenciais.
3. Compartilhe a sua planilha (como Editor) com o e-mail da conta de serviço.

### 3. Configure as Variáveis de Ambiente
O código precisa de duas variáveis no seu sistema operacional para conseguir acessar a planilha:
* `SEGUIDORES_SHEETS_ID`: O ID da sua planilha (você encontra na URL do navegador).
* `GSPREAD_CREDENTIALS`: O conteúdo completo do arquivo JSON baixado do Google Cloud.

### 4. Rode o código
Com tudo configurado, basta executar o arquivo Python no seu terminal:
```bash
python whatsapp_scrapper.py
```
Você verá o progresso no terminal e, em poucos segundos, os dados começarão a aparecer na sua planilha!
```
