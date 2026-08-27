# Intelligent Customer Signal Detector (POC)
**Proactive Multi-Signal Early Warning & Retention Intelligence for Wealth-Tech Operations**

---

## Executive Overview & Problem Context
Customer operations in FinTech and Wealth-Tech platforms traditionally operate on a **reactive paradigm**:
- Customer support only responds when an explicit complaint ticket or account cancellation request is lodged.
- By that time, the opportunity to retain the user or prevent capital flight has often already passed.
- Relevant warning signals exist across fragmented, siloed data sources:
  - *Trading Telemetry*: Order routing latency, failed WebSocket connections, execution slippage, volume contraction.
  - *Financial Telemetry*: Sudden liquid capital withdrawals, custodial balance depletion.
  - *Customer Interactions*: Subtle tone changes, passive-aggressive remarks, inquiries regarding transfer limits or account closure procedures.

### The Solution
The **Intelligent Customer Signal Detector** is an AI prototype that continuously monitors and correlates structured telemetry with unstructured chat transcripts. Operating as a **Two-Stage Funnel**, it proactively surfaces at-risk customers, identifies the root cause of friction, and prescribes department-specific operational retention playbooks before formal escalation occurs.

---

## System Architecture: The Two-Stage Funnel

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  RAW MULTI-SOURCE INGESTION                                  │
│  • Trading Telemetry (Volume Δ, Latency, Failed Orders)  • Financial Outflows & AUM         │
│  • Customer Support Logs & Raw Multi-turn Transcripts                                      │
└──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                         STAGE 1: DETERMINISTIC FUNNEL & ANOMALY FILTER                      │
│  • High-throughput statistical screening across 1,000,000+ accounts                         │
│  • Filters out ~50-60% Healthy Cohort to eliminate unnecessary token & compute cost         │
│  • Computes baseline Telemetry Anomaly Score (0-100) & multi-signal trigger count           │
└──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                               │ Candidate At-Risk Cohort Flagged
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                         STAGE 2: COGNITIVE LLM SYNTHESIZER (GEMINI API)                     │
│  • Multi-Signal Reasoning: Correlates unstructured transcripts with telemetry anomalies    │
│  • Identifies 'Silent Churn' (subtle language + large outflows) vs 'False Alarms' (bugs/UX)│
│  • Generates Structured JSON: Root-Cause Rationale + Prescriptive Next Action + Urgency     │
└──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              OPERATIONAL ACTION & COMMAND CENTER                            │
│  • Prioritized Queue for Customer Ops & Relationship Managers (RMs)                         │
│  • One-Click Retention Playbooks (Fee Waivers, RM Calls, Risk Desk Slippage Audits)        │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Differentiator: Cognitive Synthesis vs. Naive Sentiment

Traditional sentiment analysis models fail when applied to enterprise FinTech operations:
1. **The Polite Silent Churner:** A customer with a ₹3.4 Crore portfolio experiencing 840ms latency politely inquires about daily RTGS transfer limits while refusing to open more tickets. Naive sentiment scores this as *"Neutral/Polite"*, missing an imminent **₹95 Lakh capital flight**.
2. **The Passive Power User:** A loyal trader submitting 4 tickets with UX suggestions and charting feature requests is falsely flagged by naive rule-based filters (*"Tickets >= 4"*), causing ops teams to waste retention resources on an already-delighted customer.

Our Stage-2 Cognitive Synthesizer uses **Google Gemini 2.5 Flash / 1.5 Flash** to perform true multi-signal correlation:

```json
{
  "customer_id": "CUST-1001",
  "risk_level": "Critical",
  "risk_score": 96,
  "urgency_window": "< 24 Hours",
  "primary_risk_driver": "Silent HNI Capital Flight",
  "signal_correlation_rationale": "Customer experienced severe platform latency (840ms) during morning market open, resulting in an 82% trading collapse. Unstructured transcript reveals polite refusal of support tickets paired with an inquiry on RTGS transfer limits, directly explaining the ₹95.0 Lakhs capital drainage.",
  "prescriptive_action": "Urgent White-Glove intervention: Assign Principal Relationship Manager for an executive briefing and custom custodial fee tier within 2 hours.",
  "confidence_score": 0.98
}
```

---

## Curated Evaluation Matrix ("Golden Records")

| Customer ID | Name | Account Tier | Telemetry Anomalies | Interaction Transcript Signal | Naive Analysis Failure | Stage-2 Cognitive Synthesis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`CUST-1001`** | Vikramaditya Singhania | **HNI** (₹3.4 Cr) | -82.5% Vol, ₹95L Outflow, 840ms Latency | Polite refusal of ticket; asking for RTGS withdrawal limits | Ignores (only 1 ticket logged) | **Critical Silent Churn**: Assign Principal RM for White-Glove callback within 2 hours. |
| **`CUST-1002`** | Rohan Deshmukh | **Pro Trader** (₹52L) | 14 Failed Orders, 5 Tickets, ₹24L Outflow | ₹65k slippage loss during expiry; threat to move algo desk to Zerodha | Flags as routine support ticket | **Critical Tech Slippage**: Immediate Risk Desk compensation audit before algo desk migrates. |
| **`CUST-1003`** | Priyanka Sen | **Standard** (₹4.2L) | -78.0% Vol, ₹3.1L Outflow | Polite request for Tax P&L CSV and account deactivation checklist | Scored as 'Positive/Polite' | **High Competitor Churn**: Consolidating to zero-brokerage platform; dispatch options tier upgrade. |
| **`CUST-1004`** | Karthik Ramanathan | **Standard** (₹8.5L) | 7 Failed Orders, 620ms Latency | Biometric login freezes on v4.2 update; stopped intraday trading | Treated as isolated mobile ticket | **High App Release Friction**: Provide direct QA hotfix build and ₹1,000 goodwill voucher. |
| **`CUST-1005`** | Aditya Verma | **Pro Trader** (₹78L) | +22.0% Vol, ₹0 Outflow, 4 Tickets | Enthusiastic feedback on charting hotkeys and Greek payoff graphs | False Alarm (flagged on ticket count) | **Low Risk (Loyal Advocate)**: Route suggestions to Product UX and invite to Beta Testing cohort. |

---

## Installation & Setup Instructions

### 1. Clone & Environment Setup
```bash
git clone <repo_url>
cd Intelligent_Customer_Signal_Detector

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key (Optional)
Copy the example environment configuration:
```bash
cp .env.example .env
```
Edit `.env` and add your **free Google Gemini API Key** from [Google AI Studio (aistudio.google.com)](https://aistudio.google.com/):
```env
GEMINI_API_KEY=your_gemini_api_key_here
LLM_PROVIDER=gemini
```
> **Note:** If no API key is provided, the application automatically runs in **Built-in High-Precision Cognitive Simulation Mode**, allowing seamless evaluation with zero setup friction.

### 3. Generate Mock Data (Optional)
```bash
python3 src/generate_data.py
```

### 4. Launch the Streamlit Operations Command Center
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## Project Structure
```
Intelligent_Customer_Signal_Detector/
├── data/
│   └── customers.csv              # 75 synthetic FinTech profiles with Golden Records
├── src/
│   ├── generate_data.py           # Procedural data generator with realistic distributions
│   ├── data_loader.py             # Schema validation, Stage-1 telemetry anomaly scoring
│   └── llm_reasoning.py           # Gemini 2.5 Flash / OpenAI multi-signal cognitive synthesizer
├── docs/
│   └── 5_SLIDE_PRESENTATION_DECK.md # Presentation script for client pitch
├── app.py                         # Interactive Streamlit operations command center
├── requirements.txt               # Dependencies (streamlit, plotly, google-genai, etc.)
├── .env.example                   # Environment configuration template
└── README.md                      # Complete system documentation
```

---

## Technology Stack
- **Language**: Python 3.12
- **Core Processing & Telemetry Scoring**: Python Data Structures / Pandas
- **AI Synthesis Engine**: Google Gemini API (`google-genai` SDK, `gemini-3.6-flash` / `gemini-1.5-flash`)
- **Dashboard & Operations UI**: Streamlit
- **Visualizations**: Plotly Express & Plotly Graph Objects

---

## Assumptions & Scalability Design Notes
1. **30-Day Aggregation Window**: In a live production environment, streaming telemetry (Kafka/Flink) feeds a real-time feature store (Feast/Redis) that calculates 30-day sliding window metrics.
2. **Cost-Efficient Two-Stage Architecture**: Running deep LLM reasoning on 100% of platform traffic at 10M scale is economically unfeasible. Stage 1 reduces compute volume by ~50-60%, routing only genuine anomaly candidates to Stage 2.
3. **Data Privacy & Redaction**: Production deployments integrate a PII scrubbing layer (e.g. Presidio) before forwarding transcripts to the LLM.
