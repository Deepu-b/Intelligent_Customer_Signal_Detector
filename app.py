"""
Intelligent Customer Signal Detector - Executive & Operations Command Center
Built for Firstsource FinTech / Wealth-Tech POC

High-Readability, Ultra-Fast Enterprise UI:
- Fully Integrated Master Panels: Headings are directly part of the bounded tables/panels below
- Instant Customer Profile Switching: Sub-millisecond response with zero unmounting or blank panels
- 5-Item Pagination: Vertically balanced layout matching the right profile height
- Pixel-Perfect Top Action Ribbon (Connected Status and Run Batch Button have exact identical heights)
- Symmetrical, balanced dual-column layout with clean straight dividing lines
- Enhanced typography scale (15.5px bold tabs, 18px panel titles, crisp hierarchy)
- Uniform equal-height Top KPI metric boxes with compact Stage-1 info popover
- Clean, focused diagnostic view
- Single Enclosed Card Box for each candidate with simple labels
- Plain-text API Key Input (No password prompts, clean empty field, zero overlapping text)
- Sleek, Compact Tech-Blue Action Buttons
- Micro-Batching in chunks of 15 candidate records with Global Cohort Baseline
- Modern Streamlit width="stretch" syntax
"""

import os
import sys
import json
import time
import random
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import CustomerDataLoader, CustomerRecord
from src.llm_reasoning import GeminiSignalDetector
from src.generate_data import regenerate_dataset_file

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Intelligent Customer Signal Detector | Firstsource POC",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Spacious, High-Contrast Enterprise Card & Tech-Blue Button Styling with Smooth Animations
st.markdown("""
<style>
    /* Global clean typography scale */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #f1f5f9;
    }
    
    /* Prominent Tab Navigation Typography */
    button[data-baseweb="tab"] {
        font-size: 15.5px !important;
        font-weight: 700 !important;
        color: #94a3b8 !important;
        padding: 10px 18px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }

    /* Headings Scale */
    h1 {
        font-size: 28px !important;
        font-weight: 800 !important;
        letter-spacing: -0.4px !important;
    }
    h2, h3 {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.2px !important;
        margin: 0 !important;
    }
    
    .section-caption {
        font-size: 13px;
        color: #94a3b8;
    }
    
    /* Clean Straight Dividing Lines */
    .section-divider {
        border: 0;
        border-top: 1px solid #334155;
        margin: 12px 0 14px 0;
    }
    
    /* Top Action Ribbon - Pixel-Perfect 42px Equal Height */
    .action-ribbon-status {
        background: rgba(14, 165, 233, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 8px;
        height: 42px;
        display: flex;
        align-items: center;
        padding: 0 16px;
        font-size: 13.5px;
        font-weight: 600;
        color: #bae6fd;
    }
    
    /* Tech-Blue Primary Buttons */
    button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        border: 1px solid #3b82f6 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        border-radius: 8px !important;
        min-height: 42px !important;
        height: 42px !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
        border-color: #60a5fa !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.45) !important;
    }

    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 4px;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    
    /* Uniform equal-height styling for the Top 4 KPI metric cards */
    div[data-testid="stHorizontalBlock"]:has(.kpi-card-marker) [data-testid="stVerticalBlockBorderWrapper"] {
        min-height: 120px !important;
        height: 120px !important;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    /* Compact popover button inside the Stage-1 KPI card */
    div[data-testid="stHorizontalBlock"]:has(.kpi-card-marker) button[kind="secondary"] {
        padding: 0px 6px !important;
        min-height: 22px !important;
        height: 22px !important;
        font-size: 11px !important;
        line-height: 1 !important;
        margin-top: -2px !important;
    }
    
    /* Action ribbon popover button */
    div[data-testid="stHorizontalBlock"]:has(.ribbon-marker) button[kind="secondary"] {
        min-height: 42px !important;
        height: 42px !important;
        border-radius: 8px !important;
    }
    
    /* Single run button in header */
    button[key*="dhead_run_ai"] {
        min-height: 38px !important;
        height: 38px !important;
    }

    /* Risk Badges */
    .badge-critical {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 14px;
        font-weight: 800;
        font-size: 11.5px;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
    }
    .badge-high {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 14px;
        font-weight: 800;
        font-size: 11.5px;
        box-shadow: 0 2px 8px rgba(249, 115, 22, 0.4);
    }
    .badge-medium {
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
        color: #0f172a;
        padding: 4px 12px;
        border-radius: 14px;
        font-weight: 800;
        font-size: 11.5px;
        box-shadow: 0 2px 8px rgba(234, 179, 8, 0.4);
    }
    .badge-low {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 14px;
        font-weight: 800;
        font-size: 11.5px;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.4);
    }
    .badge-pending {
        background: #334155;
        color: #cbd5e1;
        padding: 4px 12px;
        border-radius: 14px;
        font-weight: 700;
        font-size: 11.5px;
        border: 1px solid #475569;
    }

    /* Telemetry Pills */
    .card-telemetry-pill {
        display: inline-block;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 4px 9px;
        margin-right: 6px;
        margin-top: 4px;
        font-size: 12.5px;
        color: #e2e8f0;
    }
    .card-driver-alert {
        font-size: 13px;
        font-weight: 700;
        color: #f87171;
        margin-top: 8px;
        line-height: 1.4;
    }
    .card-agent-brief {
        background: rgba(56, 189, 248, 0.1);
        border-left: 3px solid #38bdf8;
        border-radius: 6px;
        padding: 8px 12px;
        margin-top: 8px;
        font-size: 12px;
        color: #bae6fd;
        line-height: 1.5;
    }

    /* Detailed Profile Boxes */
    .agent-brief-box {
        background: rgba(14, 165, 233, 0.12);
        border-left: 4px solid #38bdf8;
        border-radius: 8px;
        padding: 14px 16px;
        margin: 10px 0 14px 0;
        font-size: 14px;
        color: #f8fafc;
        line-height: 1.6;
    }
    .rationale-box {
        background: rgba(30, 41, 59, 0.85);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 14px 16px;
        margin: 10px 0 14px 0;
        font-size: 13.5px;
        color: #f1f5f9;
        line-height: 1.6;
    }
    .playbook-box {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        padding: 14px 16px;
        margin: 10px 0 14px 0;
        font-size: 13.5px;
        color: #f0fdf4;
        line-height: 1.6;
    }
    .transcript-box {
        background-color: #020617;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 14px 16px;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 13px;
        color: #cbd5e1;
        line-height: 1.6;
        max-height: 220px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "dataset_version" not in st.session_state:
    st.session_state.dataset_version = 1

if "ai_results" not in st.session_state:
    st.session_state.ai_results = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = 1

# Load key into background memory from .env if available, but NEVER pre-fill in input field
env_key = os.getenv("GEMINI_API_KEY", "").strip()
if "applied_api_key" not in st.session_state:
    st.session_state.applied_api_key = env_key

if "applied_model" not in st.session_state:
    st.session_state.applied_model = "gemini-3.5-flash-lite"

if "applied_tiers" not in st.session_state:
    st.session_state.applied_tiers = ["HNI", "Pro Trader", "Standard"]

if "applied_min_portfolio" not in st.session_state:
    st.session_state.applied_min_portfolio = 100000.0


# ---------------------------------------------------------
# Sidebar Configuration Form
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## System Control Hub")
    
    st.markdown("---")
    st.subheader("Cohort Generator")
    if st.button("Randomize Customer Cohort", help="Generates a freshly randomized synthetic customer cohort.", width="stretch"):
        new_seed = random.randint(100, 999999)
        regenerate_dataset_file(seed=new_seed)
        st.session_state.dataset_version += 1
        st.session_state.ai_results.clear()
        st.session_state.current_page = 1
        st.session_state.pop("selected_customer_id", None)
        st.cache_resource.clear()
        st.toast("Customer cohort randomized with fresh signals!")
        st.rerun()

    st.markdown("---")
    st.subheader("Gemini AI Configuration")
    
    with st.form(key="sidebar_controls_form"):
        has_active_key = bool(st.session_state.applied_api_key)
        
        # Standard text input (not password) so Chrome does NOT ask to save/update passwords
        form_api_key = st.text_input(
            "Google Gemini API Key",
            value="",  # Completely blank by default, zero overlapping placeholders
            help="Paste your free API key from Google AI Studio (aistudio.google.com)."
        )
        
        if has_active_key:
            masked = f"...{st.session_state.applied_api_key[-4:]}" if len(st.session_state.applied_api_key) >= 4 else "Active"
            st.caption(f"Status: API Key Active in Memory (`{masked}`)")
        else:
            st.caption("Status: No API Key Configured")
        
        form_model = st.selectbox(
            "Gemini Model",
            ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.6-flash"],
            index=0
        )
        
        form_tiers = st.multiselect(
            "Filter Account Tier",
            ["HNI", "Pro Trader", "Standard"],
            default=st.session_state.applied_tiers
        )
        
        form_min_portfolio = st.slider(
            "Min Portfolio (₹ Lakhs)",
            min_value=1,
            max_value=300,
            value=int(st.session_state.applied_min_portfolio / 100000)
        ) * 100000

        submit_btn = st.form_submit_button("Apply Configurations", type="primary", width="stretch")

        if submit_btn:
            # Only override API key if user typed a new key into the box
            if form_api_key.strip():
                st.session_state.applied_api_key = form_api_key.strip()
            st.session_state.applied_model = form_model
            st.session_state.applied_tiers = form_tiers if form_tiers else ["HNI", "Pro Trader", "Standard"]
            st.session_state.applied_min_portfolio = float(form_min_portfolio)
            st.session_state.current_page = 1
            st.toast("Configurations applied!")
            st.rerun()

    if st.button("Clear AI Results Cache", width="stretch"):
        st.session_state.ai_results.clear()
        st.toast("AI analysis cache cleared.")
        st.rerun()

    st.markdown("---")


# ---------------------------------------------------------
# Load Data & Initialize AI Engine (Cached for instant execution)
# ---------------------------------------------------------
@st.cache_resource
def get_data_loader(version: int):
    return CustomerDataLoader()

loader = get_data_loader(st.session_state.dataset_version)
all_records = loader.get_all_records()
candidates = loader.get_candidates_for_llm()
summary_metrics = loader.get_summary_metrics()

# Initialize Gemini Detector with background active key
gemini_detector = GeminiSignalDetector(
    api_key=st.session_state.applied_api_key,
    model_name=st.session_state.applied_model
)

# Apply Tier & Portfolio Filters
scoped_candidates = [
    r for r in candidates
    if r.account_tier in st.session_state.applied_tiers and r.portfolio_value_inr >= st.session_state.applied_min_portfolio
]

# Deterministic Multi-Variate Sorting:
# Evaluates (risk_level_weight, risk_score, portfolio_value_inr, net_outflow_30d_inr)
RISK_LEVEL_WEIGHTS = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}

def get_multivariate_sort_key(rec: CustomerRecord):
    ai_data = st.session_state.ai_results.get(rec.customer_id)
    if ai_data:
        risk_level_str = ai_data.get("risk_level", "Low")
        risk_weight = RISK_LEVEL_WEIGHTS.get(risk_level_str, 1)
        risk_score = float(ai_data.get("risk_score", 0))
    else:
        # Fallback to Stage-1 Telemetry weight and score before AI execution
        risk_weight = 1
        risk_score = float(rec.stage1_telemetry_score)
        
    portfolio = float(rec.portfolio_value_inr)
    outflow = float(rec.net_outflow_30d_inr)
    return (risk_weight, risk_score, portfolio, outflow)

sorted_candidates = sorted(scoped_candidates, key=get_multivariate_sort_key, reverse=True)

# Dynamically default selected customer to the #1 HIGHEST PRIORITY customer
if sorted_candidates:
    valid_ids = [r.customer_id for r in sorted_candidates]
    if "selected_customer_id" not in st.session_state or st.session_state.selected_customer_id not in valid_ids:
        st.session_state.selected_customer_id = sorted_candidates[0].customer_id

# Pagination Setup: 5 accounts per page for optimal vertical balance & fast responsiveness
PAGE_SIZE = 5
total_candidates_count = len(sorted_candidates)
total_pages = max(1, (total_candidates_count + PAGE_SIZE - 1) // PAGE_SIZE)

# Ensure current page is valid
if st.session_state.current_page > total_pages:
    st.session_state.current_page = 1
elif st.session_state.current_page < 1:
    st.session_state.current_page = 1

start_idx = (st.session_state.current_page - 1) * PAGE_SIZE
end_idx = min(start_idx + PAGE_SIZE, total_candidates_count)
paged_candidates = sorted_candidates[start_idx:end_idx]


# ---------------------------------------------------------
# Header & Executive KPI Ribbon
# ---------------------------------------------------------
st.title("Intelligent Customer Signal Detector")
st.markdown("**Proactive Multi-Signal Early Warning & Retention Intelligence for Wealth-Tech Operations**")

col_k1, col_k2, col_k3, col_k4 = st.columns(4)

with col_k1:
    with st.container(border=True):
        st.markdown('<span class="kpi-card-marker"></span><div class="metric-label">Monitored Accounts</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{summary_metrics["total_monitored_customers"]}</div>', unsafe_allow_html=True)
        st.caption("Total Custodial Accounts")

with col_k2:
    with st.container(border=True):
        k2_head1, k2_head2 = st.columns([3.8, 1.0])
        with k2_head1:
            st.markdown('<span class="kpi-card-marker"></span><div class="metric-label">Stage-1 Candidates</div>', unsafe_allow_html=True)
        with k2_head2:
            with st.popover("ℹ️", help="Learn about Stage-1 Heuristic Filtering"):
                st.markdown("""
                **Stage-1 Heuristic Screening**
                
                - **Automated Filter:** Evaluates 100% of accounts across 5 operational rules:
                  - Latency > 300ms
                  - Trading Volume Drop > 30%
                  - 30d Capital Outflow > 20% AUM
                  - Failed Orders ≥ 3
                  - Support Tickets ≥ 2
                - **Efficiency:** Accounts triggering 2+ rules receive a baseline score (0–100). This filters out ~60% of healthy accounts so AI only processes at-risk profiles cost-effectively.
                """)
        st.markdown(f'<div class="metric-value" style="color: #fb923c;">{summary_metrics["stage1_candidates_count"]} <span style="font-size: 15px; color: #94a3b8;">({summary_metrics["stage1_candidate_pct"]}%)</span></div>', unsafe_allow_html=True)
        st.caption("Rule-Based Anomaly Screening")

with col_k3:
    with st.container(border=True):
        st.markdown('<span class="kpi-card-marker"></span><div class="metric-label">Total Platform AUM</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">₹{summary_metrics["total_aum_inr"]/10000000:.2f} Cr</div>', unsafe_allow_html=True)
        st.caption("Assets Under Custody")

with col_k4:
    ai_evaluated_count = len([c for c in scoped_candidates if c.customer_id in st.session_state.ai_results])
    with st.container(border=True):
        st.markdown('<span class="kpi-card-marker"></span><div class="metric-label">AI Evaluated</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value" style="color: #38bdf8;">{ai_evaluated_count} / {len(scoped_candidates)}</div>', unsafe_allow_html=True)
        st.caption(f"At-Risk AUM: ₹{summary_metrics['at_risk_portfolio_inr']/10000000:.2f} Cr")

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Tabs Navigation
# ---------------------------------------------------------
tab_queue, tab_simulator, tab_architecture = st.tabs([
    "Prioritized Queue & AI Deep Dive",
    "Live 'What-If' Signal Simulator",
    "Two-Stage Funnel Architecture"
])


# ---------------------------------------------------------
# TAB 1: Prioritized Queue & Deep Dive
# ---------------------------------------------------------
with tab_queue:
    # Top Action Ribbon - Pixel-Perfect Equal Height Layout
    if gemini_detector.is_configured():
        col_b1, col_b2, col_b3 = st.columns([1.7, 1.4, 0.22])
        with col_b1:
            st.markdown(f"""
            <div class="action-ribbon-status">
                <span class="ribbon-marker"></span>Connected :  <b>{st.session_state.applied_model}</b>
            </div>
            """, unsafe_allow_html=True)
        with col_b2:
            if st.button("Run Batch AI insights", type="primary", width="stretch", help="Dispatches all candidate accounts in parallel batches of 15 to Gemini AI."):
                with st.spinner(f"Synthesizing all {len(scoped_candidates)} candidate profiles"):
                    try:
                        batch_payload = [r.to_dict() for r in scoped_candidates]
                        batch_res = gemini_detector.analyze_batch(batch_payload, chunk_size=15, max_workers=3)
                        st.session_state.ai_results.update(batch_res)
                        
                        # Re-sort and set selected customer to the new #1 highest risk account
                        updated_sorted = sorted(scoped_candidates, key=get_multivariate_sort_key, reverse=True)
                        if updated_sorted:
                            st.session_state.selected_customer_id = updated_sorted[0].customer_id
                            st.session_state.current_page = 1
                            
                        st.toast("Gemini AI synthesized all candidate accounts!")
                        st.rerun()
                    except Exception as err:
                        st.error(f"Gemini API Error: {err}")
        with col_b3:
            with st.popover("ℹ️", help="Click to see what happens in a Batch AI Run"):
                st.markdown("""
                ### What Happens in Batch AI Runs?
                
                - **Parallel Dispatch:** All flagged candidate accounts are processed concurrently in micro-batches of 15.
                - **Multi-Signal Synthesis:** Gemini compares each customer's order latency, volume drop, and outflows against overall platform averages, and correlates them with raw support chat logs.
                - **Actionable Output:** Produces standardized risk scores (0–100), root-cause diagnostic labels, and frontline retention playbooks for operations teams.
                """)
    else:
        st.warning("No Gemini API Key Configured. Stage-1 Telemetry Screening is active. To enable AI Cognitive Synthesis, paste your free key in the sidebar.")

    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.12, 1.28])
    
    # Left Column: Integrated Master Panel for Customer Queue
    with col_left:
        with st.container(border=True):
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 2px;">
                <span style="font-size: 18px; font-weight: 800; color: #ffffff;">Prioritized Customer Queue</span>
                <span class="section-caption">Showing {start_idx+1}–{end_idx} of {total_candidates_count}</span>
            </div>
            <div class="section-caption">Ranked by Multi-Signal Severity & Risk Score</div>
            <hr class="section-divider">
            """, unsafe_allow_html=True)
            
            if not sorted_candidates:
                st.warning("No candidate records match the filter criteria.")
            else:
                # Render only the 5 accounts on the current page for lightning-fast DOM speed
                for r in paged_candidates:
                    is_selected = (r.customer_id == st.session_state.selected_customer_id)
                    ai_data = st.session_state.ai_results.get(r.customer_id)
                    
                    # Badge rendering
                    if ai_data:
                        risk_lvl = ai_data.get("risk_level", "Medium")
                        badge_class = f"badge-{risk_lvl.lower()}"
                        score = ai_data.get("risk_score", 50)
                        status_badge_html = f"<span class='{badge_class}'>AI: {risk_lvl.upper()} ({score}/100)</span>"
                    else:
                        status_badge_html = f"<span class='badge-pending'>Stage-1 Rule: {r.stage1_telemetry_score}/100</span>"

                    # Single Enclosed Card Box Container
                    with st.container(border=True):
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-size: 16.5px; font-weight: 800; color: #ffffff;">{r.customer_name}</span>
                            <span>{status_badge_html}</span>
                        </div>
                        <div style="font-size: 12.5px; color: #94a3b8; margin-bottom: 8px;">
                            Account ID: <code>{r.customer_id}</code> &nbsp;|&nbsp; Tier: <b>{r.account_tier}</b>
                        </div>
                        <div style="margin: 6px 0 10px 0;">
                            <span class="card-telemetry-pill">AUM: <b>₹{r.portfolio_value_inr/100000:.1f}L</b></span>
                            <span class="card-telemetry-pill">30d Outflow: <b>₹{r.net_outflow_30d_inr/100000:.1f}L</b></span>
                            <span class="card-telemetry-pill">Latency: <b>{r.avg_latency_30d_ms:.0f}ms</b></span>
                            <span class="card-telemetry-pill">Vol Δ: <b>{r.trading_volume_change_30d_pct:.0f}%</b></span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if ai_data:
                            st.markdown(f"""
                            <div class="card-driver-alert">
                                Primary Driver: {ai_data.get('primary_risk_driver')} &nbsp;•&nbsp; Urgency: <u>{ai_data.get('urgency_window')}</u>
                            </div>
                            <div class="card-agent-brief">
                                <b>Agent Brief:</b> {ai_data.get('agent_situation_summary')}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="font-size: 12px; color: #94a3b8; margin-top: 6px; margin-bottom: 6px;">
                                <i>AI Synthesis Pending. Stage-1 Trigger: {r.anomaly_count}/5 signals flagged.</i>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                        
                        # Single Simple Inspect Button inside the Card - Instant sub-millisecond switch
                        btn_label = f"View Details ({r.customer_name})" if not is_selected else f"Selected ({r.customer_name})"
                        if st.button(
                            btn_label,
                            key=f"card_sel_{r.customer_id}",
                            width="stretch",
                            type="primary" if is_selected else "secondary"
                        ):
                            st.session_state.selected_customer_id = r.customer_id
                            st.rerun()

                # Clean, Fast Pagination Navigation Controls
                st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
                pcol1, pcol2, pcol3 = st.columns([1, 1.8, 1])
                with pcol1:
                    if st.button("◀ Prev", disabled=(st.session_state.current_page <= 1), width="stretch", key="btn_prev_page"):
                        st.session_state.current_page -= 1
                        st.rerun()
                with pcol2:
                    st.markdown(
                        f"<div style='text-align: center; padding-top: 6px; font-size: 13px; color: #cbd5e1;'>"
                        f"Page <b>{st.session_state.current_page}</b> of <b>{total_pages}</b> ({total_candidates_count} total)"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                with pcol3:
                    if st.button("Next ▶", disabled=(st.session_state.current_page >= total_pages), width="stretch", key="btn_next_page"):
                        st.session_state.current_page += 1
                        st.rerun()

    # Right Column: Integrated Master Panel for Customer Deep Dive
    with col_right:
        selected_rec = loader.get_record_by_id(st.session_state.selected_customer_id)
        if not selected_rec:
            st.info("Select a customer from the queue to view details.")
        else:
            ai_data = st.session_state.ai_results.get(selected_rec.customer_id)
            
            # Enclosed Master Container for Customer Profile
            with st.container(border=True):
                # Header with Customer Name and Compact Tech-Blue Run Gemini AI Button
                dhead_c1, dhead_c2 = st.columns([1.6, 1.0])
                with dhead_c1:
                    st.markdown(f"""
                    <div style="font-size: 18px; font-weight: 800; color: #ffffff; margin-bottom: 2px;">
                        Customer Profile: {selected_rec.customer_name}
                    </div>
                    <div class="section-caption">
                        Account ID: <code>{selected_rec.customer_id}</code> &nbsp;|&nbsp; Tier: <b>{selected_rec.account_tier}</b> &nbsp;|&nbsp; Stage-1 Score: <b>{selected_rec.stage1_telemetry_score}/100</b>
                    </div>
                    """, unsafe_allow_html=True)
                with dhead_c2:
                    if gemini_detector.is_configured():
                        if st.button("Run AI insights", key=f"dhead_run_ai_{selected_rec.customer_id}", width="stretch", type="primary"):
                            with st.spinner(f"Running AI insights for {selected_rec.customer_name}..."):
                                try:
                                    single_res = gemini_detector.analyze_single(selected_rec.to_dict())
                                    st.session_state.ai_results[selected_rec.customer_id] = single_res
                                    
                                    # Auto-track pagination to the page where this customer moves after re-sorting
                                    updated_sorted = sorted(scoped_candidates, key=get_multivariate_sort_key, reverse=True)
                                    cust_idx = next((i for i, c in enumerate(updated_sorted) if c.customer_id == selected_rec.customer_id), 0)
                                    st.session_state.current_page = (cust_idx // PAGE_SIZE) + 1
                                    
                                    st.toast(f"Analysis updated in {single_res.get('latency_ms')}ms!")
                                    st.rerun()
                                except Exception as err:
                                    st.error(f"API Error: {err}")

                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

                # Telemetry Metrics Grid
                tcol1, tcol2, tcol3, tcol4 = st.columns(4)
                with tcol1:
                    st.metric("Portfolio (AUM)", f"₹{selected_rec.portfolio_value_inr/100000:.1f}L")
                with tcol2:
                    st.metric("30d Volume Δ", f"{selected_rec.trading_volume_change_30d_pct:.1f}%")
                with tcol3:
                    out_ratio = selected_rec.outflow_ratio_pct
                    st.metric("30d Net Outflow", f"₹{selected_rec.net_outflow_30d_inr/100000:.1f}L", delta=f"-{out_ratio:.1f}%" if selected_rec.net_outflow_30d_inr > 0 else "0%", delta_color="inverse")
                with tcol4:
                    st.metric("Order Latency", f"{selected_rec.avg_latency_30d_ms:.0f} ms", delta=f"{selected_rec.failed_orders_30d} failed orders", delta_color="inverse")

                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

                # Stage 2 AI Diagnosis Section
                if ai_data:
                    risk_level = ai_data.get("risk_level", "Medium")
                    badge_class = f"badge-{risk_level.lower()}"
                    
                    # 1. Frontline Agent Situation Summary
                    st.markdown("### Frontline Representative Situation Summary")
                    st.markdown(f"""
                    <div class="agent-brief-box">
                        <b>Summary & Immediate Action:</b><br>
                        {ai_data.get('agent_situation_summary')}
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

                    # 2. Root-Cause Diagnostic Rationale
                    st.markdown(f"### Root-Cause Diagnostic Rationale ({st.session_state.applied_model})")
                    st.markdown(f"""
                    <div class="rationale-box">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-weight: 700; color: #f59e0b;">Multi-Signal Cognitive Correlation:</span>
                            <span class="{badge_class}">AI Risk: {risk_level.upper()} ({ai_data.get('risk_score')}/100)</span>
                        </div>
                        {ai_data.get('signal_correlation_rationale')}
                        <div style="margin-top: 10px; font-size: 12.5px; color: #94a3b8;">
                            Churn Urgency: <b style="color: #ffffff;">{ai_data.get('urgency_window')}</b> &nbsp;|&nbsp; 
                            Model Confidence: <b style="color: #ffffff;">{int(ai_data.get('confidence_score', 0.9)*100)}%</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

                    # 3. Prescriptive Retention Playbook
                    st.markdown("### Prescriptive Operational Retention Playbook")
                    st.markdown(f"""
                    <div class="playbook-box">
                        <b>Recommended Action Plan:</b><br>
                        {ai_data.get('prescriptive_action')}
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander("Raw JSON Payload & Inference Metadata"):
                        st.json(ai_data)
                else:
                    st.markdown("""
                    <div class="agent-brief-box" style="border-left-color: #eab308; background: rgba(234, 179, 8, 0.1);">
                        <b>Gemini AI Cognitive Synthesis has not been run for this customer yet.</b><br>
                        Click the <b>'Run Gemini AI'</b> button above to synthesize this customer's profile.
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

                # Raw Support Transcript
                st.markdown("### Raw Interaction Transcript")
                st.markdown(f"""
                <div class="transcript-box">
                    {selected_rec.recent_interaction_transcript}
                </div>
                """, unsafe_allow_html=True)


# ---------------------------------------------------------
# TAB 2: Live "What-If" Signal Simulator
# ---------------------------------------------------------
with tab_simulator:
    st.subheader("Real-Time Multi-Signal Sandbox & Simulator")
    st.markdown(
        "Simulate any custom customer telemetry scenario and paste a raw chat transcript to evaluate "
        "how the Gemini AI Cognitive Synthesizer extracts root causes and recommends retention actions in real time."
    )
    
    sim_col1, sim_col2 = st.columns([1, 1.2])
    
    with sim_col1:
        st.markdown("##### 1. Structured Telemetry Inputs")
        sim_name = st.text_input("Customer Name", value="Rajiv Chhabra")
        sim_tier = st.selectbox("Account Tier", ["HNI", "Pro Trader", "Standard"], index=0)
        sim_portfolio = st.number_input("Portfolio Value (INR)", value=25000000.0, step=100000.0)
        sim_vol = st.slider("30-Day Trading Volume Change (%)", min_value=-100.0, max_value=100.0, value=-75.0)
        sim_outflow = st.number_input("30-Day Net Outflow (INR)", value=6000000.0, step=100000.0)
        sim_latency = st.slider("Avg Routing Latency (ms)", min_value=20.0, max_value=1500.0, value=780.0)
        sim_failed = st.slider("Failed Orders (30d)", min_value=0, max_value=20, value=8)
        sim_tickets = st.slider("Support Tickets (30d)", min_value=0, max_value=10, value=2)

    with sim_col2:
        st.markdown("##### 2. Raw Unstructured Interaction Transcript")
        sim_transcript = st.text_area(
            "Customer Support / RM Chat Log",
            value="Customer (11:20 AM): I noticed that my bracket orders failed to execute during the morning volatility spike. I was not able to hedge my index options. Representative: We had an exchange gateway sync issue Mr. Chhabra. Can I open a ticket? Customer: No need for tickets, this is the third time this quarter. Please verify what the daily NEFT/RTGS limit is for liquidating my margin balance.",
            height=180
        )
        
        sim_btn = st.button("Run Live Gemini AI Synthesis", type="primary", width="stretch")

        if sim_btn:
            if not gemini_detector.is_configured():
                st.error("Please configure your Gemini API Key in the sidebar form to run the simulator.")
            else:
                with st.spinner("Synthesizing multi-signal correlations with Gemini AI..."):
                    test_payload = {
                        "customer_id": "SIM-9999",
                        "customer_name": sim_name,
                        "account_tier": sim_tier,
                        "portfolio_value_inr": sim_portfolio,
                        "trading_volume_change_30d_pct": sim_vol,
                        "net_outflow_30d_inr": sim_outflow,
                        "failed_orders_30d": sim_failed,
                        "tickets_opened_30d": sim_tickets,
                        "avg_latency_30d_ms": sim_latency,
                        "recent_interaction_transcript": sim_transcript
                    }
                    
                    try:
                        sim_result = gemini_detector.analyze_single(test_payload)
                        sim_risk = sim_result.get("risk_level", "Medium")
                        badge_class = f"badge-{sim_risk.lower()}"
                        
                        st.markdown(f"""
                        <div class="rationale-box" style="margin-top: 20px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 16px; font-weight: 700; color: #ffffff;">Live Gemini AI Synthesis Result</span>
                                <span class="{badge_class}">Risk: {sim_risk.upper()} ({sim_result.get('risk_score')}/100)</span>
                            </div>
                            <div style="margin-top: 8px; font-size: 13.5px; color: #fb7185;">
                                <b>Primary Risk Driver:</b> {sim_result.get('primary_risk_driver')}
                            </div>
                            <div class="agent-brief-box" style="margin-top: 10px;">
                                <b>Agent Brief:</b> {sim_result.get('agent_situation_summary')}
                            </div>
                            <p style="font-size: 14.5px; color: #e5e7eb; margin-top: 8px; line-height: 1.6;">
                                <b>AI Correlation Rationale:</b><br>{sim_result.get('signal_correlation_rationale')}
                            </p>
                            <div class="playbook-box">
                                <b>Prescriptive Retention Action:</b><br>
                                {sim_result.get('prescriptive_action')}
                            </div>
                            <div style="margin-top: 10px; font-size: 12.5px; color: #94a3b8;">
                                Urgency: <b>{sim_result.get('urgency_window')}</b> | Confidence: <b>{int(sim_result.get('confidence_score', 0.9)*100)}%</b> | Latency: <b>{sim_result.get('latency_ms')}ms</b>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Gemini API Error: {e}")


# ---------------------------------------------------------
# TAB 4: Architecture & Two-Stage Funnel
# ---------------------------------------------------------
with tab_architecture:
    st.subheader("Architecture: Two-Stage Multi-Signal Funnel")
    st.markdown("""
    This prototype addresses the core operational flaw in traditional customer operations: **reactive escalation handling**.
    By combining high-speed deterministic telemetry filtering with deep Gemini micro-batch cognitive synthesis, the system operates at massive scale while delivering precision retention intelligence.
    """)
    
    st.markdown("""
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
    │            STAGE 2: CONCURRENT MICRO-BATCH COGNITIVE LLM SYNTHESIS (GEMINI API)             │
    │  • Chunks of 15 candidate profiles per request dispatched in parallel (max 3 workers)       │
    │  • Global Cohort Baseline Injected into each prompt for relative anomaly calibration        │
    │  • 100% Rate-Limit Safe: Strictly <= 5 RPM Free Tier limit with 429 auto-retry              │
    │  • Multi-Signal Reasoning: Correlates unstructured transcripts with telemetry anomalies    │
    │  • Generates Structured JSON: Root-Cause Rationale + Prescriptive Next Action + Urgency     │
    └──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                                   │
                                                   ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              OPERATIONAL ACTION & COMMAND CENTER                            │
    │  • Deterministic Multi-Variate Sorting: (Risk Level Weight -> Score -> Portfolio -> Outflow)│
    │  • Frontline Agent Situation Summaries & 1-Click Retention Playbooks                        │
    └─────────────────────────────────────────────────────────────────────────────────────────────┘
    ```
    """)
