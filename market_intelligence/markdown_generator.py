from typing import Optional
from market_intelligence.models import MarketIntelligenceReport, HistoryComparison


class MarkdownReportGenerator:
    """Generates complete Markdown daily report and executive dashboard."""

    @staticmethod
    def generate_full_report(report: MarketIntelligenceReport, comparison: Optional[HistoryComparison] = None) -> str:
        md = []
        md.append(f"# RELATÓRIO DIÁRIO DE INTELIGÊNCIA DE MERCADO")
        md.append(f"**Tópico / Tema:** {report.topic}")
        md.append(f"**Data da Análise:** {report.date}")
        md.append(f"**Nível de Confiança da Análise:** {report.confidence_score}%\n")
        
        md.append("---")
        md.append("## DASHBOARD EXECUTIVO")
        md.append(f"- **Tendência Geral:** {report.dashboard.general_trend}")
        md.append(f"- **Sentimento de Mercado:** {report.dashboard.sentiment.value}")
        md.append(f"- **Nível de Risco:** {report.dashboard.risk_level.value}")
        md.append(f"- **Oportunidades Identificadas:** {report.dashboard.opportunities_count}")
        md.append(f"- **Eventos Críticos da Semana:** {report.dashboard.critical_events_this_week}")
        md.append(f"- **Confiança da Análise (%):** {report.dashboard.confidence_score}%")
        md.append("---\n")

        if comparison and (comparison.relevant_changes or comparison.new_risks or comparison.new_opportunities or comparison.sentiment_changed):
            md.append("## 🔄 DESTAQUES COMPARATIVOS (VS. DIA ANTERIOR)")
            if comparison.sentiment_changed:
                md.append(f"- **Mudança de Sentimento:** De `{comparison.previous_sentiment.value if comparison.previous_sentiment else 'N/A'}` para `{comparison.new_sentiment.value}`")
            if comparison.relevant_changes:
                md.append("- **Mudanças Relevantes:**")
                for change in comparison.relevant_changes:
                    md.append(f"  - {change}")
            if comparison.new_risks:
                md.append("- **Novos Riscos Detectados:**")
                for r in comparison.new_risks:
                    md.append(f"  - [{r.level.value}] {r.category}: {r.description}")
            if comparison.new_opportunities:
                md.append("- **Novas Oportunidades Detectadas:**")
                for o in comparison.new_opportunities:
                    md.append(f"  - **{o.title}** ({o.category}): {o.justification}")
            md.append("\n---")

        md.append("## 1. RESUMO EXECUTIVO")
        for i, topic in enumerate(report.executive_summary_topics, 1):
            md.append(f"### 1.{i}. {topic.headline}")
            md.append(f"- **Impacto Esperado:** {topic.expected_impact}")
            md.append(f"- **Nível de Importância:** `{topic.importance.value}`\n")

        md.append("## 2. DESTAQUES DO DIA")
        for highlight in report.day_highlights:
            md.append(f"- {highlight}")
        md.append("\n---")

        md.append("## 3. TENDÊNCIAS DE MERCADO")
        md.append("### Tendências de Alta ⬆️")
        for b in report.bullish_trends:
            md.append(f"- {b}")
        
        md.append("\n### Tendências de Baixa ⬇️")
        for b in report.bearish_trends:
            md.append(f"- {b}")

        md.append("\n### Fatores Determinantes")
        for f in report.trend_factors:
            md.append(f"- {f}")
        md.append("\n---")

        md.append("## 4. INDICADORES ECONÔMICOS RELACIONADOS")
        md.append("| Indicador | Valor Atual | Valor Anterior | Variação | Possível Impacto |")
        md.append("|---|---|---|---|---|")
        for ind in report.indicators:
            md.append(f"| {ind.name} | {ind.current_value} | {ind.previous_value} | {ind.change} | {ind.impact} |")
        md.append("\n---")

        md.append("## 5. MOVIMENTAÇÃO DE ATIVOS")
        md.append("| Ativo | Tipo | Diária | Semanal | Mensal |")
        md.append("|---|---|---|---|---|")
        for a in report.asset_movements:
            md.append(f"| {a.asset_name} | {a.asset_type} | {a.daily_perf} | {a.weekly_perf} | {a.monthly_perf} |")
        md.append("\n---")

        md.append("## 6. RISCOS IDENTIFICADOS")
        for r in report.risks:
            md.append(f"- **[{r.level.value}] {r.category}:** {r.description}")
        md.append("\n---")

        md.append("## 7. OPORTUNIDADES DETECTADAS")
        for op in report.opportunities:
            md.append(f"- **{op.title}** ({op.category}): {op.justification}")
        md.append("\n---")

        md.append("## 8. SENTIMENTO DE MERCADO")
        md.append(f"**Classificação:** `{report.sentiment.value}`")
        md.append(f"**Evidências:** {report.sentiment_evidence}\n")
        md.append("---")

        md.append("## 9. RADAR DE EVENTOS (PRÓXIMOS EVENTOS CRÍTICOS)")
        md.append("| Data Prevista | Evento / Indicador | Impacto Esperado |")
        md.append("|---|---|---|")
        for ev in report.radar_events:
            md.append(f"| {ev.date} | {ev.event} | {ev.expected_impact} |")
        md.append("\n---")

        md.append("## 10. CONCLUSÃO ESTRATÉGICA")
        md.append(f"- **O que mudou?** {report.strategic_conclusion.what_changed}")
        md.append(f"- **O que merece atenção?** {report.strategic_conclusion.deserves_attention}")
        md.append(f"- **Quais oportunidades surgiram?** {report.strategic_conclusion.new_opportunities}")
        md.append(f"- **Quais riscos aumentaram?** {report.strategic_conclusion.increased_risks}")
        md.append(f"- **O que monitorar nos próximos dias?** {report.strategic_conclusion.monitoring_next_days}\n")
        md.append("---")

        md.append("## 11. LISTA DE FONTES UTILIZADAS E LINKS")
        for s in report.sources:
            md.append(f"- **{s.name}** (Confiabilidade: {s.reliability}) - [{s.headline}]({s.url}) [{s.timestamp}]")

        return "\n".join(md)
