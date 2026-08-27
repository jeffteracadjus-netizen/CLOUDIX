import pandas as pd


def clean_dataframe(dataframe):
    """
    Remove linhas e colunas completamente vazias.
    """
    dataframe = dataframe.copy()

    dataframe = dataframe.dropna(
        axis=0,
        how="all"
    )

    dataframe = dataframe.dropna(
        axis=1,
        how="all"
    )

    dataframe = dataframe.fillna("")

    return dataframe


def dataframe_to_text(dataframe):
    """
    Converte a planilha em texto estruturado
    para análise da CLOUDIX AI.
    """
    dataframe = clean_dataframe(dataframe)

    if dataframe.empty:
        return ""

    lines = []

    for index, row in dataframe.iterrows():

        values = []

        for value in row.tolist():

            value = str(value).strip()

            if value:
                values.append(value)

        if values:
            lines.append(
                f"Linha {index + 1}: "
                + " | ".join(values)
            )

    return "\n".join(lines)


def detect_document_type(dataframe):
    """
    Identifica qual funcionalidade da CLOUDIX AI
    é mais adequada para analisar a planilha.

    Funcionalidades:

    - vendas
    - marketing
    - financeiro
    - atendimento
    - estrategia
    """

    text = dataframe_to_text(dataframe).lower()

    keywords = {

        "financeiro": [
            "receita",
            "despesa",
            "saldo",
            "fluxo de caixa",
            "conta a pagar",
            "conta a receber",
            "fornecedor",
            "custo",
            "valor pago",
            "valor recebido",
            "entrada",
            "saída",
            "saida",
            "financeiro",
            "faturamento",
            "lucro",
            "margem",
            "investimento",
            "orçamento",
            "orcamento"
        ],

        "marketing": [
            "post",
            "posts",
            "instagram",
            "facebook",
            "stories",
            "reels",
            "marketing",
            "conteúdo",
            "conteudo",
            "kpi",
            "copy",
            "publicação",
            "publicacao",
            "engajamento",
            "campanha",
            "alcance",
            "seguidores",
            "anúncio",
            "anuncio",
            "social media",
            "branding"
        ],

        "vendas": [
            "vendas",
            "venda",
            "cliente",
            "lead",
            "pipeline",
            "conversão",
            "conversao",
            "ticket médio",
            "ticket medio",
            "produto",
            "serviço",
            "servico",
            "vendedor",
            "proposta",
            "orçamento",
            "orcamento",
            "negociação",
            "negociacao",
            "crm",
            "faturamento"
        ],

        "atendimento": [
            "atendimento",
            "cliente",
            "suporte",
            "sac",
            "chamado",
            "ticket",
            "reclamação",
            "reclamacao",
            "dúvida",
            "duvida",
            "solicitação",
            "solicitacao",
            "satisfação",
            "satisfacao",
            "feedback",
            "tempo de resposta",
            "sla",
            "nps",
            "csat",
            "experiência do cliente",
            "experiencia do cliente"
        ],

        "estrategia": [
            "estratégia",
            "estrategia",
            "planejamento",
            "plano estratégico",
            "plano estrategico",
            "objetivo",
            "metas",
            "meta",
            "swot",
            "visão",
            "visao",
            "missão",
            "missao",
            "posicionamento",
            "crescimento",
            "indicadores",
            "kpi",
            "roadmap",
            "planejamento estratégico",
            "planejamento estrategico",
            "processos",
            "gestão",
            "gestao"
        ]
    }

    scores = {
        "financeiro": 0,
        "marketing": 0,
        "vendas": 0,
        "atendimento": 0,
        "estrategia": 0
    }

    for document_type, type_keywords in keywords.items():

        for keyword in type_keywords:

            if keyword in text:
                scores[document_type] += 1

    detected_type = max(
        scores,
        key=scores.get
    )

    if scores[detected_type] == 0:
        detected_type = "geral"

    return {
        "type": detected_type,
        "scores": scores
    }


def extract_sections(dataframe):
    """
    Identifica possíveis títulos e blocos
    dentro da planilha.
    """

    dataframe = clean_dataframe(dataframe)

    sections = []

    for index, row in dataframe.iterrows():

        values = []

        for value in row.tolist():

            value = str(value).strip()

            if value:
                values.append(value)

        if not values:
            continue

        if len(values) == 1:

            sections.append({
                "row": index + 1,
                "title": values[0]
            })

    return sections


def analyze_spreadsheet(dataframe):
    """
    Função principal do analisador de planilhas.

    Executa:

    1. Limpeza dos dados
    2. Classificação da planilha
    3. Conversão para texto
    4. Identificação de seções
    5. Geração de preview
    """

    dataframe = clean_dataframe(dataframe)

    document_type = detect_document_type(
        dataframe
    )

    text = dataframe_to_text(
        dataframe
    )

    sections = extract_sections(
        dataframe
    )

    return {
        "document_type": document_type,

        "rows": len(dataframe),

        "columns": len(dataframe.columns),

        "text": text,

        "sections": sections,

        "preview": dataframe.head(
            20
        ).to_dict(
            orient="records"
        )
    }