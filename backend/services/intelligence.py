import re


def _extract_number(text, label):
    """
    Procura um número associado a uma determinada métrica
    dentro do texto extraído da planilha.
    """

    if not text:
        return None

    pattern = (
        re.escape(label)
        + r".*?\|\s*([-+]?\d+(?:[.,]\d+)?)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if not match:
        return None

    value = match.group(1)

    try:
        return float(
            value.replace(",", ".")
        )
    except (ValueError, TypeError):
        return None


def _format_money(value):
    """
    Formata valores monetários para apresentação.
    """

    if value is None:
        return "não identificado"

    sign = "-" if value < 0 else ""
    value = abs(value)

    return (
        f"{sign}US$ "
        f"{value:,.2f}"
    )


def _format_percent(value):
    """
    Converte uma proporção em percentual.
    """

    if value is None:
        return "não identificado"

    # Valores como 0.62 representam 62%.
    if abs(value) <= 1:
        value = value * 100

    return f"{value:.2f}%"


def _format_multiple(value):
    """
    Formata múltiplos financeiros.
    """

    if value is None:
        return "não identificado"

    return f"{value:.2f}x"


def _extract_financial_metrics(text):
    """
    Extrai métricas financeiras importantes diretamente
    do texto produzido pelo analisador da planilha.
    """

    metrics = {
        "revenue": _extract_number(
            text,
            "Receita Bruta Total (2026)"
        ),

        "gross_profit": _extract_number(
            text,
            "Lucro Bruto Total"
        ),

        "gross_margin": _extract_number(
            text,
            "Margem Bruta Média"
        ),

        "operating_expenses": _extract_number(
            text,
            "Total Despesas Operacionais"
        ),

        "ebitda": _extract_number(
            text,
            "EBITDA Total (2026)"
        ),

        "ebitda_margin": _extract_number(
            text,
            "Margem EBITDA Média"
        ),

        "net_profit": _extract_number(
            text,
            "Lucro Líquido Total"
        ),

        "net_margin": _extract_number(
            text,
            "Margem Líquida Média"
        ),

        "mrr": _extract_number(
            text,
            "MRR Dezembro/2026"
        ),

        "arr": _extract_number(
            text,
            "ARR (saída do ano)"
        ),

        "headcount": _extract_number(
            text,
            "Headcount final"
        ),

        "ltv_cac": _extract_number(
            text,
            "LTV/CAC (Dez/2026)"
        ),

        "subscriptions": _extract_number(
            text,
            "Assinaturas"
        ),

        "ads": _extract_number(
            text,
            "Ads"
        ),

        "api": _extract_number(
            text,
            "API/Créditos IA"
        ),

        "subscriptions_share": _extract_number(
            text,
            "Assinaturas"
        ),

        "ads_share": _extract_number(
            text,
            "Ads"
        ),

        "api_share": _extract_number(
            text,
            "API/Créditos IA"
        )
    }

    return metrics


def _build_financial_analysis(
    result,
    text
):
    """
    Constrói uma análise financeira baseada nos
    indicadores efetivamente encontrados na planilha.
    """

    metrics = _extract_financial_metrics(
        text
    )

    revenue = metrics["revenue"]
    gross_profit = metrics["gross_profit"]
    gross_margin = metrics["gross_margin"]
    operating_expenses = metrics["operating_expenses"]
    ebitda = metrics["ebitda"]
    ebitda_margin = metrics["ebitda_margin"]
    net_profit = metrics["net_profit"]
    net_margin = metrics["net_margin"]
    mrr = metrics["mrr"]
    arr = metrics["arr"]
    headcount = metrics["headcount"]
    ltv_cac = metrics["ltv_cac"]
    subscriptions = metrics["subscriptions"]
    ads = metrics["ads"]
    api = metrics["api"]

    # ==========================================================
    # RESUMO
    # ==========================================================

    result["summary"] = (
        "A CLOUDIX AI identificou um documento financeiro "
        "com indicadores de receita, rentabilidade, despesas, "
        "recorrência e composição das receitas. "
        "A análise foi construída a partir dos valores "
        "encontrados no documento."
    )

    # ==========================================================
    # EVIDÊNCIAS
    # ==========================================================

    evidences = []

    if revenue is not None:
        evidences.append(
            "A receita bruta total de 2026 foi de "
            f"{_format_money(revenue)}."
        )

    if gross_profit is not None:
        evidences.append(
            "O lucro bruto total identificado foi de "
            f"{_format_money(gross_profit)}."
        )

    if gross_margin is not None:
        evidences.append(
            "A margem bruta média identificada foi de "
            f"{_format_percent(gross_margin)}."
        )

    if operating_expenses is not None:
        evidences.append(
            "As despesas operacionais totalizaram "
            f"{_format_money(operating_expenses)}."
        )

    if ebitda is not None:
        evidences.append(
            "O EBITDA total identificado foi de "
            f"{_format_money(ebitda)}."
        )

    if ebitda_margin is not None:
        evidences.append(
            "A margem EBITDA média foi de "
            f"{_format_percent(ebitda_margin)}."
        )

    if net_profit is not None:
        evidences.append(
            "O resultado líquido identificado foi de "
            f"{_format_money(net_profit)}."
        )

    if net_margin is not None:
        evidences.append(
            "A margem líquida média identificada foi de "
            f"{_format_percent(net_margin)}."
        )

    if mrr is not None:
        evidences.append(
            "O MRR de dezembro de 2026 foi de "
            f"{_format_money(mrr)}."
        )

    if arr is not None:
        evidences.append(
            "O ARR na saída de 2026 foi de "
            f"{_format_money(arr)}."
        )

    if ltv_cac is not None:
        evidences.append(
            "O indicador LTV/CAC identificado foi de "
            f"{_format_multiple(ltv_cac)}."
        )

    if headcount is not None:
        evidences.append(
            "O headcount final identificado foi de "
            f"{int(headcount)} colaboradores."
        )

    if subscriptions is not None:
        evidences.append(
            "A receita de assinaturas em dezembro foi de "
            f"{_format_money(subscriptions)}."
        )

    if ads is not None:
        evidences.append(
            "A receita de Ads em dezembro foi de "
            f"{_format_money(ads)}."
        )

    if api is not None:
        evidences.append(
            "A receita de API/Créditos IA em dezembro foi de "
            f"{_format_money(api)}."
        )

    result["evidences"] = evidences

    # ==========================================================
    # PONTOS FORTES
    # ==========================================================

    strengths = []

    if gross_margin is not None:
        if gross_margin >= 0.50:
            strengths.append(
                "A empresa apresenta uma margem bruta elevada, "
                "indicando boa capacidade de geração de resultado "
                "após os custos diretamente relacionados à receita."
            )
        elif gross_margin >= 0.30:
            strengths.append(
                "A margem bruta apresenta nível relevante, "
                "demonstrando capacidade de absorção dos custos "
                "diretos da operação."
            )

    if mrr is not None and mrr > 0:
        strengths.append(
            "Existe uma base relevante de receita recorrente, "
            "representada pelo MRR."
        )

    if arr is not None and arr > 0:
        strengths.append(
            "O negócio apresenta uma base anualizada de receita "
            "recorrente representada pelo ARR."
        )

    if ltv_cac is not None:
        if ltv_cac >= 3:
            strengths.append(
                "O LTV/CAC identificado é elevado, indicando uma "
                "relação favorável entre valor do cliente e custo "
                "de aquisição."
            )
        elif ltv_cac > 1:
            strengths.append(
                "O LTV/CAC está acima de 1x, indicando que o valor "
                "estimado do cliente supera o custo de aquisição."
            )

    if subscriptions is not None:
        strengths.append(
            "Assinaturas representam uma fonte relevante de "
            "monetização e contribuem para a recorrência do negócio."
        )

    if not strengths:
        strengths.append(
            "Foram identificados indicadores financeiros suficientes "
            "para iniciar uma avaliação estruturada da operação."
        )

    result["strengths"] = strengths

    # ==========================================================
    # LACUNAS / RISCOS
    # ==========================================================

    gaps = []

    if net_profit is not None and net_profit < 0:
        gaps.append(
            "O lucro líquido está negativo, indicando que a operação "
            "termina o período com prejuízo após os demais impactos "
            "financeiros."
        )

    if net_margin is not None and net_margin < 0:
        gaps.append(
            "A margem líquida negativa demonstra que a receita atual "
            "não está sendo suficiente para gerar rentabilidade líquida."
        )

    if ebitda_margin is not None and ebitda_margin < 0.05:
        gaps.append(
            "A margem EBITDA é baixa em relação à receita, indicando "
            "que uma parcela significativa da receita é consumida "
            "pelas despesas operacionais."
        )

    if operating_expenses is not None and revenue is not None:
        if revenue > 0:
            expense_ratio = (
                operating_expenses / revenue
            )

            if expense_ratio > 0.50:
                gaps.append(
                    "As despesas operacionais representam uma parcela "
                    f"elevada da receita, aproximadamente "
                    f"{expense_ratio * 100:.2f}%."
                )

    if revenue is not None and arr is not None:
        if revenue > 0:
            recurring_ratio = arr / revenue

            if recurring_ratio < 0.80:
                gaps.append(
                    "A receita anual total é superior ao ARR, indicando "
                    "que parte relevante da receita pode estar vindo "
                    "de componentes não recorrentes."
                )

    if not gaps:
        gaps.append(
            "Não foram identificados riscos financeiros críticos "
            "a partir dos indicadores disponíveis."
        )

    result["gaps"] = gaps

    # ==========================================================
    # OPORTUNIDADES
    # ==========================================================

    opportunities = []

    if net_profit is not None and net_profit < 0:
        opportunities.append(
            "Priorizar a recuperação da margem líquida através da "
            "redução de despesas, aumento de receita ou combinação "
            "das duas estratégias."
        )

    if ebitda_margin is not None and ebitda_margin < 0.05:
        opportunities.append(
            "Revisar as principais despesas operacionais para "
            "identificar custos que podem ser reduzidos sem "
            "prejudicar o crescimento."
        )

    if subscriptions is not None and mrr is not None:
        opportunities.append(
            "Aumentar a participação de receitas recorrentes por "
            "meio da expansão da base de assinaturas."
        )

    if ads is not None:
        opportunities.append(
            "Avaliar o potencial de expansão da monetização por Ads "
            "sem comprometer a experiência dos usuários."
        )

    if api is not None:
        opportunities.append(
            "Explorar o crescimento da receita de API/Créditos IA "
            "como uma segunda fonte de monetização escalável."
        )

    if ltv_cac is not None and ltv_cac >= 3:
        opportunities.append(
            "A relação LTV/CAC favorável pode permitir aumentar "
            "investimentos comerciais e de aquisição, desde que "
            "a rentabilidade por cliente seja preservada."
        )

    opportunities.append(
        "Criar acompanhamento mensal de receita, despesas, "
        "EBITDA e lucro líquido para identificar rapidamente "
        "mudanças na rentabilidade."
    )

    result["opportunities"] = opportunities

    # ==========================================================
    # KPIs
    # ==========================================================

    result["kpis"] = [
        "Receita Bruta",
        "Receita Recorrente Mensal (MRR)",
        "Receita Recorrente Anualizada (ARR)",
        "Lucro Bruto",
        "Margem Bruta",
        "Despesas Operacionais",
        "EBITDA",
        "Margem EBITDA",
        "Lucro Líquido",
        "Margem Líquida",
        "LTV/CAC",
        "Receita por cliente",
        "Custo de aquisição de cliente (CAC)",
        "Churn",
        "Crescimento da receita",
        "Participação da receita recorrente"
    ]

    # ==========================================================
    # INSIGHTS
    # ==========================================================

    insights = []

    if revenue is not None:
        insights.append(
            f"A empresa apresentou receita bruta anual de "
            f"{_format_money(revenue)}."
        )

    if gross_margin is not None and gross_margin >= 0.50:
        insights.append(
            f"A margem bruta de {_format_percent(gross_margin)} "
            "indica uma estrutura com forte geração de margem "
            "antes das despesas operacionais."
        )

    if ebitda is not None and ebitda_margin is not None:
        insights.append(
            f"O EBITDA de {_format_money(ebitda)} e a margem EBITDA "
            f"de {_format_percent(ebitda_margin)} mostram que a "
            "rentabilidade operacional ainda é relativamente baixa "
            "em comparação com o volume de receita."
        )

    if net_profit is not None and net_profit < 0:
        insights.append(
            f"O principal ponto de atenção é o resultado líquido "
            f"negativo de {_format_money(net_profit)}, indicando "
            "que o crescimento da receita ainda não está se "
            "convertendo em lucro líquido."
        )

    if mrr is not None and arr is not None:
        insights.append(
            f"O negócio encerrou o período com MRR de "
            f"{_format_money(mrr)} e ARR de "
            f"{_format_money(arr)}, demonstrando uma base "
            "significativa de receita recorrente."
        )

    if ltv_cac is not None:
        insights.append(
            f"O LTV/CAC de {_format_multiple(ltv_cac)} indica uma "
            "relação positiva entre valor potencial do cliente "
            "e custo de aquisição."
        )

    # Composição da receita
    composition = []

    if subscriptions is not None:
        composition.append(
            ("Assinaturas", subscriptions)
        )

    if ads is not None:
        composition.append(
            ("Ads", ads)
        )

    if api is not None:
        composition.append(
            ("API/Créditos IA", api)
        )

    if composition:
        composition.sort(
            key=lambda item: item[1],
            reverse=True
        )

        leader = composition[0]

        total_composition = sum(
            value
            for _, value in composition
        )

        if total_composition > 0:
            leader_share = (
                leader[1]
                / total_composition
                * 100
            )

            insights.append(
                f"A principal fonte de receita identificada em "
                f"dezembro é {leader[0]}, representando aproximadamente "
                f"{leader_share:.2f}% da composição identificada."
            )

    if not insights:
        insights.append(
            "Os dados financeiros disponíveis permitem uma análise "
            "inicial, mas ainda são necessários indicadores adicionais "
            "para uma avaliação mais profunda."
        )

    result["insights"] = insights

    # ==========================================================
    # RECOMENDAÇÕES
    # ==========================================================

    recommendations = []

    if net_profit is not None and net_profit < 0:
        recommendations.append(
            "Criar um plano específico para transformar o resultado "
            "líquido negativo em resultado positivo."
        )

    if operating_expenses is not None:
        recommendations.append(
            "Detalhar as despesas operacionais por categoria e "
            "identificar os grupos responsáveis pela maior parcela "
            "dos gastos."
        )

    if ebitda_margin is not None and ebitda_margin < 0.05:
        recommendations.append(
            "Estabelecer uma meta progressiva de aumento da margem EBITDA."
        )

    recommendations.extend([
        "Acompanhar mensalmente receita, EBITDA e lucro líquido.",
        "Separar receitas recorrentes e não recorrentes.",
        "Monitorar a evolução do MRR e ARR.",
        "Acompanhar LTV/CAC juntamente com CAC e churn.",
        "Avaliar a rentabilidade individual de cada fonte de receita.",
        "Criar um painel financeiro para acompanhamento contínuo.",
        "Comparar os resultados reais com as metas e projeções."
    ])

    result["recommendations"] = recommendations

    # ==========================================================
    # PLANO DE AÇÃO
    # ==========================================================

    result["action_plan"] = [
        {
            "step": 1,
            "action": "Mapear receitas e despesas",
            "objective": (
                "Separar todas as fontes de receita, custos e "
                "despesas operacionais."
            )
        },
        {
            "step": 2,
            "action": "Diagnosticar a rentabilidade",
            "objective": (
                "Identificar os fatores responsáveis pela diferença "
                "entre a receita e o lucro líquido."
            )
        },
        {
            "step": 3,
            "action": "Reduzir custos prioritários",
            "objective": (
                "Atacar as categorias de despesas com maior impacto "
                "sobre o resultado."
            )
        },
        {
            "step": 4,
            "action": "Aumentar receita recorrente",
            "objective": (
                "Expandir MRR e ARR através do crescimento das "
                "assinaturas e retenção dos clientes."
            )
        },
        {
            "step": 5,
            "action": "Monitorar indicadores",
            "objective": (
                "Acompanhar receita, margem bruta, EBITDA, margem "
                "líquida, MRR, ARR e LTV/CAC."
            )
        },
        {
            "step": 6,
            "action": "Revisar estratégia mensalmente",
            "objective": (
                "Tomar decisões com base na evolução dos indicadores "
                "financeiros."
            )
        }
    ]

    # ==========================================================
    # MÉTRICAS EXTRAÍDAS
    # ==========================================================

    result["financial_metrics"] = {
        "revenue": revenue,
        "gross_profit": gross_profit,
        "gross_margin": gross_margin,
        "operating_expenses": operating_expenses,
        "ebitda": ebitda,
        "ebitda_margin": ebitda_margin,
        "net_profit": net_profit,
        "net_margin": net_margin,
        "mrr": mrr,
        "arr": arr,
        "headcount": headcount,
        "ltv_cac": ltv_cac,
        "revenue_composition": {
            "subscriptions": subscriptions,
            "ads": ads,
            "api_credits": api
        }
    }


def generate_intelligence(analysis):
    """
    Motor de inteligência da CLOUDIX AI.

    Recebe o resultado do analisador de planilhas
    e gera uma interpretação especializada.
    """

    document_type = analysis["document_type"]["type"]

    text = analysis.get(
        "text",
        ""
    )

    sections = analysis.get(
        "sections",
        []
    )

    rows = analysis.get(
        "rows",
        0
    )

    columns = analysis.get(
        "columns",
        0
    )

    matched_keywords = analysis.get(
        "document_type",
        {}
    ).get(
        "matched_keywords",
        []
    )

    scores = analysis.get(
        "document_type",
        {}
    ).get(
        "scores",
        {}
    )

    confidence = analysis.get(
        "document_type",
        {}
    ).get(
        "confidence",
        0
    )

    result = {
        "document_type": document_type,
        "summary": "",
        "evidences": [],
        "strengths": [],
        "gaps": [],
        "opportunities": [],
        "kpis": [],
        "insights": [],
        "recommendations": [],
        "action_plan": [],
        "metadata": {
            "rows": rows,
            "columns": columns,
            "sections_found": len(
                sections
            ),
            "confidence": confidence,
            "scores": scores,
            "matched_keywords": matched_keywords
        }
    }

    # ==========================================================
    # MARKETING
    # ==========================================================

    if document_type == "marketing":

        result["summary"] = (
            "A CLOUDIX AI identificou uma estrutura de "
            "planejamento de marketing e crescimento, com "
            "elementos relacionados a conteúdo, redes sociais, "
            "engajamento, conversão e geração de leads."
        )

        result["evidences"] = [
            f"Foram identificadas {rows} linhas e {columns} colunas "
            "na estrutura analisada.",

            "Foram encontradas palavras-chave relacionadas "
            "a marketing e comunicação.",

            "O documento apresenta elementos relacionados "
            "a conteúdo, redes sociais e publicação.",

            "Foram identificados indicadores e conceitos "
            "relacionados à medição de desempenho.",

            "Existem elementos relacionados à geração "
            "de leads e conversão."
        ]

        result["strengths"] = [
            "O planejamento apresenta pilares estratégicos "
            "de comunicação.",

            "Existe definição de frequência de publicação.",

            "Os formatos de conteúdo estão previamente definidos.",

            "O documento apresenta objetivos diferentes para "
            "autoridade, educação, conexão e conversão.",

            "Existe preocupação com indicadores de desempenho.",

            "Há uma relação clara entre marketing, conteúdo "
            "e geração de leads."
        ]

        result["gaps"] = [
            "Não foram encontrados dados históricos de desempenho "
            "das publicações.",

            "Não há informações suficientes para determinar "
            "quais conteúdos geram maior retorno.",

            "Não foram identificadas metas numéricas claras "
            "para os principais KPIs.",

            "Não há dados suficientes para calcular o ROI real "
            "das ações de marketing.",

            "A estratégia define ações, mas ainda pode evoluir "
            "para um sistema de acompanhamento baseado em resultados."
        ]

        result["opportunities"] = [
            "Criar um painel de acompanhamento de desempenho "
            "das publicações.",

            "Comparar alcance, engajamento e geração de leads "
            "por tipo de conteúdo.",

            "Identificar quais pilares apresentam maior "
            "potencial de conversão.",

            "Relacionar campanhas de marketing com vendas.",

            "Utilizar dados históricos para otimizar os horários "
            "e formatos de publicação.",

            "Criar um ciclo contínuo de teste, análise e otimização."
        ]

        result["kpis"] = [
            "Alcance",
            "Impressões",
            "Taxa de engajamento",
            "Salvamentos",
            "Compartilhamentos",
            "Visualizações de Reels",
            "Retenção de vídeo",
            "Cliques",
            "Mensagens no Direct",
            "Leads gerados",
            "Taxa de conversão",
            "Custo por lead",
            "ROI",
            "ROAS"
        ]

        result["insights"] = [
            "A estratégia apresenta equilíbrio entre construção "
            "de autoridade, educação, relacionamento e conversão.",

            "A presença de um pilar específico de conversão indica "
            "que o marketing não está sendo tratado apenas como "
            "geração de alcance.",

            "A utilização de diferentes formatos permite testar "
            "diferentes comportamentos do público.",

            "A estratégia possui potencial para gerar leads através "
            "de chamadas para ação e contato pelo Direct.",

            "O principal próximo passo é conectar o planejamento "
            "de conteúdo aos resultados reais obtidos."
        ]

        result["recommendations"] = [
            "Definir metas numéricas para cada KPI.",
            "Registrar o desempenho de cada publicação.",
            "Comparar os resultados entre os quatro pilares.",
            "Identificar os conteúdos que geram mais leads.",
            "Relacionar leads gerados com vendas realizadas.",
            "Criar relatórios semanais de desempenho.",
            "Ajustar a estratégia com base nos dados coletados."
        ]

        result["action_plan"] = [
            {
                "step": 1,
                "action": "Definir KPIs e metas",
                "objective": (
                    "Estabelecer métricas claras para avaliar o desempenho."
                )
            },
            {
                "step": 2,
                "action": "Registrar resultados",
                "objective": (
                    "Criar histórico de desempenho das publicações."
                )
            },
            {
                "step": 3,
                "action": "Comparar conteúdos",
                "objective": (
                    "Identificar formatos e temas com melhor desempenho."
                )
            },
            {
                "step": 4,
                "action": "Relacionar marketing e vendas",
                "objective": (
                    "Medir quantos leads realmente geram oportunidades comerciais."
                )
            },
            {
                "step": 5,
                "action": "Otimizar estratégia",
                "objective": (
                    "Aumentar os resultados com base nos dados coletados."
                )
            }
        ]

    # ==========================================================
    # VENDAS
    # ==========================================================

    elif document_type == "vendas":

        result["summary"] = (
            "A CLOUDIX AI identificou um documento relacionado "
            "à área comercial e ao desempenho de vendas."
        )

        result["insights"] = [
            "Foram identificados elementos relacionados ao processo comercial.",
            "Os dados podem ser utilizados para avaliar o desempenho das vendas.",
            "A estrutura pode auxiliar na identificação de oportunidades comerciais.",
            "Os dados podem ser relacionados a clientes, leads, produtos e conversões."
        ]

        result["recommendations"] = [
            "Identificar produtos ou serviços com maior desempenho.",
            "Avaliar a evolução das vendas.",
            "Monitorar conversão de leads.",
            "Monitorar ticket médio.",
            "Relacionar vendas com geração de receita."
        ]

    # ==========================================================
    # FINANCEIRO
    # ==========================================================

    elif document_type == "financeiro":

        _build_financial_analysis(
            result,
            text
        )

    # ==========================================================
    # ATENDIMENTO
    # ==========================================================

    elif document_type == "atendimento":

        result["summary"] = (
            "A CLOUDIX AI identificou um documento relacionado "
            "ao atendimento e à experiência do cliente."
        )

        result["insights"] = [
            "Foram identificados elementos relacionados ao relacionamento com clientes.",
            "Os dados podem ajudar a avaliar a qualidade do atendimento.",
            "É possível identificar padrões de reclamações e solicitações.",
            "Indicadores podem revelar gargalos no atendimento."
        ]

        result["recommendations"] = [
            "Identificar os principais motivos de contato.",
            "Monitorar tempo médio de resposta.",
            "Identificar gargalos recorrentes.",
            "Avaliar satisfação dos clientes.",
            "Criar procedimentos para problemas recorrentes."
        ]

    # ==========================================================
    # ESTRATÉGIA
    # ==========================================================

    elif document_type == "estrategia":

        result["summary"] = (
            "A CLOUDIX AI identificou um documento relacionado "
            "ao planejamento e à estratégia empresarial."
        )

        result["insights"] = [
            "Foram identificados elementos relacionados ao planejamento estratégico.",
            "O documento pode conter objetivos e metas.",
            "Os dados podem ajudar a identificar prioridades.",
            "Os objetivos podem ser relacionados a indicadores.",
            "A estrutura pode auxiliar na identificação de oportunidades."
        ]

        result["recommendations"] = [
            "Transformar objetivos em metas mensuráveis.",
            "Definir indicadores.",
            "Priorizar ações de maior impacto.",
            "Relacionar estratégia com as demais áreas.",
            "Criar rotina de acompanhamento.",
            "Revisar periodicamente as metas."
        ]

    # ==========================================================
    # GERAL
    # ==========================================================

    else:

        result["summary"] = (
            "A CLOUDIX AI identificou a estrutura do documento, "
            "mas não conseguiu determinar com segurança qual "
            "área deve realizar a análise."
        )

        result["insights"] = [
            "O documento possui dados estruturados.",
            "Não foram encontrados elementos suficientes para classificação.",
            "Uma análise adicional pode determinar a área adequada."
        ]

        result["recommendations"] = [
            "Adicionar uma descrição sobre o objetivo do documento.",
            "Organizar os dados em tabelas com títulos claros.",
            "Permitir seleção manual da área da CLOUDIX AI.",
            "Utilizar a CLOUDIX AI Geral para documentos ambíguos."
        ]

    return result