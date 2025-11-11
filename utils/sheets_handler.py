import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
]

SHEET_URL = "https://docs.google.com/spreadsheets/d/1szufRBTdixoD92thGvGTgdpDGLVOVr5XLsJjWN3lisM/edit?gid=0#gid=0" 

def get_sheets_client():
    try:
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        client = gspread.authorize(creds)
        return client
    except KeyError:
        st.error("Erro Crítico: Configuração 'gcp_service_account' não encontrada no secrets.toml.")
        return None
    except Exception as e:
        st.error(f"Erro ao autenticar com Google Sheets: {e}")
        return None

def save_to_sheet(project_name, doc_type, content):
    client = get_sheets_client()
    if client is None:
        st.error("Falha ao conectar com o Google Sheets. O projeto NÃO foi salvo.")
        return False
    
    try:
        sheet = client.open_by_url(SHEET_URL).sheet1
        
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        new_row = [current_date, project_name, doc_type, content]
        
        sheet.append_row(new_row)
        return True
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Erro: Planilha não encontrada pela URL. Verifique o link e as permissões de compartilhamento.")
        return False
    except Exception as e:
        st.error(f"Erro ao salvar na planilha: {e}")
        return False

def load_from_sheet():
    client = get_sheets_client()
    if client is None:
        st.error("Falha ao conectar com o Google Sheets. Não foi possível carregar o histórico.")
        return [] 
    
    try:
        sheet = client.open_by_url(SHEET_URL).sheet1
        
        # Pega TODOS os registros da planilha e os retorna como uma lista de dicionários
        records = sheet.get_all_records()
        return records
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Erro: Planilha não encontrada pela URL. Verifique o link e as permissões de compartilhamento.")
        return []
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        return []