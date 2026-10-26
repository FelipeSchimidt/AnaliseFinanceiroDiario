from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ImportanceLevel(str, Enum):
    HIGH = "Alto"
    MEDIUM = "Médio"
    LOW = "Baixo"


class SentimentType(str, Enum):
    VERY_POSITIVE = "Muito Positivo"
    POSITIVE = "Positivo"
    NEUTRAL = "Neutro"
    NEGATIVE = "Negativo"
    VERY_NEGATIVE = "Muito Negativo"


class TrendDirection(str, Enum):
    UP = "⬆️ High"
    DOWN = "⬇️ Low"
    SIDEWAYS = "➡️ Sideways"


class Indicator(BaseModel):
    name: str
    current_value: str
    previous_value: str
    change: str
    impact: str


class AssetMovement(BaseModel):
    asset_name: str
    asset_type: str  # Action, ETF, Commodity, Crypto, Currency
    daily_perf: str
    weekly_perf: str
    monthly_perf: str


class RiskItem(BaseModel):
    category: str  # Economic, Political, Regulatory, Geopolitical, Sectoral
    description: str
    level: ImportanceLevel


class OpportunityItem(BaseModel):
    title: str
    category: str  # Promising Sector, Highlighted Company, Asset, Emerging Trend
    justification: str


class EventItem(BaseModel):
    date: str
    event: str
    expected_impact: str


class NewsSource(BaseModel):
    name: str
    reliability: str
    url: str
    headline: str
    timestamp: str


class StrategicConclusion(BaseModel):
    what_changed: str
    deserves_attention: str
    new_opportunities: str
    increased_risks: str
    monitoring_next_days: str


class ExecutiveSummaryTopic(BaseModel):
    headline: str
    expected_impact: str
    importance: ImportanceLevel


class ExecutiveDashboard(BaseModel):
    general_trend: str
    sentiment: SentimentType
    risk_level: ImportanceLevel
    opportunities_count: int
    critical_events_this_week: int
    confidence_score: float  # e.g. 92.5 (%)


class MarketIntelligenceReport(BaseModel):
    topic: str
    date: str
    confidence_score: float
    executive_summary_topics: List[ExecutiveSummaryTopic] = Field(default_factory=list)
    day_highlights: List[str] = Field(default_factory=list)
    bullish_trends: List[str] = Field(default_factory=list)
    bearish_trends: List[str] = Field(default_factory=list)
    trend_factors: List[str] = Field(default_factory=list)
    indicators: List[Indicator] = Field(default_factory=list)
    asset_movements: List[AssetMovement] = Field(default_factory=list)
    risks: List[RiskItem] = Field(default_factory=list)
    opportunities: List[OpportunityItem] = Field(default_factory=list)
    sentiment: SentimentType
    sentiment_evidence: str
    radar_events: List[EventItem] = Field(default_factory=list)
    strategic_conclusion: StrategicConclusion
    sources: List[NewsSource] = Field(default_factory=list)
    dashboard: ExecutiveDashboard


class HistoryComparison(BaseModel):
    current_date: str
    previous_date: Optional[str]
    sentiment_changed: bool
    previous_sentiment: Optional[SentimentType]
    new_sentiment: SentimentType
    new_risks: List[RiskItem] = Field(default_factory=list)
    new_opportunities: List[OpportunityItem] = Field(default_factory=list)
    relevant_changes: List[str] = Field(default_factory=list)
