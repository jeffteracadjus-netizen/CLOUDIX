import math
import re

import pandas as pd


# ==========================================================
# UTILITÁRIOS
# ==========================================================

def is_number(value):
    """
    Verifica se um valor pode ser interpretado como número.
    """

    if value is None:
        return False

    if isinstance(value, bool):
        return False

    try:
        number = float(value)
        return math.isfinite(number)

    except (ValueError, TypeError):
        return False


def to_number(value):
    """
    Converte um valor para número quando possível.

    Suporta:
    - números normais
    - valores com R$, €, £
    - porcentagens
    - formato brasileiro
    - strings numéricas
    """

    if is_number(value):
        return float(value)

    if not isinstance(value, str):
        return None

    value = value.strip()

    if not value:
        return None

    # Remove espaços
    value = value.replace("\xa0", " ")

    # Remove símbolos comuns
    cleaned = re.sub(
        r"[R$€£%]",
        "",
        value
    )

    cleaned = cleaned.strip()

    if not cleaned:
        return None

    # Trata números negativos entre parênteses.
    # Exemplo: (1500,50) -> -1500.50
    negative = False

    if (
        cleaned.startswith("(")
        and cleaned.endswith(")")
    ):
        negative = True
        cleaned = cleaned[1:-1].strip()

    # Trata formatos brasileiros.
    #
    # 1.234,56 -> 1234.56
    # 1234,56  -> 1234.56
    #
    # Também preserva números americanos:
    # 1234.56 -> 1234.56
    if "," in cleaned and "." in cleaned:

        last_comma = cleaned.rfind(",")
        last_dot = cleaned.rfind(".")

        if last_comma > last_dot:
            # Formato brasileiro
            cleaned = cleaned.replace(".", "")
            cleaned = cleaned.replace(",", ".")

        else:
            # Formato internacional
            cleaned = cleaned.replace(",", "")

    elif "," in cleaned:

        # Quando existe apenas vírgula,
        # consideramos como separador decimal.
        cleaned = cleaned.replace(",", ".")

    # Remove espaços restantes
    cleaned = cleaned.replace(" ", "")

    try:

        number = float(cleaned)

        if not math.isfinite(number):
            return None

        if negative:
            number = -number

        return number

    except (ValueError, TypeError):
        return None


def round_number(value, decimals=2):
    """
    Arredonda números para apresentação.
    """

    if value is None:
        return None

    try:
        return round(
            float(value),
            decimals
        )

    except (ValueError, TypeError):
        return None


# ==========================================================
# LIMPEZA
# ==========================================================

def prepare_dataframe(dataframe):
    """
    Prepara o DataFrame para análise matemática.
    """

    if dataframe is None:
        return pd.DataFrame()

    dataframe = dataframe.copy()

    # Remove linhas completamente vazias
    dataframe = dataframe.dropna(
        axis=0,
        how="all"
    )

    # Remove colunas completamente vazias
    dataframe = dataframe.dropna(
        axis=1,
        how="all"
    )

    return dataframe


# ==========================================================
# CONVERSÃO DE COLUNA
# ==========================================================

def convert_column_to_numbers(dataframe, column):
    """
    Converte uma coluna inteira para números.
    Valores que não puderem ser convertidos viram NaN.
    """

    if column not in dataframe.columns:
        return pd.Series(
            dtype="float64"
        )

    return dataframe[column].apply(
        to_number
    )


# ==========================================================
# COLUNAS NUMÉRICAS
# ==========================================================

def detect_numeric_columns(dataframe):
    """
    Identifica colunas predominantemente numéricas.

    Mantém o identificador original da coluna.

    Uma coluna precisa ter pelo menos 30%
    de valores numéricos para ser considerada.
    """

    dataframe = prepare_dataframe(
        dataframe
    )

    numeric_columns = []

    if dataframe.empty:
        return numeric_columns

    for column in dataframe.columns:

        series = dataframe[column]

        converted = series.apply(
            to_number
        )

        valid_values = converted.notna().sum()

        total_values = len(series)

        if total_values == 0:
            continue

        ratio = (
            valid_values / total_values
        )

        if ratio >= 0.30:

            numeric_columns.append(
                column
            )

    return numeric_columns


# ==========================================================
# MÉTRICAS DE UMA COLUNA
# ==========================================================

def calculate_column_metrics(
    dataframe,
    column
):
    """
    Calcula estatísticas básicas de uma coluna.
    """

    if column not in dataframe.columns:
        return None

    series = convert_column_to_numbers(
        dataframe,
        column
    )

    series = series.dropna()

    if series.empty:
        return None

    values = series.tolist()

    total = sum(values)

    average = (
        total / len(values)
    )

    minimum = min(values)

    maximum = max(values)

    return {
        "column": str(column),
        "count": len(values),
        "sum": round_number(
            total
        ),
        "average": round_number(
            average
        ),
        "minimum": round_number(
            minimum
        ),
        "maximum": round_number(
            maximum
        )
    }


# ==========================================================
# CRESCIMENTO
# ==========================================================

def calculate_growth(values):
    """
    Calcula crescimento entre o primeiro
    e o último valor.
    """

    if values is None:
        return None

    if len(values) < 2:
        return None

    first = values[0]

    last = values[-1]

    if first == 0:
        return None

    growth = (
        (last - first)
        / abs(first)
    ) * 100

    return round_number(
        growth
    )


# ==========================================================
# TENDÊNCIA
# ==========================================================

def detect_trend(values):
    """
    Identifica uma tendência simples:

    - crescente
    - decrescente
    - estavel
    - insuficiente
    """

    if values is None:
        return "insuficiente"

    if len(values) < 2:
        return "insuficiente"

    first = values[0]

    last = values[-1]

    if first == 0:

        if last > 0:
            return "crescente"

        if last < 0:
            return "decrescente"

        return "estavel"

    difference = (
        (last - first)
        / abs(first)
    ) * 100

    if difference > 5:
        return "crescente"

    if difference < -5:
        return "decrescente"

    return "estavel"


# ==========================================================
# VERIFICAÇÃO DE SÉRIE TEMPORAL
# ==========================================================

def is_time_series_dataframe(dataframe):
    """
    Verifica se o DataFrame aparenta representar
    uma série temporal.

    Isso é importante porque uma planilha como:

        Receita
        Lucro
        EBITDA
        Margem
        Headcount

    NÃO deve ser tratada como uma sequência temporal.

    A tendência só deve ser calculada quando houver
    evidência de que as linhas representam períodos.
    """

    if dataframe is None:
        return False

    dataframe = prepare_dataframe(
        dataframe
    )

    if dataframe.empty:
        return False

    # Procura colunas com datas.
    for column in dataframe.columns:

        series = dataframe[column]

        if pd.api.types.is_datetime64_any_dtype(
            series
        ):
            return True

        # Tenta converter textos para datas.
        converted = pd.to_datetime(
            series,
            errors="coerce"
        )

        valid = converted.notna().sum()

        if len(series) == 0:
            continue

        ratio = valid / len(series)

        if ratio >= 0.70:
            return True

    # Verifica nomes comuns de período.
    period_keywords = [
        "data",
        "date",
        "mes",
        "mês",
        "month",
        "ano",
        "year",
        "periodo",
        "período",
        "period",
        "semana",
        "week",
        "trimestre",
        "quarter"
    ]

    for column in dataframe.columns:

        column_name = str(
            column
        ).lower()

        for keyword in period_keywords:

            if keyword in column_name:
                return True

    return False


# ==========================================================
# ANÁLISE DE TENDÊNCIAS
# ==========================================================

def analyze_trends(
    dataframe,
    numeric_columns
):
    """
    Analisa tendências das colunas numéricas.

    IMPORTANTE:

    Tendências somente são calculadas quando
    a planilha aparenta ser uma série temporal.

    Isso evita resultados incorretos em relatórios
    executivos que misturam métricas diferentes.
    """

    trends = []

    dataframe = prepare_dataframe(
        dataframe
    )

    if dataframe.empty:
        return trends

    if not is_time_series_dataframe(
        dataframe
    ):
        return trends

    for column in numeric_columns:

        if column not in dataframe.columns:
            continue

        series = convert_column_to_numbers(
            dataframe,
            column
        )

        series = series.dropna()

        if len(series) < 2:
            continue

        values = series.tolist()

        growth = calculate_growth(
            values
        )

        trend = detect_trend(
            values
        )

        trends.append({
            "column": str(column),
            "trend": trend,
            "growth_percent": growth
        })

    return trends


# ==========================================================
# INDICADORES IMPORTANTES
# ==========================================================

def identify_key_metrics(
    dataframe,
    numeric_columns
):
    """
    Identifica métricas potencialmente relevantes
    para a análise empresarial.
    """

    metrics = []

    for column in numeric_columns:

        result = calculate_column_metrics(
            dataframe,
            column
        )

        if result:

            metrics.append(
                result
            )

    return metrics


# ==========================================================
# VALORES EXTREMOS
# ==========================================================

def identify_extremes(
    dataframe,
    numeric_columns
):
    """
    Identifica maiores e menores valores.
    """

    extremes = []

    for column in numeric_columns:

        if column not in dataframe.columns:
            continue

        series = convert_column_to_numbers(
            dataframe,
            column
        )

        series = series.dropna()

        if series.empty:
            continue

        maximum = series.max()

        minimum = series.min()

        extremes.append({
            "column": str(column),
            "maximum": round_number(
                maximum
            ),
            "minimum": round_number(
                minimum
            )
        })

    return extremes


# ==========================================================
# RESUMO ESTATÍSTICO
# ==========================================================

def generate_statistics(
    dataframe,
    numeric_columns
):
    """
    Gera resumo estatístico geral.
    """

    total_numeric_values = 0

    for column in numeric_columns:

        if column not in dataframe.columns:
            continue

        series = convert_column_to_numbers(
            dataframe,
            column
        )

        total_numeric_values += (
            series.notna().sum()
        )

    return {
        "numeric_columns": len(
            numeric_columns
        ),
        "numeric_values": int(
            total_numeric_values
        ),
        "rows": len(
            dataframe
        ),
        "columns": len(
            dataframe.columns
        )
    }


# ==========================================================
# CLASSIFICAÇÃO BÁSICA DE MÉTRICAS
# ==========================================================

def classify_metric_column(column_name):
    """
    Classifica uma coluna pelo nome.

    Essa informação poderá ser usada futuramente
    pelo intelligence.py.
    """

    name = str(
        column_name
    ).lower()

    if any(
        keyword in name
        for keyword in [
            "receita",
            "revenue",
            "faturamento",
            "vendas",
            "sales",
            "mrr",
            "arr"
        ]
    ):
        return "receita"

    if any(
        keyword in name
        for keyword in [
            "despesa",
            "despesas",
            "expense",
            "custo",
            "custos",
            "cost"
        ]
    ):
        return "despesa"

    if any(
        keyword in name
        for keyword in [
            "lucro",
            "profit",
            "resultado"
        ]
    ):
        return "lucro"

    if any(
        keyword in name
        for keyword in [
            "margem",
            "margin"
        ]
    ):
        return "margem"

    if any(
        keyword in name
        for keyword in [
            "ebitda"
        ]
    ):
        return "ebitda"

    if any(
        keyword in name
        for keyword in [
            "headcount",
            "funcionarios",
            "funcionários",
            "employees"
        ]
    ):
        return "pessoas"

    if any(
        keyword in name
        for keyword in [
            "ltv",
            "cac"
        ]
    ):
        return "unit_economics"

    return "outro"


# ==========================================================
# MÉTRICAS CLASSIFICADAS
# ==========================================================

def generate_classified_metrics(
    dataframe,
    numeric_columns
):
    """
    Gera métricas com uma classificação semântica básica.

    Exemplo:

    Receita Bruta Total -> receita
    Lucro Líquido -> lucro
    Margem EBITDA -> margem
    Headcount -> pessoas
    """

    classified = []

    for column in numeric_columns:

        result = calculate_column_metrics(
            dataframe,
            column
        )

        if not result:
            continue

        result["category"] = (
            classify_metric_column(
                column
            )
        )

        classified.append(
            result
        )

    return classified


# ==========================================================
# MOTOR PRINCIPAL
# ==========================================================

def calculate_metrics(dataframe):
    """
    Motor principal de métricas da CLOUDIX AI.

    Analisa os dados da planilha e produz
    informações matemáticas que poderão ser
    interpretadas posteriormente pelo motor
    de inteligência.
    """

    dataframe = prepare_dataframe(
        dataframe
    )

    # ------------------------------------------------------
    # DATAFRAME VAZIO
    # ------------------------------------------------------

    if dataframe.empty:

        return {
            "available": False,

            "message": (
                "A planilha não possui dados "
                "suficientes para análise."
            ),

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

    # ------------------------------------------------------
    # COLUNAS NUMÉRICAS
    # ------------------------------------------------------

    numeric_columns = (
        detect_numeric_columns(
            dataframe
        )
    )

    # ------------------------------------------------------
    # ESTATÍSTICAS
    # ------------------------------------------------------

    statistics = generate_statistics(
        dataframe,
        numeric_columns
    )

    # ------------------------------------------------------
    # MÉTRICAS
    # ------------------------------------------------------

    metrics = identify_key_metrics(
        dataframe,
        numeric_columns
    )

    # ------------------------------------------------------
    # TENDÊNCIAS
    # ------------------------------------------------------

    trends = analyze_trends(
        dataframe,
        numeric_columns
    )

    # ------------------------------------------------------
    # EXTREMOS
    # ------------------------------------------------------

    extremes = identify_extremes(
        dataframe,
        numeric_columns
    )

    # ------------------------------------------------------
    # RETORNO
    # ------------------------------------------------------

    return {
        "available": True,

        "statistics": statistics,

        "metrics": metrics,

        "trends": trends,

        "extremes": extremes
    }