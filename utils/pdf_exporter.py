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
        #    multi_cell() é como um text_area, ele quebra a linha automaticamente
        #    Usamos encode/decode para garantir que o FPDF2 (baseado em Python)
        #    lide corretamente com o texto que vem da IA.
        
        # Removemos o "markdown" pois o fpdf2 não o renderiza, apenas o texto.
        # Isso é uma limitação, mas garante o funcionamento.
        
        pdf.multi_cell(0, 5, md_text)
        
        # 5. Retornar os bytes
        #    Usamos .output(dest='S') para string/bytes, mas precisamos
        #    encodar para latin-1 para o Streamlit (um truque do FPDF2)
        return pdf.output(dest='S').encode('latin-1')

    except Exception as e:
        st.error(f"Erro ao gerar o PDF (fpdf2): {e}")
        return None