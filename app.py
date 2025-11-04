import streamlit as st
import google.generativeai as genai
from datetime import datetime

from modules import M1_diagnostico, M2_brainstorm, M3_design, M4_delivery, M5_qa, M6_governance, M7_refine

st.set_page_config(page_title="Automation Architect AI", page_icon="🤖", layout="wide")
st.title("🤖 Automation Architect AI")

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

# --- NAVEGAÇÃO EM ABAS (Com Nomes Corrigidos) ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💡 1. Diagnóstico (AS-IS)", 
    "🧠 2. Arquitetura (Solução)", 
    "✍️ 3. Design (TO-BE)", 
    "📄 4. Delivery (Docs)", 
    "🧪 5. QA & Testes",
    "📜 6. Governança (Final)",
    "🔄 7. Refinar" 
])

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