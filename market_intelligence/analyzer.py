from market_intelligence.models import MarketIntelligenceReport
from market_intelligence.fetcher import MarketDataFetcher


class MarketAnalyzer:
    """Consolidates news, calculates confidence score, and eliminates redundancies."""

    def __init__(self, topic: str):
        self.topic = topic
        self.fetcher = MarketDataFetcher(topic)

    def generate_daily_report(self) -> MarketIntelligenceReport:
        report = self.fetcher.gather_data_and_analyze()
        
        # Ensure confidence score logic based on source reliability
        high_reliability_count = sum(
            1 for s in report.sources if "Alta" in s.reliability or "90%" in s.reliability or "95%" in s.reliability or "98%" in s.reliability
        )
        if len(report.sources) > 0:
            calc_confidence = min(99.0, round(80.0 + (high_reliability_count / len(report.sources)) * 18.0, 1))
            report.confidence_score = calc_confidence
            report.dashboard.confidence_score = calc_confidence

        return report
