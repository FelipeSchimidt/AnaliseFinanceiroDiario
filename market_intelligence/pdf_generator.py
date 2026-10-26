import re
from fpdf import FPDF
from market_intelligence.models import MarketIntelligenceReport


def clean_unicode(text: str) -> str:
    """Sanitize symbols or non-latin1 characters for standard FPDF core fonts."""
    if not text:
        return ""
    replacements = {
        "⬆️": "[ALTA]",
        "⬆": "[ALTA]",
        "⬇️": "[BAIXA]",
        "⬇": "[BAIXA]",
        "➡️": "[NEUTRO]",
        "•": "-",
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')


class ExecutiveSummaryPDFGenerator:
    """Generates a clean, professional 1-page Executive Summary PDF using fpdf2."""

    @staticmethod
    def generate_pdf(report: MarketIntelligenceReport, output_filepath: str) -> str:
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(left=12, top=12, right=12)
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=12)

        # Usable width: 210 - 24 = 186 mm
        eff_width = 186

        # Header Title
        pdf.set_font("Helvetica", style="B", size=14)
        pdf.set_text_color(20, 35, 60)  # Dark navy
        pdf.cell(w=eff_width, h=8, text=clean_unicode("RESUMO EXECUTIVO DIÁRIO - INTELIGÊNCIA DE MERCADO"), new_x="LMARGIN", new_y="NEXT", align="C")

        # Subtitle
        pdf.set_font("Helvetica", size=9)
        pdf.set_text_color(100, 100, 100)
        subtitle_str = f"Tema: {report.topic} | Data: {report.date} | Nível de Confiança: {report.confidence_score}%"
        pdf.cell(w=eff_width, h=5, text=clean_unicode(subtitle_str), new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(2)

        # Line divider
        pdf.set_draw_color(200, 200, 200)
        pdf.line(12, pdf.get_y(), 198, pdf.get_y())
        pdf.ln(3)

        # Executive Dashboard Box
        pdf.set_fill_color(240, 244, 248)
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.set_text_color(20, 35, 60)
        pdf.cell(w=eff_width, h=6, text=clean_unicode(" DASHBOARD EXECUTIVO"), fill=True, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", size=8.5)
        pdf.set_text_color(40, 40, 40)
        
        dash_text = (
            f"Tendência Geral: {report.dashboard.general_trend}   |   "
            f"Sentimento: {report.dashboard.sentiment.value}   |   "
            f"Risco: {report.dashboard.risk_level.value}\n"
            f"Oportunidades Mapeadas: {report.dashboard.opportunities_count}   |   "
            f"Eventos Críticos Semanais: {report.dashboard.critical_events_this_week}"
        )
        pdf.multi_cell(w=eff_width, h=4.5, text=clean_unicode(dash_text))
        pdf.ln(2)

        # Section 1: Executive Summary Topics
        pdf.set_fill_color(230, 238, 245)
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.set_text_color(20, 35, 60)
        pdf.cell(w=eff_width, h=6, text=clean_unicode(" 1. RESUMO EXECUTIVO E DESTAQUES CHAVE"), fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        for topic in report.executive_summary_topics:
            pdf.set_font("Helvetica", style="B", size=8.5)
            pdf.set_text_color(0, 51, 102)
            pdf.multi_cell(w=eff_width, h=4, text=clean_unicode(f"- [{topic.importance.value}] {topic.headline}"))
            pdf.set_font("Helvetica", size=8)
            pdf.set_text_color(60, 60, 60)
            pdf.multi_cell(w=eff_width, h=3.8, text=clean_unicode(f"  Impacto Esperado: {topic.expected_impact}"))
            pdf.ln(1)

        pdf.ln(2)

        # Section 2: Strategic Conclusion
        pdf.set_fill_color(230, 238, 245)
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.set_text_color(20, 35, 60)
        pdf.cell(w=eff_width, h=6, text=clean_unicode(" 2. CONCLUSÃO ESTRATÉGICA"), fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.set_font("Helvetica", size=8)
        pdf.set_text_color(40, 40, 40)
        sc = report.strategic_conclusion
        pdf.multi_cell(w=eff_width, h=3.8, text=clean_unicode(f"- O que mudou: {sc.what_changed}"))
        pdf.multi_cell(w=eff_width, h=3.8, text=clean_unicode(f"- Merece atenção: {sc.deserves_attention}"))
        pdf.multi_cell(w=eff_width, h=3.8, text=clean_unicode(f"- Novas Oportunidades: {sc.new_opportunities}"))
        pdf.multi_cell(w=eff_width, h=3.8, text=clean_unicode(f"- Monitoramento (Próximos dias): {sc.monitoring_next_days}"))

        pdf.ln(3)
        
        # Footer
        pdf.set_font("Helvetica", style="I", size=7.5)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(w=eff_width, h=4, text=clean_unicode("Relatório gerado automaticamente por Análise Financeiro Diário - Inteligência de Mercado"), align="C")

        pdf.output(output_filepath)
        return output_filepath
