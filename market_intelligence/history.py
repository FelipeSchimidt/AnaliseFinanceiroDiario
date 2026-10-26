import os
import json
from typing import Optional, List
from market_intelligence.models import MarketIntelligenceReport, HistoryComparison, RiskItem, OpportunityItem


class HistoryTracker:
    """Saves daily reports to disk and computes day-over-day changes."""

    def __init__(self, history_dir: str = "data/history"):
        self.history_dir = history_dir
        os.makedirs(self.history_dir, exist_ok=True)

    def _get_filename(self, topic: str, date_str: str) -> str:
        safe_topic = "".join(c if c.isalnum() else "_" for c in topic)
        return os.path.join(self.history_dir, f"{safe_topic}_{date_str}.json")

    def save_report(self, report: MarketIntelligenceReport) -> str:
        filepath = self._get_filename(report.topic, report.date)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))
        return filepath

    def get_latest_previous_report(self, topic: str, current_date: str) -> Optional[MarketIntelligenceReport]:
        safe_topic = "".join(c if c.isalnum() else "_" for c in topic)
        files = [
            f for f in os.listdir(self.history_dir)
            if f.startswith(safe_topic) and f.endswith(".json") and not f.endswith(f"{current_date}.json")
        ]
        if not files:
            return None
        
        files.sort(reverse=True)
        latest_file = os.path.join(self.history_dir, files[0])
        try:
            with open(latest_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return MarketIntelligenceReport(**data)
        except Exception:
            return None

    def compare_with_previous(self, current: MarketIntelligenceReport) -> HistoryComparison:
        previous = self.get_latest_previous_report(current.topic, current.date)
        if not previous:
            return HistoryComparison(
                current_date=current.date,
                previous_date=None,
                sentiment_changed=False,
                previous_sentiment=None,
                new_sentiment=current.sentiment,
                new_risks=[],
                new_opportunities=[],
                relevant_changes=["Primeiro relatório gerado para este tópico no histórico."],
            )

        sentiment_changed = current.sentiment != previous.sentiment

        prev_risk_descs = {r.description.strip().lower() for r in previous.risks}
        new_risks = [r for r in current.risks if r.description.strip().lower() not in prev_risk_descs]

        prev_opp_titles = {o.title.strip().lower() for o in previous.opportunities}
        new_opps = [o for o in current.opportunities if o.title.strip().lower() not in prev_opp_titles]

        relevant_changes = []
        if sentiment_changed:
            relevant_changes.append(f"Sentimento de mercado alterou de {previous.sentiment.value} para {current.sentiment.value}.")
        if current.dashboard.general_trend != previous.dashboard.general_trend:
            relevant_changes.append(f"Tendência geral mudou de {previous.dashboard.general_trend} para {current.dashboard.general_trend}.")
        if new_risks:
            relevant_changes.append(f"{len(new_risks)} novos riscos foram identificados.")
        if new_opps:
            relevant_changes.append(f"{len(new_opps)} novas oportunidades surgiram.")

        return HistoryComparison(
            current_date=current.date,
            previous_date=previous.date,
            sentiment_changed=sentiment_changed,
            previous_sentiment=previous.sentiment,
            new_sentiment=current.sentiment,
            new_risks=new_risks,
            new_opportunities=new_opps,
            relevant_changes=relevant_changes,
        )
