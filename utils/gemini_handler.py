import google.generativeai as genai

def call_gemini_api(prompt_text):
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"Ocorreu um erro ao chamar a API do Gemini: {e}"