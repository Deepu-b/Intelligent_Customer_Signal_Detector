"""
Data Loader and Stage-1 Deterministic Filter for Intelligent Customer Signal Detector POC.
Domain: FinTech / Wealth-Tech Trading & Investment Platform

Implements:
1. CSV Loading & Schema Validation
2. Stage-1 Deterministic Funnel & Telemetry Anomaly Scoring (0-100)
3. Multi-Signal Flag Generation
4. High-level Portfolio & Operations Aggregates
"""

import os
import csv
from typing import List, Dict, Any, Optional, Tuple


class CustomerRecord:
    """Represents a validated single customer telemetry record."""
    def __init__(self, data: Dict[str, Any]):
        self.customer_id: str = str(data.get("customer_id", "")).strip()
        self.customer_name: str = str(data.get("customer_name", "Anonymous")).strip()
        self.account_tier: str = str(data.get("account_tier", "Standard")).strip()
        
        # Numeric conversions with fallback defaults
        self.portfolio_value_inr: float = float(data.get("portfolio_value_inr", 0.0))
        self.trading_volume_change_30d_pct: float = float(data.get("trading_volume_change_30d_pct", 0.0))
        self.net_outflow_30d_inr: float = float(data.get("net_outflow_30d_inr", 0.0))
        self.failed_orders_30d: int = int(float(data.get("failed_orders_30d", 0)))
        self.tickets_opened_30d: int = int(float(data.get("tickets_opened_30d", 0)))
        self.avg_latency_30d_ms: float = float(data.get("avg_latency_30d_ms", 0.0))
        
        # Raw unstructured interaction transcript
        self.recent_interaction_transcript: str = str(data.get("recent_interaction_transcript", "")).strip()
        
        # Stage 1 Computed Properties
        self.outflow_ratio_pct: float = (self.net_outflow_30d_inr / self.portfolio_value_inr * 100.0) if self.portfolio_value_inr > 0 else 0.0
        self.signal_flags: Dict[str, bool] = self._compute_signal_flags()
        self.anomaly_count: int = sum(1 for v in self.signal_flags.values() if v)
        self.stage1_telemetry_score: float = self._compute_stage1_score()
        self.is_candidate_for_llm: bool = self._is_candidate()

    def _compute_signal_flags(self) -> Dict[str, bool]:
        """Evaluates individual telemetry anomaly triggers."""
        return {
            "volume_contraction": self.trading_volume_change_30d_pct < -30.0,
            "capital_outflow": (self.outflow_ratio_pct > 12.0) or (self.net_outflow_30d_inr >= 1000000.0),
            "latency_degradation": self.avg_latency_30d_ms >= 300.0,
            "order_execution_failure": self.failed_orders_30d >= 2,
            "support_friction": self.tickets_opened_30d >= 2,
        }

    def _compute_stage1_score(self) -> float:
        """
        Computes a deterministic telemetry risk score between 0.0 and 100.0.
        Weights multi-signal anomalies and scales with account tier sensitivity.
        """
        score = 0.0
        
        # Volume drop contribution (up to 25 pts)
        if self.trading_volume_change_30d_pct < 0:
            drop_mag = min(abs(self.trading_volume_change_30d_pct), 100.0)
            score += (drop_mag / 100.0) * 25.0
            
        # Outflow contribution (up to 30 pts)
        outflow_weight = min(self.outflow_ratio_pct, 100.0) / 100.0
        score += outflow_weight * 30.0
        
        # Latency contribution (up to 20 pts)
        if self.avg_latency_30d_ms > 100.0:
            excess_latency = min(self.avg_latency_30d_ms - 100.0, 900.0) / 900.0
            score += excess_latency * 20.0
            
        # Order failure contribution (up to 15 pts)
        fail_pts = min(self.failed_orders_30d * 2.5, 15.0)
        score += fail_pts
        
        # Ticket volume contribution (up to 10 pts)
        ticket_pts = min(self.tickets_opened_30d * 2.0, 10.0)
        score += ticket_pts
        
        # Tier Multiplier (HNIs and Pro Traders have higher financial sensitivity)
        tier_multiplier = 1.15 if self.account_tier == "HNI" else (1.05 if self.account_tier == "Pro Trader" else 1.0)
        final_score = min(score * tier_multiplier, 100.0)
        return round(final_score, 1)

    def _is_candidate(self) -> bool:
        """
        Stage 1 Funnel Decision:
        Determines whether record should be routed to Stage 2 Cognitive LLM Synthesizer.
        """
        # Route to LLM if:
        # 1. 2 or more signals triggered simultaneously
        # 2. Stage 1 score >= 28.0
        # 3. High Net-Worth (HNI) with any single signal (zero-tolerance for silent HNI churn)
        # 4. Explicit support tickets >= 1 with any volume drop
        if self.anomaly_count >= 2:
            return True
        if self.stage1_telemetry_score >= 28.0:
            return True
        if self.account_tier == "HNI" and (self.anomaly_count >= 1 or self.outflow_ratio_pct > 5.0):
            return True
        if self.tickets_opened_30d >= 1 and self.trading_volume_change_30d_pct < -20.0:
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Converts object back to serializable dictionary."""
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "account_tier": self.account_tier,
            "portfolio_value_inr": self.portfolio_value_inr,
            "trading_volume_change_30d_pct": self.trading_volume_change_30d_pct,
            "net_outflow_30d_inr": self.net_outflow_30d_inr,
            "outflow_ratio_pct": round(self.outflow_ratio_pct, 1),
            "failed_orders_30d": self.failed_orders_30d,
            "tickets_opened_30d": self.tickets_opened_30d,
            "avg_latency_30d_ms": self.avg_latency_30d_ms,
            "signal_flags": self.signal_flags,
            "anomaly_count": self.anomaly_count,
            "stage1_telemetry_score": self.stage1_telemetry_score,
            "is_candidate_for_llm": self.is_candidate_for_llm,
            "recent_interaction_transcript": self.recent_interaction_transcript,
        }


class CustomerDataLoader:
    """Handles loading, filtering, and aggregation of customer data."""
    
    def __init__(self, csv_filepath: Optional[str] = None):
        if csv_filepath is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.csv_filepath = os.path.join(base_dir, "data", "customers.csv")
        else:
            self.csv_filepath = csv_filepath
            
        self.records: List[CustomerRecord] = []
        self._load_data()

    def _load_data(self) -> None:
        """Reads CSV file and parses CustomerRecord objects."""
        if not os.path.exists(self.csv_filepath):
            raise FileNotFoundError(f"Customer dataset not found at: {self.csv_filepath}")
            
        with open(self.csv_filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.records = [CustomerRecord(row) for row in reader]

    def get_all_records(self) -> List[CustomerRecord]:
        """Returns all loaded customer records."""
        return self.records

    def get_candidates_for_llm(self) -> List[CustomerRecord]:
        """Returns records flagged by Stage-1 deterministic funnel for LLM reasoning."""
        return [r for r in self.records if r.is_candidate_for_llm]

    def get_healthy_cohort(self) -> List[CustomerRecord]:
        """Returns records classified as healthy baseline by Stage-1."""
        return [r for r in self.records if not r.is_candidate_for_llm]

    def get_record_by_id(self, customer_id: str) -> Optional[CustomerRecord]:
        """Looks up a customer by their unique ID."""
        for r in self.records:
            if r.customer_id == customer_id:
                return r
        return None

    def get_summary_metrics(self) -> Dict[str, Any]:
        """Calculates executive and operational summary metrics across the dataset."""
        total_customers = len(self.records)
        if total_customers == 0:
            return {}

        candidates = self.get_candidates_for_llm()
        total_aum = sum(r.portfolio_value_inr for r in self.records)
        total_outflows = sum(r.net_outflow_30d_inr for r in self.records)
        at_risk_aum = sum(r.portfolio_value_inr for r in candidates)
        at_risk_outflows = sum(r.net_outflow_30d_inr for r in candidates)
        
        tier_breakdown = {}
        for r in self.records:
            tier_breakdown[r.account_tier] = tier_breakdown.get(r.account_tier, 0) + 1
            
        candidate_tier_breakdown = {}
        for r in candidates:
            candidate_tier_breakdown[r.account_tier] = candidate_tier_breakdown.get(r.account_tier, 0) + 1

        return {
            "total_monitored_customers": total_customers,
            "stage1_candidates_count": len(candidates),
            "stage1_candidate_pct": round(len(candidates) / total_customers * 100.0, 1),
            "total_aum_inr": total_aum,
            "total_net_outflow_inr": total_outflows,
            "at_risk_portfolio_inr": at_risk_aum,
            "at_risk_portfolio_pct": round(at_risk_aum / total_aum * 100.0, 1) if total_aum > 0 else 0.0,
            "at_risk_outflow_inr": at_risk_outflows,
            "tier_distribution": tier_breakdown,
            "candidate_tier_distribution": candidate_tier_breakdown,
        }


if __name__ == "__main__":
    loader = CustomerDataLoader()
    metrics = loader.get_summary_metrics()
    
    print("=" * 70)
    print("STAGE 1 DETERMINISTIC FUNNEL & DATA LOADER SUMMARY")
    print("=" * 70)
    print(f"Total Monitored Accounts:     {metrics['total_monitored_customers']}")
    print(f"Stage-1 Flagged Candidates:   {metrics['stage1_candidates_count']} ({metrics['stage1_candidate_pct']}%)")
    print(f"Total Platform Assets (AUM):  ₹{metrics['total_aum_inr']:,.2f}")
    print(f"Total Portfolio at Risk:      ₹{metrics['at_risk_portfolio_inr']:,.2f} ({metrics['at_risk_portfolio_pct']}%)")
    print(f"30-Day Outflow at Risk:       ₹{metrics['at_risk_outflow_inr']:,.2f}")
    
    print("\nStage-1 Candidates by Tier:")
    for tier, cnt in metrics['candidate_tier_distribution'].items():
        total_in_tier = metrics['tier_distribution'].get(tier, 0)
        print(f"  - {tier:<12}: {cnt:2d} / {total_in_tier:2d} flagged ({cnt/total_in_tier*100:.1f}%)")
        
    print("\nTop 5 Stage-1 Flagged Accounts by Telemetry Score:")
    sorted_candidates = sorted(loader.get_candidates_for_llm(), key=lambda x: x.stage1_telemetry_score, reverse=True)
    for c in sorted_candidates[:5]:
        print(f"  [{c.customer_id}] {c.customer_name:<24} | Tier: {c.account_tier:<10} | Stage1 Score: {c.stage1_telemetry_score:>5.1f} | Anomalies: {c.anomaly_count}/5")
    print("=" * 70)
