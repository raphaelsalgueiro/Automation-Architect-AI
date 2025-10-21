import streamlit as st
import google.generativeai as genai

from modules import M1_discovery, M2_design, M3_delivery, M4_qa

st.set_page_config(page_title="Automation Architect AI", page_icon="🤖", layout="wide")
st.title("🤖 Automation Architect AI")

GOOGLE_API_KEY = "AIzaSyAi93gAzIjbMHhM_i9aF-YFeALsMwYj7kM"
genai.configure(api_key=GOOGLE_API_KEY)

tab_discovery, tab_design, tab_delivery, tab_qa = st.tabs([
    "💡 Discovery", 
    "✍️ Design", 
    "📄 Delivery", 
    "🧪 QA & Testes"
])

with tab_discovery:
    M1_discovery.run()

with tab_design:
    M2_design.run()

with tab_delivery:
    M3_delivery.run()

with tab_qa:
    M4_qa.run()