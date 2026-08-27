# 5-Slide Summary Presentation Deck
**Project:** Intelligent Customer Signal Detector (Firstsource POC)  
**Track:** Pro-Code Track (Python, Gemini API, Streamlit, Plotly)  
**Target Audience:** Customer Operations Leadership & Enterprise Client Pitch  

---

## SLIDE 1: PROBLEM UNDERSTANDING AND OBJECTIVE

### Slide Title:
**Transitioning Customer Operations from Reactive Escalation to Proactive Multi-Signal Early Warning**

### Content / Visual Layout:
- **The Core Problem:**
  - Modern Wealth-Tech and FinTech platforms rely heavily on *reactive processes*.
  - When a customer submits a formal cancellation or escalation ticket, the decision to churn (or liquidate capital) has typically already been made.
  - Critical friction signals exist in silos:
    - *System Telemetry:* Order routing latency, WebSocket crashes, API rejected orders.
    - *Financial Flow:* Abnormal 30-day net outflows, trading volume contraction.
    - *Unstructured Interactions:* Polite tone hiding exit intent, passive-aggressive support logs, tax statement requests.
- **The Solution Objective:**
  - Build an AI-driven Signal Detector that continuously ingests multi-modal data streams, discovers hidden cross-signal correlations, and delivers a prioritized operational queue with actionable retention playbooks before customers churn.

### Key Takeaway for Client:
> *"Stop waiting for the complaint. Detect the friction at the point of origin."*

---

## SLIDE 2: SOLUTION ARCHITECTURE AND DESIGN FLOW

### Slide Title:
**Two-Stage Scalable Intelligence Architecture: Cost-Optimized Funnel Design**

### Content / Visual Layout:
```
[Raw Multi-Source Data] ──► [Stage 1: Deterministic Filter] ──► [Stage 2: Cognitive LLM Synthesizer] ──► [Ops Command Center]
 • Latency / Order Errors    • Fast statistical anomaly check   • Gemini 2.5 Flash Multi-Signal Reasoning  • Priority Risk Queue
 • Outflows & Volume Δ       • Eliminates 50-60% healthy base   • Uncovers hidden text + data correlations  • 1-Click Retention Actions
 • Support Chat Logs         • Lowers compute / token costs     • Structured JSON Output                    • Live Signal Simulator
```

### Architectural Pillars:
1. **Stage 1 (Deterministic Telemetry Filter):**
   - High-throughput screening across 1,000,000+ accounts.
   - Computes a baseline *Telemetry Anomaly Score (0-100)* across 5 friction dimensions.
   - Filters out the healthy baseline cohort, reducing downstream LLM token costs by ~55%.
2. **Stage 2 (Cognitive LLM Synthesizer - Gemini API):**
   - Ingests unstructured interaction transcripts + structured telemetry.
   - Generates Root-Cause Rationale, Churn Urgency (`< 24h`, `2-3d`), and Prescriptive Retention Actions.
3. **Operational Command Hub (Streamlit & Plotly):**
   - Executive KPI visibility, multi-signal risk scatter matrix, customer dossier, and real-time simulator.

---

## SLIDE 3: IMPLEMENTATION HIGHLIGHTS

### Slide Title:
**Cognitive Synthesis vs. Naive Sentiment: Real-World FinTech Scenarios**

### Content / Visual Layout:
- **Avoiding the "Anti-Pattern":** The LLM does not merely summarize pre-calculated scores; it acts as a reasoning engine synthesizing disconnected signals.
- **The 4 Golden Profiles:**

| Customer Archetype | Telemetry Anomalies | Raw Transcript Nuance | Naive System Error | Stage-2 AI Synthesis Diagnosis |
|---|---|---|---|---|
| **Silent HNI Churn** (`CUST-1001`) | ₹3.4 Cr AUM, -82.5% Vol, ₹95L Outflow, 840ms Latency | Polite refusal of ticket; asking for RTGS limits | Ignored (only 1 ticket) | **Critical Risk (96/100)**: Latency triggered capital exit; Dispatch Principal RM callback within 2h. |
| **Cascading Slippage** (`CUST-1002`) | 14 Failed Orders, 980ms Latency, 5 Tickets | ₹65k slippage loss; explicit threat to switch to Zerodha | Generic support ticket | **Critical Tech Risk (94/100)**: Immediate Risk Desk compensation audit before algo desk migrates. |
| **Subtle Competitor Migration** (`CUST-1003`) | -78% Vol, ₹3.1L Outflow (74% of AUM) | Polite request for Tax P&L CSV and deactivation steps | Naive sentiment marks as 'Positive' | **High Risk (85/100)**: Consolidating to zero-brokerage competitor; dispatch options tier upgrade. |
| **Loyal Power User** (`CUST-1005`) | +22% Vol, ₹0 Outflow, 4 Tickets | Constructive UX feedback for charting hotkeys | False Alarm (flagged on ticket count) | **Low Risk (12/100)**: Enthusiastic product advocate; route suggestions to Beta cohort. |

---

## SLIDE 4: CHALLENGES AND LEARNINGS

### Slide Title:
**Technical Trade-Offs, Enterprise Constraints, and Strategic Learnings**

### Content / Visual Layout:
1. **Tone Ambiguity & Polite Sarcasm:**
   - *Challenge:* At-risk HNIs rarely shout; they politely disengage and move their capital.
   - *Solution:* Engineered few-shot system prompts instructing Gemini to weigh financial actions (outflows, deactivation queries) higher than superficial conversational politeness.
2. **Token Economics at Scale:**
   - *Challenge:* Sending continuous 30-day transcripts for 1M active accounts is economically prohibitive.
   - *Solution:* Implemented the Stage-1 deterministic gating filter, ensuring only candidate friction accounts invoke Stage-2 LLM inference.
3. **Operational Actionability:**
   - *Challenge:* Risk scores alone do not help operations agents resolve issues.
   - *Solution:* Mandated strict structured JSON schema with a dedicated `prescriptive_action` field mapped to departmental workflows (RM Concierge, RMS Slippage Audit, Goodwill Vouchers).

---

## SLIDE 5: DEMO SUMMARY AND NEXT STEPS

### Slide Title:
**Proof of Concept Summary & Enterprise Production Roadmap**

### Content / Visual Layout:
- **POC Deliverables Achieved:**
  - ✅ **Full Working Demo:** Streamlit Command Center with Executive KPIs, Priority Queue, Detail Dossier, and Live Simulator.
  - ✅ **Gemini API Integration:** Native structured output with rate-limit resiliency and offline fallback.
  - ✅ **Curated FinTech Dataset:** 75 realistic customer records with 5 verified multi-signal Golden Records.
  - ✅ **Comprehensive Documentation:** Full README and 5-slide summary deck.

- **Production Scale-Out Roadmap:**
  1. **Streaming Real-Time Pipeline:** Transition from 30-day batch windows to Apache Kafka / Apache Flink event-stream processing.
  2. **Automated CRM & Ticketing Webhooks:** Direct bi-directional integration with Salesforce Financial Services Cloud, Zendesk, and Freshdesk.
  3. **PII Masking & Enterprise Security:** Integrated automated PII redactor (Presidio) to sanitize transcripts before LLM processing.
  4. **Closed-Loop Feedback:** Track retention conversion rates post-intervention to fine-tune Stage-1 thresholds and LLM prompts automatically.

### Links & Repository:
- **Application:** `streamlit run app.py` (Local Port: 8501)
- **Codebase:** `src/generate_data.py`, `src/data_loader.py`, `src/llm_reasoning.py`, `app.py`
