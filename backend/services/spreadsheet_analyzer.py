import re
import unicodedata

import pandas as pd


# ==========================================================
# UTILITÁRIOS
# ==========================================================

def normalize_text(value):
    """
    Normaliza textos para facilitar a identificação de palavras,
    independentemente de acentos, maiúsculas ou minúsculas.
    """

    if value is None:
        return ""

    text = str(value).strip().lower()

    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )

    return text


def clean_dataframe(dataframe):
    """
    Remove linhas e colunas completamente vazias
    e substitui valores ausentes.
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


# ==========================================================
# DATAFRAME → TEXTO
# ==========================================================

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


# ==========================================================
# PALAVRAS-CHAVE
# ==========================================================

KEYWORDS = {

    "financeiro": [
        "financeiro",
        "financas",
        "receita",
        "receitas",
        "despesa",
        "despesas",
        "saldo",
        "fluxo de caixa",
        "conta a pagar",
        "contas a pagar",
        "conta a receber",
        "contas a receber",
        "fornecedor",
        "fornecedores",
        "custo",
        "custos",
        "valor pago",
        "valor recebido",
        "entrada",
        "entradas",
        "saida",
        "saidas",
        "faturamento",
        "lucro",
        "lucro liquido",
        "margem",
        "investimento",
        "orcamento",
        "desembolso",
        "capital",
        "despesa operacional",
        "dre"
    ],

    "marketing": [
        "marketing",
        "post",
        "posts",
        "instagram",
        "facebook",
        "tiktok",
        "linkedin",
        "stories",
        "story",
        "reels",
        "conteudo",
        "kpi",
        "copy",
        "publicacao",
        "publicacoes",
        "engajamento",
        "campanha",
        "campanhas",
        "alcance",
        "seguidores",
        "seguidor",
        "anuncio",
        "anuncios",
        "social media",
        "branding",
        "impressao",
        "impressoes",
        "clique",
        "cliques",
        "ctr",
        "cpc",
        "cpm",
        "roi",
        "roas",
        "midia",
        "audiencia"
    ],

    "vendas": [
        "venda",
        "vendas",
        "cliente",
        "clientes",
        "lead",
        "leads",
        "pipeline",
        "conversao",
        "conversoes",
        "ticket medio",
        "produto",
        "produtos",
        "servico",
        "servicos",
        "vendedor",
        "vendedores",
        "proposta",
        "propostas",
        "orcamento",
        "orcamentos",
        "negociacao",
        "negociacoes",
        "crm",
        "faturamento",
        "pedido",
        "pedidos",
        "contrato",
        "contratos",
        "fechamento",
        "fechamentos",
        "comissao",
        "comissoes",
        "pipeline comercial"
    ],

    "atendimento": [
        "atendimento",
        "cliente",
        "clientes",
        "suporte",
        "sac",
        "chamado",
        "chamados",
        "ticket",
        "tickets",
        "reclamacao",
        "reclamacoes",
        "duvida",
        "duvidas",
        "solicitacao",
        "solicitacoes",
        "satisfacao",
        "feedback",
        "tempo de resposta",
        "tempo medio de resposta",
        "sla",
        "nps",
        "csat",
        "experiencia do cliente",
        "experiencia",
        "resolucao",
        "problema",
        "problemas",
        "atendente",
        "atendentes",
        "fila",
        "tempo de espera"
    ],

    "estrategia": [
        "estrategia",
        "estrategico",
        "planejamento",
        "plano estrategico",
        "objetivo",
        "objetivos",
        "meta",
        "metas",
        "swot",
        "visao",
        "missao",
        "posicionamento",
        "crescimento",
        "indicadores",
        "kpi",
        "roadmap",
        "planejamento estrategico",
        "processos",
        "gestao",
        "gestao empresarial",
        "prioridade",
        "prioridades",
        "projeto",
        "projetos",
        "resultado",
        "resultados",
        "desempenho",
        "planejamento empresarial"
    ]
}


# ==========================================================
# PESOS ESPECÍFICOS
# ==========================================================

KEYWORD_WEIGHTS = {

    "financeiro": {
        "dre": 5,
        "fluxo de caixa": 5,
        "conta a pagar": 4,
        "contas a pagar": 4,
        "conta a receber": 4,
        "contas a receber": 4,
        "receita": 3,
        "despesa": 3,
        "lucro": 4,
        "margem": 3,
        "saldo": 3,
        "faturamento": 2
    },

    "marketing": {
        "instagram": 4,
        "social media": 5,
        "engajamento": 4,
        "alcance": 3,
        "seguidores": 3,
        "reels": 3,
        "stories": 3,
        "campanha": 4,
        "ctr": 5,
        "cpc": 4,
        "cpm": 4,
        "roas": 5,
        "conteudo": 3
    },

    "vendas": {
        "pipeline": 5,
        "pipeline comercial": 5,
        "lead": 3,
        "leads": 3,
        "conversao": 4,
        "ticket medio": 5,
        "vendedor": 4,
        "vendedores": 4,
        "proposta": 3,
        "fechamento": 4,
        "comissao": 3
    },

    "atendimento": {
        "sla": 5,
        "nps": 5,
        "csat": 5,
        "tempo de resposta": 5,
        "tempo medio de resposta": 5,
        "reclamacao": 4,
        "chamado": 4,
        "ticket": 3,
        "satisfacao": 4
    },

    "estrategia": {
        "swot": 5,
        "roadmap": 5,
        "plano estrategico": 5,
        "planejamento estrategico": 5,
        "objetivos": 3,
        "metas": 3,
        "visao": 3,
        "missao": 3,
        "posicionamento": 4
    }
}


# ==========================================================
# CLASSIFICAÇÃO
# ==========================================================

def detect_document_type(dataframe):
    """
    Identifica a área mais adequada da CLOUDIX AI
    para analisar a planilha.

    A classificação considera:
    - conteúdo;
    - palavras-chave;
    - frequência;
    - pesos;
    - estrutura das colunas.
    """

    dataframe = clean_dataframe(dataframe)

    text = dataframe_to_text(dataframe)

    normalized_text = normalize_text(text)

    scores = {
        "financeiro": 0,
        "marketing": 0,
        "vendas": 0,
        "atendimento": 0,
        "estrategia": 0
    }

    matched_keywords = {
        "financeiro": [],
        "marketing": [],
        "vendas": [],
        "atendimento": [],
        "estrategia": []
    }

    # ------------------------------------------------------
    # Análise das palavras-chave
    # ------------------------------------------------------

    for document_type, keywords in KEYWORDS.items():

        for keyword in keywords:

            normalized_keyword = normalize_text(keyword)

            if normalized_keyword in normalized_text:

                weight = KEYWORD_WEIGHTS.get(
                    document_type,
                    {}
                ).get(
                    keyword,
                    1
                )

                occurrences = normalized_text.count(
                    normalized_keyword
                )

                # Limita o peso da repetição para evitar
                # que uma palavra domine completamente a análise.
                occurrences = min(
                    occurrences,
                    5
                )

                scores[document_type] += (
                    weight * occurrences
                )

                matched_keywords[
                    document_type
                ].append(keyword)

    # ------------------------------------------------------
    # Análise dos nomes das colunas
    # ------------------------------------------------------

    column_text = " ".join(
        normalize_text(column)
        for column in dataframe.columns
    )

    # Caso o DataFrame tenha cabeçalho numérico,
    # analisamos também a primeira linha.
    if not dataframe.empty:

        first_row = " ".join(
            normalize_text(value)
            for value in dataframe.iloc[0].tolist()
        )

        column_text += " " + first_row

    for document_type, keywords in KEYWORDS.items():

        for keyword in keywords:

            normalized_keyword = normalize_text(keyword)

            if normalized_keyword in column_text:

                scores[document_type] += 2

    # ------------------------------------------------------
    # Resultado
    # ------------------------------------------------------

    detected_type = max(
        scores,
        key=scores.get
    )

    highest_score = scores[detected_type]

    total_score = sum(
        scores.values()
    )

    if highest_score == 0:

        detected_type = "geral"
        confidence = 0

    else:

        confidence = round(
            highest_score / max(total_score, 1),
            2
        )

    return {
        "type": detected_type,
        "scores": scores,
        "confidence": confidence,
        "matched_keywords": matched_keywords[
            detected_type
        ] if detected_type != "geral" else []
    }


# ==========================================================
# SEÇÕES
# ==========================================================

def extract_sections(dataframe):
    """
    Identifica possíveis títulos e blocos
    dentro da planilha.
    """

    dataframe = clean_dataframe(
        dataframe
    )

    sections = []

    for index, row in dataframe.iterrows():

        values = []

        for value in row.tolist():

            value = str(value).strip()

            if value:

                values.append(value)

        if not values:
            continue

        # Uma única célula preenchida normalmente
        # representa um título/seção.
        if len(values) == 1:

            title = values[0]

            sections.append({
                "row": index + 1,
                "title": title
            })

    return sections


# ==========================================================
# TIPOS DE DADOS
# ==========================================================

# ==========================================================
# MÉTRICAS
# ==========================================================

def calculate_metrics(dataframe):
    """
    Calcula métricas estatísticas básicas
    das colunas numéricas da planilha.
    """

    dataframe = clean_dataframe(dataframe)

    metrics = []
    trends = []
    extremes = []

    if dataframe.empty:
        return {
            "available": False,
            "statistics": {
                "numeric_columns": 0,
                "numeric_values": 0,
                "rows": 0,
                "columns": 0
            },
            "metrics": [],
            "trends": [],
            "extremes": []
        }

    numeric_columns = 0
    numeric_values = 0

    for column in dataframe.columns:

        series = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

        valid_values = series.dropna()

        if valid_values.empty:
            continue

        numeric_columns += 1
        numeric_values += len(valid_values)

        metrics.append({
            "column": str(column),
            "count": int(valid_values.count()),
            "sum": float(valid_values.sum()),
            "average": float(valid_values.mean()),
            "minimum": float(valid_values.min()),
            "maximum": float(valid_values.max()),
            "median": float(valid_values.median())
        })

        # --------------------------------------------------
        # TENDÊNCIA
        # --------------------------------------------------

        if len(valid_values) >= 2:

            first_value = float(valid_values.iloc[0])
            last_value = float(valid_values.iloc[-1])

            if first_value != 0:

                variation = (
                    (last_value - first_value)
                    / abs(first_value)
                ) * 100

                trends.append({
                    "column": str(column),
                    "first_value": first_value,
                    "last_value": last_value,
                    "variation_percent": round(
                        variation,
                        2
                    )
                })

        # --------------------------------------------------
        # EXTREMOS
        # --------------------------------------------------

        extremes.append({
            "column": str(column),
            "minimum": float(valid_values.min()),
            "maximum": float(valid_values.max())
        })

    return {
        "available": numeric_columns > 0,
        "statistics": {
            "numeric_columns": numeric_columns,
            "numeric_values": numeric_values,
            "rows": len(dataframe),
            "columns": len(dataframe.columns)
        },
        "metrics": metrics,
        "trends": trends,
        "extremes": extremes
    }

    # ==========================================================
# TIPOS DE DADOS
# ==========================================================

def detect_data_features(dataframe):
    """
    Identifica características gerais dos dados
    que poderão ser utilizadas posteriormente
    pelo motor de inteligência da CLOUDIX AI.
    """

    dataframe = clean_dataframe(dataframe)

    numeric_columns = []
    date_columns = []
    text_columns = []

    for column in dataframe.columns:

        series = dataframe[column]

        # Tentativa de conversão numérica
        numeric_series = pd.to_numeric(
            series,
            errors="coerce"
        )

        numeric_ratio = (
            numeric_series.notna().mean()
            if len(series) > 0
            else 0
        )

        # Tentativa de conversão de data
        date_series = pd.to_datetime(
            series,
            errors="coerce"
        )

        date_ratio = (
            date_series.notna().mean()
            if len(series) > 0
            else 0
        )

        if numeric_ratio >= 0.7:

            numeric_columns.append(
                str(column)
            )

        elif date_ratio >= 0.7:

            date_columns.append(
                str(column)
            )

        else:

            text_columns.append(
                str(column)
            )

    return {
        "numeric_columns": numeric_columns,
        "date_columns": date_columns,
        "text_columns": text_columns
    }

# ==========================================================
# PREVIEW
# ==========================================================

def generate_preview(dataframe, limit=20):
    """
    Gera uma prévia segura da planilha.
    """

    dataframe = clean_dataframe(
        dataframe
    )

    preview = dataframe.head(
        limit
    ).copy()

    # Converte valores para formatos JSON seguros.
    for column in preview.columns:

        preview[column] = preview[
            column
        ].apply(
            lambda value:
                value.item()
                if hasattr(value, "item")
                else value
        )

    return preview.to_dict(
        orient="records"
    )


# ==========================================================
# ANÁLISE PRINCIPAL
# ==========================================================

def analyze_spreadsheet(dataframe):
    """
    Função principal do analisador de planilhas.

    Executa:

    1. Limpeza dos dados
    2. Classificação da planilha
    3. Conversão para texto
    4. Identificação de seções
    5. Identificação dos tipos de dados
    6. Geração de preview
    """

    dataframe = clean_dataframe(
        dataframe
    )

    document_type = detect_document_type(
        dataframe
    )

    text = dataframe_to_text(
        dataframe
    )

    sections = extract_sections(
        dataframe
    )

    data_features = detect_data_features(
        dataframe
    )

    metrics = calculate_metrics(
    dataframe
)

    preview = generate_preview(
        dataframe
    )

    return {
    "document_type": document_type,

    "rows": len(dataframe),

    "columns": len(
        dataframe.columns
    ),

    "text": text,

    "sections": sections,

    "data_features": data_features,

    "metrics": metrics,

    "preview": preview
}