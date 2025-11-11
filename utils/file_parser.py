import streamlit as st
import pdfplumber
import docx
import io

def parse_file(uploaded_file):
    """
    Recebe um UploadedFile do Streamlit e extrai o texto.
    Retorna uma string com o texto extraído.
    """
    file_type = uploaded_file.type
    text = ""
    
    try:
        # Lendo PDF
        if file_type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            
        # Lendo DOCX
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            for para in doc.paragraphs:
                text += para.text + "\n"
        
        # Lendo TXT
        elif file_type == "text/plain":
            text = uploaded_file.read().decode("utf-8")
        
        else:
            st.warning(f"Tipo de arquivo '{file_type}' não suportado: {uploaded_file.name}")
            return None

        return f"\n--- INÍCIO DO DOCUMENTO: {uploaded_file.name} ---\n{text}\n--- FIM DO DOCUMENTO: {uploaded_file.name} ---\n"
    
    except Exception as e:
        st.error(f"Erro ao ler o arquivo {uploaded_file.name}: {e}")
        return None