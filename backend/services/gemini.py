import os
import time
import google.generativeai as genai

# Aceita uma chave única ou múltiplas chaves separadas por vírgula no Render
RAW_KEYS = os.getenv("GEMINI_API_KEY", "")
API_KEYS = [k.strip() for k in RAW_KEYS.split(",") if k.strip()]

# Lista de modelos de reserva caso a consulta automática falhe
CANDIDATE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
    "gemini-pro",
]


def get_active_model(api_key: str):
    """
    Identifica dinamicamente um modelo ativo e disponível para a chave de API.
    """
    genai.configure(api_key=api_key)

    try:
        # Consulta a lista de modelos suportados pela API do Google
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                model_name = m.name.replace("models/", "")
                return genai.GenerativeModel(model_name)
    except Exception as e:
        print(f"[Gemini ListModels Warning]: {e}")

    # Se a lista falhar, tenta os nomes da lista de reserva
    for model_name in CANDIDATE_MODELS:
        try:
            return genai.GenerativeModel(model_name)
        except Exception:
            continue

    return genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(
    prompt: str,
    previous_interaction_id=None,
    retries: int = 3,
    delay: int = 5,
    **kwargs,
):
    """
    Envia solicitações para o Gemini com seleção dinâmica de modelo,
    suporte a rotação de chaves e re-tentativas automáticas em caso de limite (429).
    """
    if not API_KEYS:
        return {
            "text": "Nenhuma chave da API do Gemini foi configurada no servidor."
        }

    for key_index, api_key in enumerate(API_KEYS):
        try:
            model = get_active_model(api_key)
            current_delay = delay

            for attempt in range(retries):
                try:
                    response = model.generate_content(prompt)
                    return {"text": response.text}

                except Exception as e:
                    error_msg = str(e)

                    # Trata erro 404 (modelo indisponível) mudando de modelo/chave
                    if "404" in error_msg or "not found" in error_msg.lower():
                        print(
                            f"[Gemini Chave {key_index + 1}] Modelo não encontrado (404). A tentar com novo modelo..."
                        )
                        break

                    # Trata erro de limite de cota (429)
                    if any(
                        k in error_msg
                        for k in [
                            "429",
                            "Quota",
                            "Rate limit",
                            "RESOURCE_EXHAUSTED",
                        ]
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
                        return {
                            "text": f"Erro no processamento da IA: {error_msg}"
                        }

        except Exception as key_err:
            print(f"[Gemini Key Error]: {key_err}")
            continue

    return {
        "text": "A IA está com um alto volume de requisições no momento. Por favor, tente enviar sua pergunta novamente em alguns segundos."
    }