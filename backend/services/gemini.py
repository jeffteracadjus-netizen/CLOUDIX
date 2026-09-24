import os

from dotenv import load_dotenv
from google import genai


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY não foi configurada no arquivo .env"
    )


# ==========================================================
# CLIENTE GEMINI
# ==========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

MODEL = "gemini-3.6-flash"


# ==========================================================
# CLOUDIX AI
# ==========================================================

def ask_gemini(
    message: str,
    system_instruction: str | None = None,
    previous_interaction_id: str | None = None
):

    try:

        interaction_data = {
            "model": MODEL,
            "input": message
        }

        if system_instruction:

            interaction_data["system_instruction"] = (
                system_instruction
            )

        if previous_interaction_id:

            interaction_data[
                "previous_interaction_id"
            ] = previous_interaction_id

        interaction = client.interactions.create(
            **interaction_data
        )

        return {
            "text": interaction.output_text,
            "interaction_id": interaction.id
        }

    except Exception as error:

        raise RuntimeError(
            f"Erro ao consultar o Gemini: {str(error)}"
        ) from error