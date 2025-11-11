import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os 

# 1. IMPORTAMOS O NOVO MÓDULO DO DASHBOARD
from modules import M0_dashboard, M1_diagnostico, M2_brainstorm, M3_design, M4_delivery, M5_qa, M6_governance, M7_refine

st.set_page_config(page_title="Automation Architect AI", page_icon="🤖", layout="wide")

# --- Bloco da Logo (sem mudanças) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo_da_empresa.png")

col1, col2 = st.columns([1, 5], vertical_alignment="center", gap="small") 

with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=100) 
    else:
        st.error("Logo não encontrada!") 

with col2:
    st.markdown(
        "<h1 style='margin-top: -20px; margin-bottom: 0px; margin-left: -40px;'>Automation Architect AI</h1>", 
        unsafe_allow_html=True
    )
# --- Fim do Bloco da Logo ---


if 'clipboard' not in st.session_state:
    st.session_state.clipboard = {
        "diagnostico_asis": "",
        "arquitetura_solucao": "",
        "design_pdd": "",
        "delivery_docs": "",
        "qa_plano": "",
        "governance_doc": "",
        "refine_output": ""
    }

if 'current_date' not in st.session_state:
    st.session_state.current_date = datetime.now().strftime("%d/%m/%Y")

try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"] 
    genai.configure(api_key=GOOGLE_API_KEY)
except KeyError:
    st.error("Erro: Chave de API do Google não encontrada no arquivo secrets.toml!")
    st.stop()
except Exception as e:
    st.error(f"Erro ao configurar a API do Google: {e}")
    st.stop()

# 2. ADICIONAMOS A "TAB 0" (DASHBOARD) NA FRENTE
tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Dashboard", # <-- A NOVA ABA
    "💡 1. Diagnóstico (AS-IS)", 
    "🧠 2. Arquitetura (Solução)", 
    "✍️ 3. Design (TO-BE)", 
    "📄 4. Delivery (Docs)", 
    "🧪 5. QA & Testes",
    "📜 6. Governança (Final)",
    "🔄 7. Refinar" 
])

# 3. ADICIONAMOS A LÓGICA DA "TAB 0"
with tab0:
    M0_dashboard.run()

with tab1:
    M1_diagnostico.run()

with tab2:
    M2_brainstorm.run()

with tab3:
    M3_design.run()

with tab4:
    M4_delivery.run()

with tab5:
    M5_qa.run()

with tab6:
    M6_governance.run()

with tab7:
    M7_refine.run()