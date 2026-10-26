import os
import pytest
from market_intelligence.models import (
    MarketIntelligenceReport,
    ImportanceLevel,
    SentimentType,
)
from market_intelligence.analyzer import MarketAnalyzer
from market_intelligence.markdown_generator import MarkdownReportGenerator
from market_intelligence.pdf_generator import ExecutiveSummaryPDFGenerator
from market_intelligence.history import HistoryTracker
from market_intelligence.notifications import NotificationDispatcher


def test_market_analyzer_stocks():
    analyzer = MarketAnalyzer("Bolsa Brasileira")
    report = analyzer.generate_daily_report()
    assert report.topic == "Bolsa Brasileira"
    assert report.confidence_score >= 80.0
    assert len(report.executive_summary_topics) > 0
    assert len(report.indicators) > 0
    assert len(report.sources) > 0


def test_market_analyzer_crypto():
    analyzer = MarketAnalyzer("Criptomoedas")
    report = analyzer.generate_daily_report()
    assert report.topic == "Criptomoedas"
    assert report.sentiment in [SentimentType.VERY_POSITIVE, SentimentType.POSITIVE]
    assert len(report.asset_movements) > 0


def test_markdown_generator():
    analyzer = MarketAnalyzer("Bolsa Americana")
    report = analyzer.generate_daily_report()
    md = MarkdownReportGenerator.generate_full_report(report)
    assert "# RELATÓRIO DIÁRIO DE INTELIGÊNCIA DE MERCADO" in md
    assert "## DASHBOARD EXECUTIVO" in md
    assert "## 10. CONCLUSÃO ESTRATÉGICA" in md


def test_pdf_generator(tmp_path):
    analyzer = MarketAnalyzer("Commodities")
    report = analyzer.generate_daily_report()
    pdf_path = os.path.join(tmp_path, "test_summary.pdf")
    generated = ExecutiveSummaryPDFGenerator.generate_pdf(report, pdf_path)
    assert os.path.exists(generated)
    assert os.path.getsize(generated) > 1000


def test_history_tracker(tmp_path):
    tracker = HistoryTracker(history_dir=str(tmp_path))
    analyzer = MarketAnalyzer("Bolsa Brasileira")
    
    rep1 = analyzer.generate_daily_report()
    rep1.date = "2026-10-25"
    rep1.sentiment = SentimentType.NEUTRAL
    tracker.save_report(rep1)

    rep2 = analyzer.generate_daily_report()
    rep2.date = "2026-10-26"
    rep2.sentiment = SentimentType.POSITIVE
    
    comp = tracker.compare_with_previous(rep2)
    assert comp.sentiment_changed is True
    assert comp.previous_sentiment == SentimentType.NEUTRAL
    assert comp.new_sentiment == SentimentType.POSITIVE


def test_notification_dispatcher():
    dispatcher = NotificationDispatcher()
    res = dispatcher.dispatch_all("Bolsa Brasileira", "2026-10-26", "Test summary")
    assert "email" in res
    assert "teams" in res
    assert "slack" in res
