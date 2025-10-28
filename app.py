import streamlit as st
import google.generativeai as genai

from modules import M1_discovery, M2_design, M3_delivery, M4_qa, M5_refine

st.set_page_config(page_title="Automation Architect AI", page_icon="🤖", layout="wide")
st.title("🤖 Automation Architect AI")

try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"] 
    genai.configure(api_key=GOOGLE_API_KEY)
except KeyError:
    st.error("Erro: Chave de API do Google não encontrada no arquivo secrets.toml!")
    st.stop()
except Exception as e:
    st.error(f"Erro ao configurar a API do Google: {e}")
    st.stop()

tab_discovery, tab_design, tab_delivery, tab_qa, tab_refine = st.tabs([
    "💡 Discovery", 
    "✍️ Design", 
    "📄 Delivery", 
    "🧪 QA & Testes",
    "🔄 Refinar" 
])

with tab_discovery:
    M1_discovery.run()

with tab_design:
    M2_design.run()

with tab_delivery:
    M3_delivery.run()

with tab_qa:
    M4_qa.run()

with tab_refine:
    M5_refine.run()