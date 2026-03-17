import os
import re
import json
import time
import logging
import requests
import gspread
import pytz
from datetime import datetime
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials
from tenacity import retry, stop_after_attempt, wait_exponential

# --- 1. CONFIGURAÇÃO DE LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('whatsapp_channels.log', encoding='utf-8')]
)
logger = logging.getLogger(__name__)

# --- 2. CONFIGURAÇÕES E CONSTANTES ---
# (Carregadas das variáveis de ambiente)
try:
    GSPREAD_CREDENTIALS = os.getenv("GSPREAD_CREDENTIALS")
    SHEET_ID = os.getenv("SEGUIDORES_SHEETS_ID")
    SHEET_NAME = "SEGUIDORES"
    
    if not GSPREAD_CREDENTIALS or not SHEET_ID:
        raise ValueError("Variáveis de ambiente GSPREAD_CREDENTIALS ou SEGUIDORES_SHEETS_ID não configuradas.")
except Exception as e:
    logger.error(f"Erro na configuração inicial: {e}")
    exit(1)

# --- 3. FUNÇÕES DE APOIO ---

def conectar_google_sheets():
    """Faz a autenticação e retorna a aba da planilha."""
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds_dict = json.loads(GSPREAD_CREDENTIALS)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        
        workbook = client.open_by_key(SHEET_ID)
        return workbook.worksheet(SHEET_NAME)
    except Exception as e:
        logger.error(f"Erro ao conectar ao Google Sheets: {e}")
        raise

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def extrair_dados_canal(url):
    """Acessa a URL e extrai UF (Nome Completo) e Seguidores."""
    logger.info(f"🔍 Coletando: {url}")
    
    # 1. Atualizamos os headers para exigir o idioma Português (pt-BR)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7' 
    }
    
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    
    uf = "Nome não encontrado"
    seguidores = "Não encontrado"
    
    # 2. Extração do Nome Completo do Canal
    uf_elements = soup.find_all('h1')
    if uf_elements:
        uf = uf_elements[0].get_text(strip=True)

    # 3. Extração de Seguidores (Procurando nos H5)
    followers_elements = soup.find_all('h5')
    
    if followers_elements:
        for h5 in followers_elements:
            # Obtém o texto e substitui espaços invisíveis
            text = h5.get_text(strip=True).replace('\xa0', ' ')
            texto_minusculo = text.lower()
            
            # 4. Verifica se contém a palavra em Português ou em Inglês
            if 'seguidores' in texto_minusculo or 'followers' in texto_minusculo:
                
                # Extrai a partir do ponto separador
                if '•' in text:
                    seguidores = text.split('•')[-1].strip()
                # Mantém retrocompatibilidade caso usem a barra no futuro
                elif '|' in text:
                    seguidores = text.split('|')[-1].strip()
                else:
                    seguidores = text
                    
                break # Encontrou a informação, sai do loop

    # 5. Data e Hora da extração
    data_hora = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
    
    return [uf, seguidores, data_hora]

def obter_urls():
    """Retorna a lista de URLs dos canais."""
    return [
        "https://www.whatsapp.com/channel/0029VaMaH2l7NoZtWIOSpF42",
        "https://www.whatsapp.com/channel/0029VaMOOc5HAdNSlwzilF2D",
        "https://www.whatsapp.com/channel/0029VaHojqwEgGfINHRdaM1O",
        "https://www.whatsapp.com/channel/0029VaLj0w390x34dqUFAF2D",
        "https://www.whatsapp.com/channel/0029VaH4XZl2kNFrIiqJhW1v",
        "https://www.whatsapp.com/channel/0029VaFUMFDGehERivTfl82c",
        "https://www.whatsapp.com/channel/0029VaKFcgZGpLHMbLtVip0o",
        "https://www.whatsapp.com/channel/0029VaH6EZQ4tRrxV1Nmsu22",
        "https://www.whatsapp.com/channel/0029VaFqLpxBA1ex71Tia73C",
        "https://www.whatsapp.com/channel/0029VaMadWRKrWR4SXOSRs3f",
        "https://www.whatsapp.com/channel/0029VaHQV6cATRSjG1Bexg0I",
        "https://www.whatsapp.com/channel/0029VaLwpQm8V0thNF0kTU3x",
        "https://www.whatsapp.com/channel/0029VaLLddhHFxP740WKOr20",
        "https://www.whatsapp.com/channel/0029VaMptPtH5JLvbdNuEh0E",
        "https://www.whatsapp.com/channel/0029VaLWrXy05MUautn3nK1o",
        "https://www.whatsapp.com/channel/0029VaH7vkPGpLHMNt77eA2k",
        "https://www.whatsapp.com/channel/0029VaFqKSa7T8bQZZGFp220",
        "https://www.whatsapp.com/channel/0029VaM1F3OD38CNgvxDlD1Q",
        "https://www.whatsapp.com/channel/0029VaGuQ6q5kg7BmGs3bP3M",
        "https://www.whatsapp.com/channel/0029VaLwsAA3wtb93fsLKO1T",
        "https://www.whatsapp.com/channel/0029VaM52Mh3rZZUK0TPFX06",
        "https://www.whatsapp.com/channel/0029VaHL41DKrWQqgTNZmM3x",
        "https://www.whatsapp.com/channel/0029VaLRJlfEFeXrQ7UGdN1v",
        "https://www.whatsapp.com/channel/0029VaF71dxE50UrLuWGn62e",
        "https://www.whatsapp.com/channel/0029VaM5VQWCXC3NUN03Sf35",
        "https://www.whatsapp.com/channel/0029VaFtyKR65yDDETsmH40A",
        "https://www.whatsapp.com/channel/0029VaHECYE8fewh3S5aAQ2Q"
    ]

# --- 4. FLUXO PRINCIPAL (ORQUESTRADOR) ---

def main():
    logger.info("🚀 Iniciando processo de coleta...")
    
    try:
        # 1. Conecta na planilha
        aba = conectar_google_sheets()
        urls = obter_urls()
        
        sucesso = 0
        falha = 0
        
        # 2. Loop de processamento
        for i, url in enumerate(urls, 1):
            try:
                # Extrai dados
                dados = extrair_dados_canal(url)
                
                # Salva na planilha (colunas A, B, C)
                aba.append_row(dados)
                
                logger.info(f"✅ [{i}/{len(urls)}] Salvo: {dados[0]} | {dados[1]}")
                sucesso += 1
                
                # Delay para evitar bloqueios
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar canal {url}: {e}")
                falha += 1

        # 3. Relatório Final
        logger.info("-" * 30)
        logger.info(f"Concluído! Sucesso: {sucesso} | Falhas: {falha}")
        
    except Exception as e:
        logger.error(f"💥 Erro fatal: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
