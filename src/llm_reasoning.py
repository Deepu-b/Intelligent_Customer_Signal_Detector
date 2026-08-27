"""
Cognitive LLM Synthesizer & Multi-Signal Reasoning Engine for Intelligent Customer Signal Detector POC.
Domain: FinTech / Wealth-Tech Trading & Investment Platform

Features:
- Micro-Batching Architecture (Batches of 15 candidate records per request)
- Robust JSON List/Dict Response Normalizer (handles single-item arrays and object wrappers)
- Global Cohort Context Injection for relative calibration across all records
- Concurrent execution (max 3 workers, strictly <= 5 RPM Free Tier limit)
- Automatic 429 backoff retry resilience
- Enforced native JSON output via Google Gemini API (gemini-3.5-flash-lite / gemini-3.5-flash)
"""

import os
import sys
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, Optional, List

# Ensure root & src directories are in path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Safe environment loading
def _load_env_files():
    try:
        from dotenv import load_dotenv
        load_dotenv()
        load_dotenv(os.path.join(parent_dir, ".env"))
        load_dotenv(os.path.join(os.getcwd(), ".env"))
    except ImportError:
        pass
        
    for path in [os.path.join(parent_dir, ".env"), os.path.join(os.getcwd(), ".env"), ".env"]:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            except Exception:
                pass

_load_env_files()


SYSTEM_PROMPT = """
You are the Lead Customer Retention & Risk AI Synthesizer for a FinTech & Wealth-Tech Trading platform.
Your task is to analyze customer telemetry alongside raw support/chat transcripts to detect early warning signals of churn, frustration, or operational risk BEFORE formal escalation occurs.

CRITICAL DIRECTIVES:
1. Perform "Cognitive Synthesis"—connect the dots between unstructured text nuances (tone, unstated intentions, competitor mentions, passive-aggression, deactivation queries) and structured telemetry anomalies (latency spikes, execution errors, volume drops, capital outflows).
2. Use the provided Global Cohort Baseline to calibrate how extreme this customer's anomalies are relative to the broader population.
3. Distinguish between 'False Alarms' (e.g. passionate power-user feature requests or routine inquiries) and 'Silent Churn' (e.g. HNIs with massive outflows, subtle requests for withdrawal limits, and polite refusals of support tickets).
4. Output MUST be valid JSON conforming strictly to the requested schema.
"""


def build_microbatch_prompt(candidate_chunk: List[Dict[str, Any]], cohort_baseline: Dict[str, float]) -> str:
    """
    Builds a micro-batch prompt for a chunk of up to 15 customers with global cohort baseline calibration.
    """
    baseline_section = f"""
[GLOBAL COHORT BASELINE (For Relative Calibration)]:
- Platform Candidate Avg Routing Latency: {cohort_baseline.get('avg_latency_ms', 0):.1f} ms
- Platform Candidate Avg 30-Day Net Outflow: ₹{cohort_baseline.get('avg_outflow_inr', 0):,.2f}
- Platform Candidate Avg 30-Day Volume Change: {cohort_baseline.get('avg_volume_change_pct', 0):.1f}%
"""

    payload_items = []
    for c in candidate_chunk:
        payload_items.append({
            "customer_id": c.get("customer_id"),
            "customer_name": c.get("customer_name"),
            "account_tier": c.get("account_tier"),
            "portfolio_value_inr": float(c.get("portfolio_value_inr", 0)),
            "trading_volume_change_30d_pct": float(c.get("trading_volume_change_30d_pct", 0)),
            "net_outflow_30d_inr": float(c.get("net_outflow_30d_inr", 0)),
            "failed_orders_30d": int(float(c.get("failed_orders_30d", 0))),
            "tickets_opened_30d": int(float(c.get("tickets_opened_30d", 0))),
            "avg_latency_30d_ms": float(c.get("avg_latency_30d_ms", 0)),
            "recent_interaction_transcript": c.get("recent_interaction_transcript", "")
        })

    return f"""
{baseline_section}
Analyze the following batch of {len(payload_items)} at-risk customer profiles.
For EACH customer, perform multi-signal cognitive synthesis correlating their raw chat transcript with their telemetry numbers.

INPUT CUSTOMER PROFILES (JSON):
{json.dumps(payload_items, indent=2)}

OUTPUT REQUIREMENTS:
Return a JSON array containing the structured evaluations for ALL {len(payload_items)} customers in this batch chunk.
Each object in the JSON array MUST have these exact fields:
[
  {{
    "customer_id": "<ID of the customer>",
    "risk_level": "Critical" | "High" | "Medium" | "Low",
    "risk_score": <integer from 1 to 100>,
    "urgency_window": "< 24 Hours" | "2-3 Days" | "1-2 Weeks" | "Stable / Monitor",
    "primary_risk_driver": "<Concise 3-6 word label of root cause>",
    "agent_situation_summary": "<2 crisp sentences summarizing the situation and immediate next step for the frontline operations representative>",
    "signal_correlation_rationale": "<2-4 sentences explaining how the transcript nuances correlate with the telemetry numbers>",
    "prescriptive_action": "<Concrete, department-specific retention or operational action playbook>",
    "confidence_score": <float between 0.70 and 0.99>
  }}
]
"""


def build_single_analysis_prompt(customer_data: Dict[str, Any], cohort_baseline: Optional[Dict[str, float]] = None) -> str:
    """Builds prompt for analyzing a single customer on demand."""
    baseline_section = ""
    if cohort_baseline:
        baseline_section = f"""
[GLOBAL COHORT BASELINE (For Relative Calibration)]:
- Platform Candidate Avg Routing Latency: {cohort_baseline.get('avg_latency_ms', 0):.1f} ms
- Platform Candidate Avg 30-Day Net Outflow: ₹{cohort_baseline.get('avg_outflow_inr', 0):,.2f}
- Platform Candidate Avg 30-Day Volume Change: {cohort_baseline.get('avg_volume_change_pct', 0):.1f}%
"""

    return f"""
{baseline_section}
Analyze the following customer interaction and telemetry profile:

[CUSTOMER TELEMETRY PROFILE]:
- Customer ID: {customer_data.get('customer_id')}
- Customer Name: {customer_data.get('customer_name')}
- Account Tier: {customer_data.get('account_tier')} (Standard / Pro Trader / HNI)
- Portfolio Value (AUM): ₹{float(customer_data.get('portfolio_value_inr', 0)):,.2f}
- 30-Day Trading Volume Change: {customer_data.get('trading_volume_change_30d_pct')}%
- 30-Day Net Capital Outflow: ₹{float(customer_data.get('net_outflow_30d_inr', 0)):,.2f}
- Failed Orders (30d): {customer_data.get('failed_orders_30d')}
- Support Tickets (30d): {customer_data.get('tickets_opened_30d')}
- Avg Order Routing Latency (30d): {customer_data.get('avg_latency_30d_ms')} ms

[RAW RECENT INTERACTION TRANSCRIPT]:
\"\"\"{customer_data.get('recent_interaction_transcript', 'No transcript available.')}\"\"\"

Generate a comprehensive risk analysis in strict JSON format with these exact keys:
{{
  "customer_id": "{customer_data.get('customer_id')}",
  "risk_level": "Critical" | "High" | "Medium" | "Low",
  "risk_score": <integer from 1 to 100>,
  "urgency_window": "< 24 Hours" | "2-3 Days" | "1-2 Weeks" | "Stable / Monitor",
  "primary_risk_driver": "<Concise 3-6 word label of core issue>",
  "agent_situation_summary": "<2 crisp sentences summarizing the situation and immediate next step for the frontline operations representative>",
  "signal_correlation_rationale": "<2-4 sentences explaining the correlation between the raw transcript and structured telemetry>",
  "prescriptive_action": "<Concrete, department-specific retention playbook>",
  "confidence_score": <float between 0.70 and 0.99>
}}
"""


def _normalize_json_to_list(raw_parsed: Any) -> List[Dict[str, Any]]:
    """Helper to ensure parsed JSON response is always a list of dictionaries."""
    if isinstance(raw_parsed, list):
        return [item for item in raw_parsed if isinstance(item, dict)]
    elif isinstance(raw_parsed, dict):
        for k in ["evaluations", "customers", "data", "results", "candidates"]:
            if k in raw_parsed and isinstance(raw_parsed[k], list):
                return [item for item in raw_parsed[k] if isinstance(item, dict)]
        return [raw_parsed]
    return []


def _normalize_json_to_dict(raw_parsed: Any) -> Dict[str, Any]:
    """Helper to ensure single-customer response is always a single dictionary."""
    if isinstance(raw_parsed, list):
        return raw_parsed[0] if len(raw_parsed) > 0 and isinstance(raw_parsed[0], dict) else {}
    elif isinstance(raw_parsed, dict):
        return raw_parsed
    return {}


class GeminiSignalDetector:
    """
    Direct Google Gemini AI Engine utilizing Micro-Batching (Chunks of 15 records per request)
    with Global Cohort Context Injection and Automatic 429 Retry.
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.5-flash-lite"):
        # If explicitly passed and non-empty, use it; otherwise fall back to environment variable
        if api_key is not None and api_key.strip():
            self.api_key = api_key.strip()
        else:
            self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
            
        self.model_name = model_name or "gemini-3.5-flash-lite"
        self.client = None
        self.last_error = None
        
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 [GEMINI CLIENT INITIALIZED] Model: {self.model_name}")
            except Exception as e:
                self.last_error = str(e)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ [GEMINI INIT ERROR] {e}")

    def is_configured(self) -> bool:
        """Returns True if a valid Gemini client is initialized."""
        return self.client is not None

    def _analyze_chunk_with_retry(self, chunk: List[Dict[str, Any]], cohort_baseline: Dict[str, float], chunk_index: int, max_retries: int = 3) -> List[Dict[str, Any]]:
        """
        Internal worker method to call Gemini API for a single micro-batch chunk of 15 records.
        """
        from google.genai import types

        prompt = build_microbatch_prompt(chunk, cohort_baseline)
        
        for attempt in range(1, max_retries + 1):
            start_time = time.time()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📤 [MICRO-BATCH #{chunk_index}] Sending {len(chunk)} customers to Gemini ({self.model_name}) (Attempt {attempt}/{max_retries})...")
            
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=f"{SYSTEM_PROMPT}\n\n{prompt}",
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )
                
                raw_json = json.loads(response.text)
                parsed_chunk = _normalize_json_to_list(raw_json)
                elapsed_sec = time.time() - start_time
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 📥 [MICRO-BATCH #{chunk_index} SUCCESS] Evaluated {len(parsed_chunk)} customers in {elapsed_sec:.2f}s!")
                return parsed_chunk
                
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    wait_sec = 4.0 * attempt
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏳ [QUOTA WAIT for Chunk #{chunk_index}] Rate limit encountered. Backing off {wait_sec:.1f}s before retry...")
                    time.sleep(wait_sec)
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ [CHUNK #{chunk_index} ERROR]: {e}")
                    if attempt == max_retries:
                        raise e
                    time.sleep(2.0)
                    
        raise RuntimeError(f"Micro-batch #{chunk_index} failed after {max_retries} attempts.")

    def analyze_batch(self, candidate_records: List[Dict[str, Any]], chunk_size: int = 15, max_workers: int = 3) -> Dict[str, Dict[str, Any]]:
        """
        Processes ALL candidate customer records using Micro-Batching (chunks of 15, max_workers=3).
        Calculates Global Cohort Baseline averages across all records, and executes parallel requests safely under 5 RPM.
        """
        if not self.client:
            raise ValueError("Gemini API key is not configured. Please provide a valid key.")

        count = len(candidate_records)
        if count == 0:
            return {}

        start_time = time.time()
        timestamp = datetime.now().strftime('%H:%M:%S')

        # 1. Calculate Global Cohort Baseline Averages across ALL candidate records
        avg_latency = sum(float(r.get("avg_latency_30d_ms", 0)) for r in candidate_records) / count
        avg_outflow = sum(float(r.get("net_outflow_30d_inr", 0)) for r in candidate_records) / count
        avg_volume_change = sum(float(r.get("trading_volume_change_30d_pct", 0)) for r in candidate_records) / count

        cohort_baseline = {
            "avg_latency_ms": round(avg_latency, 1),
            "avg_outflow_inr": round(avg_outflow, 2),
            "avg_volume_change_pct": round(avg_volume_change, 1)
        }

        # 2. Split candidate records into chunks of 15 records
        chunks = [candidate_records[i:i + chunk_size] for i in range(0, count, chunk_size)]
        num_chunks = len(chunks)

        print(f"\n[{timestamp}] 🚀 [MICRO-BATCH BATCH STARTED] Partitioned {count} candidates into {num_chunks} chunks (max {chunk_size}/chunk). Executing with {min(num_chunks, max_workers)} parallel workers (Quota safe <= 5 RPM)...")
        print(f"[{timestamp}] 📊 [GLOBAL COHORT BASELINE INJECTED] Latency: {avg_latency:.1f}ms | Outflow: ₹{avg_outflow:,.0f} | Vol Change: {avg_volume_change:.1f}%")

        results: Dict[str, Dict[str, Any]] = {}

        # 3. Submit chunks concurrently across thread pool (max 3 workers)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_chunk_idx = {
                executor.submit(self._analyze_chunk_with_retry, chunk, cohort_baseline, idx + 1): idx + 1
                for idx, chunk in enumerate(chunks)
            }

            for future in as_completed(future_to_chunk_idx):
                chunk_idx = future_to_chunk_idx[future]
                try:
                    chunk_evaluations = future.result()
                    for item in chunk_evaluations:
                        cid = item.get("customer_id")
                        if cid:
                            item["is_live_ai"] = True
                            item["model_used"] = self.model_name
                            item["provider_used"] = f"Google Gemini API ({self.model_name} Micro-Batch)"
                            results[cid] = item
                except Exception as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ [MICRO-BATCH #{chunk_idx} FAILED]: {e}")
                    self.last_error = str(e)

        total_sec = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ [MICRO-BATCH COMPLETED] Evaluated {len(results)}/{count} customers across {num_chunks} chunks in {total_sec:.2f}s total!")
        return results

    def analyze_single(self, customer_data: Dict[str, Any], cohort_baseline: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Processes a single customer on-demand with Gemini API.
        """
        if not self.client:
            raise ValueError("Gemini API key is not configured.")

        from google.genai import types

        start_time = time.time()
        cust_id = customer_data.get("customer_id", "UNKNOWN")
        cust_name = customer_data.get("customer_name", "Anonymous")
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ⚡ [SINGLE AI CALL] Ingesting {cust_id} ({cust_name}) into Gemini API ({self.model_name})...")
        
        prompt = build_single_analysis_prompt(customer_data, cohort_baseline=cohort_baseline)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"{SYSTEM_PROMPT}\n\n{prompt}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                )
            )
            
            raw_json = json.loads(response.text)
            result = _normalize_json_to_dict(raw_json)
            elapsed_ms = (time.time() - start_time) * 1000
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ [SINGLE AI SUCCESS in {elapsed_ms:.0f}ms] Risk: {result.get('risk_level')} ({result.get('risk_score')}/100) | Driver: {result.get('primary_risk_driver')}")
            
            result["is_live_ai"] = True
            result["model_used"] = self.model_name
            result["provider_used"] = f"Google Gemini API ({self.model_name})"
            result["latency_ms"] = round(elapsed_ms, 1)
            result["raw_response_text"] = response.text
            return result
            
        except Exception as e:
            self.last_error = str(e)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ [SINGLE AI CALL FAILED for {cust_id}]: {e}")
            raise e
