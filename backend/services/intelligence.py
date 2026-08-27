def generate_intelligence(analysis):
    """
    Gera inteligência inicial com base no tipo de documento
    identificado pelo analisador da CLOUDIX AI.

    Funcionalidades:
    - Vendas
    - Marketing
    - Financeiro
    - Atendimento
    - Estratégia
    """

    document_type = analysis["document_type"]["type"]

    text = analysis.get("text", "")

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

    result = {
        "document_type": document_type,
        "summary": "",
        "insights": [],
        "recommendations": [],
        "metadata": {
            "rows": rows,
            "columns": columns,
            "sections_found": len(sections)
        }
    }

    # ==========================================================
    # VENDAS
    # ==========================================================

    if document_type == "vendas":

        result["summary"] = (
            "A CLOUDIX AI identificou o documento como "
            "relacionado à área de vendas e desempenho comercial."
        )

        result["insights"] = [
            "Foram identificados elementos relacionados ao processo comercial.",
            "Os dados podem ser utilizados para avaliar desempenho de vendas.",
            "A estrutura permite investigar oportunidades de melhoria no processo comercial.",
            "É possível relacionar os dados com clientes, produtos, leads e conversões."
        ]

        result["recommendations"] = [
            "Identificar produtos ou serviços com maior desempenho.",
            "Avaliar a evolução das vendas ao longo dos períodos disponíveis.",
            "Identificar oportunidades de aumento da conversão de leads.",
            "Monitorar ticket médio e volume de vendas.",
            "Relacionar ações comerciais com geração de receita."
        ]

    # ==========================================================
    # MARKETING
    # ==========================================================

    elif document_type == "marketing":

        result["summary"] = (
            "A CLOUDIX AI identificou o documento como "
            "relacionado à área de marketing, comunicação e crescimento."
        )

        result["insights"] = [
            "Foram identificados elementos relacionados ao planejamento de marketing.",
            "O documento apresenta estrutura de organização de ações e conteúdos.",
            "Foram encontrados possíveis pilares estratégicos de comunicação.",
            "Existem indicadores que podem ser utilizados para medir o desempenho das ações.",
            "As ações de marketing podem ser relacionadas à geração de leads e vendas."
        ]

        result["recommendations"] = [
            "Transformar as ações de marketing em metas mensuráveis.",
            "Acompanhar os principais KPIs de cada ação.",
            "Identificar quais conteúdos apresentam maior potencial de engajamento.",
            "Relacionar campanhas de marketing com geração de leads.",
            "Avaliar a contribuição do marketing para as vendas.",
            "Criar uma rotina de análise e otimização dos resultados."
        ]

    # ==========================================================
    # FINANCEIRO
    # ==========================================================

    elif document_type == "financeiro":

        result["summary"] = (
            "A CLOUDIX AI identificou o documento como "
            "relacionado à gestão financeira da empresa."
        )

        result["insights"] = [
            "Foram identificados elementos potencialmente relacionados à movimentação financeira.",
            "Os dados podem permitir análise de receitas e despesas.",
            "É possível identificar padrões de entradas e saídas.",
            "Os dados podem auxiliar na avaliação da saúde financeira da empresa."
        ]

        result["recommendations"] = [
            "Separar receitas, custos e despesas.",
            "Calcular o resultado financeiro dos períodos analisados.",
            "Identificar categorias com maior impacto financeiro.",
            "Monitorar evolução das receitas e despesas.",
            "Avaliar oportunidades de redução de custos.",
            "Criar indicadores de margem, crescimento e rentabilidade."
        ]

    # ==========================================================
    # ATENDIMENTO
    # ==========================================================

    elif document_type == "atendimento":

        result["summary"] = (
            "A CLOUDIX AI identificou o documento como "
            "relacionado à área de atendimento e experiência do cliente."
        )

        result["insights"] = [
            "Foram identificados elementos relacionados ao relacionamento com clientes.",
            "Os dados podem ajudar a avaliar a qualidade do atendimento.",
            "É possível identificar padrões de reclamações, solicitações ou dúvidas.",
            "Indicadores de atendimento podem ser utilizados para encontrar gargalos.",
            "Os dados podem contribuir para melhorar a experiência do cliente."
        ]

        result["recommendations"] = [
            "Identificar os principais motivos de contato dos clientes.",
            "Monitorar tempo médio de resposta.",
            "Identificar gargalos recorrentes no atendimento.",
            "Avaliar índices de satisfação dos clientes.",
            "Criar procedimentos para problemas recorrentes.",
            "Relacionar problemas de atendimento com retenção e vendas."
        ]

    # ==========================================================
    # ESTRATÉGIA
    # ==========================================================

    elif document_type == "estrategia":

        result["summary"] = (
            "A CLOUDIX AI identificou o documento como "
            "relacionado ao planejamento e à estratégia empresarial."
        )

        result["insights"] = [
            "Foram identificados elementos relacionados ao planejamento estratégico.",
            "O documento pode conter objetivos, metas e direcionamentos para a empresa.",
            "Os dados podem ser utilizados para identificar prioridades estratégicas.",
            "É possível relacionar objetivos estratégicos com indicadores de desempenho.",
            "A estrutura pode auxiliar na identificação de oportunidades e gargalos."
        ]

        result["recommendations"] = [
            "Transformar objetivos estratégicos em metas mensuráveis.",
            "Definir indicadores para acompanhar cada objetivo.",
            "Priorizar ações com maior impacto para o negócio.",
            "Relacionar estratégia com vendas, marketing, financeiro e atendimento.",
            "Criar uma rotina de acompanhamento dos resultados.",
            "Revisar periodicamente as metas e ajustar o planejamento."
        ]

    # ==========================================================
    # GERAL
    # ==========================================================

    else:

        result["summary"] = (
            "A CLOUDIX AI identificou a estrutura do documento, "
            "mas não conseguiu determinar com segurança qual "
            "das cinco áreas deve realizar a análise."
        )

        result["insights"] = [
            "O documento possui dados estruturados.",
            "Não foram encontrados elementos suficientes para classificar o documento.",
            "Uma análise adicional pode determinar a área mais adequada."
        ]

        result["recommendations"] = [
            "Adicionar uma descrição sobre o objetivo do documento.",
            "Organizar os dados em tabelas com títulos e categorias claras.",
            "Permitir que o usuário selecione manualmente a área da CLOUDIX AI.",
            "Utilizar a CLOUDIX AI Geral para interpretar documentos ambíguos."
        ]

    return result