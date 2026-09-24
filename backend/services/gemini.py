import os
import time
import google.generativeai as genai

# Configura a chave de API do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def ask_gemini(prompt: str, retries: int = 3, delay: int = 3):
    """
    Envia solicitações para o Gemini com sistema de re-tentativa automática (retry pattern)
    em caso de limite de requisições excedido (Erro 429).
    """
    if not GEMINI_API_KEY:
        return {"text": "Chave da API do Gemini não configurada no servidor."}

    model = genai.GenerativeModel("gemini-1.5-flash")

    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return {"text": response.text}

        except Exception as e:
            error_msg = str(e)

            # Verifica se o erro é de cota/limite de requisições (429)
            if any(k in error_msg for k in ["429", "Quota", "Rate limit", "RESOURCE_EXHAUSTED"]):
                if attempt < retries - 1:
                    print(
                        f"[Gemini] Cota temporária atingida. Aguardando {delay}s (Tentativa {attempt + 1}/{retries})..."
                    )
                    time.sleep(delay)
                    delay *= 2  # Aumenta o tempo de espera (3s, 6s, 12s)
                    continue

            print(f"[Gemini Error]: {error_msg}")
            return {
                "text": "A IA está com um alto volume de requisições no momento. Por favor, tente enviar sua pergunta novamente em alguns segundos."
            }