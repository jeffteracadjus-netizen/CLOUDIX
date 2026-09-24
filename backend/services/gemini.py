import os
import time
import google.generativeai as genai

# Aceita uma chave única ou múltiplas chaves separadas por vírgula
RAW_KEYS = os.getenv("GEMINI_API_KEY", "")
API_KEYS = [k.strip() for k in RAW_KEYS.split(",") if k.strip()]

# Lista de modelos oficiais e estáveis suportados pela Google
VALID_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-1.0-pro"
]

def ask_gemini(prompt: str, previous_interaction_id=None, retries: int = 3, delay: int = 3, **kwargs):
    """
    Envia solicitações para o Gemini testando modelos oficiais e alternando
    entre chaves e re-tentativas automáticas em caso de limite (429).
    """
    if not API_KEYS:
        return {"text": "Nenhuma chave da API do Gemini foi configurada no servidor."}

    for key_index, api_key in enumerate(API_KEYS):
        try:
            genai.configure(api_key=api_key)

            # Testa os modelos oficiais por ordem de prioridade
            for model_name in VALID_MODELS:
                try:
                    model = genai.GenerativeModel(model_name)
                    current_delay = delay

                    for attempt in range(retries):
                        try:
                            response = model.generate_content(prompt)
                            return {"text": response.text}

                        except Exception as e:
                            error_msg = str(e)

                            # Se o modelo não for encontrado (404), passa para o próximo modelo válido
                            if "404" in error_msg or "not found" in error_msg.lower():
                                break

                            # Se for erro de limite de requisições / cota (429)
                            if any(k in error_msg for k in ["429", "Quota", "Rate limit", "RESOURCE_EXHAUSTED"]):
                                if attempt < retries - 1:
                                    print(f"[Gemini] Cota atingida no modelo {model_name}. Aguardando {current_delay}s...")
                                    time.sleep(current_delay)
                                    current_delay *= 2
                                    continue
                                else:
                                    # Esgotou as tentativas para este modelo, tenta o próximo
                                    break
                            else:
                                print(f"[Gemini Error]: {error_msg}")
                                return {"text": f"Erro no processamento da IA: {error_msg}"}

                except Exception as model_err:
                    print(f"[Gemini Model Error - {model_name}]: {model_err}")
                    continue

        except Exception as key_err:
            print(f"[Gemini Key Error]: {key_err}")
            continue

    return {
        "text": "A IA está a processar um volume elevado de solicitações neste momento. Por favor, aguarde cerca de 10 a 15 segundos e envie a sua pergunta novamente."
    }