from fpdf import FPDF
import streamlit as st
import os

def create_pdf_bytes(md_text):
    """
    Converte uma string Markdown (texto) em bytes de um arquivo PDF.
    Esta versão usa FPDF2 de forma simples (sem HTML) para garantir
    compatibilidade com o Streamlit Cloud e caracteres Unicode.
    """
    try:
        # 1. Definir o caminho para a fonte (só precisamos da regular)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FONT_PATH = os.path.join(BASE_DIR, '..', 'assets', 'DejaVuSans.ttf')

        if not os.path.exists(FONT_PATH):
            st.error(f"Erro Crítico: Fonte 'DejaVuSans.ttf' não encontrada na pasta 'assets'!")
            return None

        # 2. Configurar o PDF
        pdf = FPDF()
        
        # 3. Adicionar a fonte Unicode
        pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
        pdf.set_font('DejaVu', '', 11)
        
        pdf.add_page()
        
        # 4. Escrever o texto
        pdf.multi_cell(0, 5, md_text)
        
        # --- INÍCIO DA CORREÇÃO ---
        # 5. Retornar os bytes
        #    Removemos o 'dest="S"'. Chamando .output() sem argumentos
        #    (ou com dest='B') retorna o formato 'bytes' que o st.download_button espera.
        return pdf.output()
        # --- FIM DA CORREÇÃO ---

    except Exception as e:
        st.error(f"Erro ao gerar o PDF (fpdf2): {e}")
        return None