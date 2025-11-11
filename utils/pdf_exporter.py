import markdown2
from xhtml2pdf import pisa
import streamlit as st
import os
import io
import base64  # <-- Importamos para embutir as fontes

def create_pdf_bytes(md_text):
    """
    Converte uma string Markdown em bytes de um arquivo PDF usando xhtml2pdf (pisa).
    Esta versão EMBUTE as fontes em Base64 para evitar bugs de arquivo 'Temp' no Windows.
    """
    try:
        # 1. Definir os caminhos para as fontes
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ASSETS_DIR = os.path.join(BASE_DIR, '..', 'assets')
        
        FONT_REGULAR_PATH = os.path.join(ASSETS_DIR, 'DejaVuSans.ttf')
        FONT_BOLD_PATH = os.path.join(ASSETS_DIR, 'DejaVuSans-Bold.ttf')
        FONT_ITALIC_PATH = os.path.join(ASSETS_DIR, 'DejaVuSans-Oblique.ttf')
        FONT_BOLDITALIC_PATH = os.path.join(ASSETS_DIR, 'DejaVuSans-BoldOblique.ttf')

        # 2. Ler os arquivos de fonte e codificá-los em Base64
        def get_base64_font(font_path):
            if not os.path.exists(font_path):
                st.error(f"Erro Crítico: Fonte não encontrada em {font_path}")
                return None
            with open(font_path, "rb") as f:
                return base64.b64encode(f.read()).decode('utf-8')

        font_regular_b64 = get_base64_font(FONT_REGULAR_PATH)
        font_bold_b64 = get_base64_font(FONT_BOLD_PATH)
        font_italic_b64 = get_base64_font(FONT_ITALIC_PATH)
        font_bolditalic_b64 = get_base64_font(FONT_BOLDITALIC_PATH)

        if not all([font_regular_b64, font_bold_b64, font_italic_b64, font_bolditalic_b64]):
            st.error("Falha ao carregar uma ou mais fontes da pasta 'assets'. Verifique se todos os 4 arquivos 'DejaVuSans...' estão lá.")
            return None

        # 3. Converter Markdown para HTML
        html = markdown2.markdown(
            md_text, 
            extras=["tables", "fenced-code-blocks", "cuddled-lists"]
        )

        # 4. Criar o CSS com as fontes EMbutidas (Base64)
        css_style = f"""
        @font-face {{
            font-family: 'DejaVu';
            src: url(data:application/font-ttf;charset=utf-8;base64,{font_regular_b64});
            font-weight: normal; font-style: normal;
        }}
        @font-face {{
            font-family: 'DejaVu';
            src: url(data:application/font-ttf;charset=utf-8;base64,{font_bold_b64});
            font-weight: bold; font-style: normal;
        }}
        @font-face {{
            font-family: 'DejaVu';
            src: url(data:application/font-ttf;charset=utf-8;base64,{font_italic_b64});
            font-weight: normal; font-style: italic;
        }}
        @font-face {{
            font-family: 'DejaVu';
            src: url(data:application/font-ttf;charset=utf-8;base64,{font_bolditalic_b64});
            font-weight: bold; font-style: italic;
        }}

        /* Estilos gerais */
        body {{ 
            font-family: 'DejaVu', 'Arial', sans-serif; 
            line-height: 1.5; 
            font-size: 11px; 
        }}
        h1 {{ font-size: 24px; }}
        h2 {{ font-size: 18px; }}
        h3 {{ font-size: 14px; }}
        table {{ 
            border-collapse: collapse; 
            width: 100%; 
            margin-top: 10px; 
            margin-bottom: 10px; 
        }}
        th, td {{ 
            border: 1px solid #ddd; 
            padding: 8px; 
            text-align: left; 
            page-break-inside: avoid; 
        }}
        th {{ background-color: #f2f2f2; }}
        pre {{ 
            background-color: #f5f5f5; 
            padding: 10px; 
            border: 1px solid #ddd; 
            border-radius: 4px; 
            overflow-x: auto; 
            page-break-inside: avoid; 
        }}
        code {{ font-family: 'Courier New', Courier, monospace; }}
        ul, ol {{ padding-left: 20px; }}
        """

        # 5. Criar o documento HTML final
        html_with_style = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>{css_style}</style>
        </head>
        <body>{html}</body>
        </html>
        """
        
        # 6. Criar um buffer de bytes para o PDF
        result = io.BytesIO()

        # 7. Gerar o PDF
        #    REMOVEMOS o 'path=FONT_DIR' e o 'link_callback'.
        #    Eles não são mais necessários, pois as fontes estão embutidas.
        pdf = pisa.CreatePDF(
            html_with_style,    # o HTML
            dest=result,        # o buffer de saída
        )
        
        # 8. Retornar os bytes
        if not pdf.err:
            return result.getvalue()
        else:
            st.error(f"Erro ao gerar o PDF (xhtml2pdf): {pdf.err}")
            return None

    except Exception as e:
        st.error(f"Erro ao gerar o PDF: {e}")
        return None