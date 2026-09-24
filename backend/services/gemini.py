import os
import time
import google.generativeai as genai

# Aceita uma chave única ou múltiplas chaves separadas por vírgula no Render
RAW_KEYS = os.getenv("GEMINI_API_KEY", "")
API_KEYS = [k.strip() for k in RAW_KEYS.split(",") if k.strip()]


def ask_gemini(
    prompt: str,
    previous_interaction_id=None,
    retries: int = 3,
    delay: int = 5,
    **kwargs
):
    """
    Envia solicitações para o Gemini com suporte a rotação de chaves
    e tentativas automáticas em caso de limite de cota (Erro 429).
    """
    if not API_KEYS:
        return {"text": "Nenhuma chave da API do Gemini foi configurada no servidor."}

    # Percorre as chaves de API disponíveis se uma delas atingir o limite
    for key_index, api_key in enumerate(API_KEYS):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            current_delay = delay
            for attempt in range(retries):
                try:
                    response = model.generate_content(prompt)
                    return {"text": response.text}

                except Exception as e:
                    error_msg = str(e)

                    # Se for limite de requisições / cota excedida (429)
                    if any(
                        k in error_msg
                        for k in ["429", "Quota", "Rate limit", "RESOURCE_EXHAUSTED"]
                    ):
                        if attempt < retries - 1:
                            print(
                                f"[Gemini Chave {key_index + 1}] Cota atingida. Aguardando {current_delay}s (Tentativa {attempt + 1}/{retries})..."
                            )
                            time.sleep(current_delay)
                            current_delay *= 2
                            continue
                        else:
                            print(
                                f"[Gemini Chave {key_index + 1}] Esgotada. Mudando para a próxima chave..."
                            )
                            break
                    else:
                        print(f"[Gemini Error]: {error_msg}")
                        return {"text": f"Erro no processamento da IA: {error_msg}"}

        except Exception as key_err:
            print(f"[Gemini Key Error]: {key_err}")
            continue

    return {
        "text": "A IA está com um alto volume de requisições no momento. Por favor, tente enviar sua pergunta novamente em alguns segundos."
    }