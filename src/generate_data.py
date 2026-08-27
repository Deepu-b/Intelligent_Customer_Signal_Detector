"""
Data Generation Script for Intelligent Customer Signal Detector POC (Firstsource)
Domain: FinTech / Wealth-Tech Trading & Investment Platform

Generates realistic customer telemetry and multi-turn chat interactions
with curated 'Golden Records' illustrating multi-signal correlation.
"""

import os
import csv
import random
from typing import List, Dict, Any, Optional

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "customers.csv")

# ---------------------------------------------------------
# Curated Golden Records (Showcasing Multi-Signal AI Logic)
# ---------------------------------------------------------
GOLDEN_RECORDS: List[Dict[str, Any]] = [
    {
        "customer_id": "CUST-1001",
        "customer_name": "Vikramaditya Singhania",
        "account_tier": "HNI",
        "portfolio_value_inr": 34000000.0,  # 3.4 Crore
        "trading_volume_change_30d_pct": -82.5,
        "net_outflow_30d_inr": 9500000.0,  # 95 Lakhs withdrawn
        "failed_orders_30d": 1,
        "tickets_opened_30d": 1,
        "avg_latency_30d_ms": 840.0,  # Peak market delay
        "recent_interaction_transcript": (
            "Customer (10:14 AM): Good morning. I noticed that during the market open volatility on Tuesday, "
            "order confirmation took over 12 seconds on your platform. "
            "Representative (10:16 AM): Hello Mr. Singhania, thank you for reaching out. We had a brief gateway sync delay. "
            "Would you like me to open a technical support investigation? "
            "Customer (10:18 AM): No need for a ticket. I have already adjusted my asset allocation accordingly. "
            "Just confirm what the daily limit is for transferring funds out to my primary HDFC custodial account. "
            "Representative (10:20 AM): The limit is 50 Lakhs per online transaction or up to 2 Crores via RTGS with authorization. "
            "Customer (10:21 AM): Understood. Please ensure the authorization queue is cleared today."
        )
    },
    {
        "customer_id": "CUST-1002",
        "customer_name": "Rohan Deshmukh",
        "account_tier": "Pro Trader",
        "portfolio_value_inr": 5200000.0,  # 52 Lakhs
        "trading_volume_change_30d_pct": -65.0,
        "net_outflow_30d_inr": 2400000.0,  # 24 Lakhs withdrawn
        "failed_orders_30d": 14,
        "tickets_opened_30d": 5,
        "avg_latency_30d_ms": 980.0,
        "recent_interaction_transcript": (
            "Customer (14:35 PM): This is completely unacceptable. Your WebSocket API crashed twice during Thursday's BankNifty expiry. "
            "I had 4 algorithmic straddle legs fail to execute and got hit with 65,000 INR slippage. "
            "Representative (14:38 PM): We sincerely apologize for the inconvenience, Rohan. Our engineering team deployed a hotfix at 2 PM. "
            "Customer (14:40 PM): A hotfix doesn't recover 65k! I opened 3 tickets (TKT-8821, TKT-8840, TKT-8899) and all your L1 agents gave me canned replies. "
            "I already withdrew 24 Lakhs this morning. If my slippage compensation isn't reviewed by your risk desk today, "
            "I am liquidating the rest and moving my automated desk to Zerodha."
        )
    },
    {
        "customer_id": "CUST-1003",
        "customer_name": "Priyanka Sen",
        "account_tier": "Standard",
        "portfolio_value_inr": 420000.0,  # 4.2 Lakhs
        "trading_volume_change_30d_pct": -78.0,
        "net_outflow_30d_inr": 310000.0,  # 3.1 Lakhs withdrawn
        "failed_orders_30d": 3,
        "tickets_opened_30d": 2,
        "avg_latency_30d_ms": 320.0,
        "recent_interaction_transcript": (
            "Customer (11:05 AM): Hi team, hope you're having a good week. I was trying to download my consolidated capital gains statement "
            "and transaction ledger for the last 2 financial years in CSV format. "
            "Representative (11:07 AM): Hi Priyanka! You can find tax reports under Profile > Statements > Tax P&L. "
            "Customer (11:09 AM): Thank you! Also, what is the exact step-by-step checklist to de-link my bank account and initiate account deactivation "
            "if needed in the future? "
            "Representative (11:12 AM): May I ask why you're considering deactivation? "
            "Customer (11:14 AM): Just consolidating my trading portfolios onto a single platform that offers zero brokerage on options. Thanks for the quick response."
        )
    },
    {
        "customer_id": "CUST-1004",
        "customer_name": "Karthik Ramanathan",
        "account_tier": "Standard",
        "portfolio_value_inr": 850000.0,  # 8.5 Lakhs
        "trading_volume_change_30d_pct": -55.0,
        "net_outflow_30d_inr": 480000.0,
        "failed_orders_30d": 7,
        "tickets_opened_30d": 4,
        "avg_latency_30d_ms": 620.0,
        "recent_interaction_transcript": (
            "Customer (09:45 AM): Ever since the v4.2 mobile update, the biometric login keeps timing out and freezing on the order placement screen. "
            "I missed placing my stop-loss order yesterday. "
            "Representative (09:47 AM): We recommend clearing your app cache or reinstalling the app from the Play Store. "
            "Customer (09:50 AM): I did that three times already. Look at the app reviews on Play Store, everyone is complaining about the same bug. "
            "I've stopped intraday trades on your app until this is resolved."
        )
    },
    {
        "customer_id": "CUST-1005",
        "customer_name": "Aditya Verma",
        "account_tier": "Pro Trader",
        "portfolio_value_inr": 7800000.0,  # 78 Lakhs
        "trading_volume_change_30d_pct": 22.0,
        "net_outflow_30d_inr": 0.0,
        "failed_orders_30d": 1,
        "tickets_opened_30d": 4,  # High tickets, but constructive power-user feedback!
        "avg_latency_30d_ms": 55.0,
        "recent_interaction_transcript": (
            "Customer (16:10 PM): Hey guys, love the new charting tools on the desktop terminal! Just wanted to share some UX feedback: "
            "would it be possible to add customizable hotkeys for multi-leg order entry? Also noticed a minor tooltip typo on the Options Greek tab. "
            "Representative (16:13 PM): Thanks so much for the feedback Aditya! I have submitted this directly to our product UI team. "
            "Customer (16:15 PM): Awesome, keep up the great work! Looking forward to the next release."
        )
    },
]

# ---------------------------------------------------------
# Realistic Generation Pools for Procedural Customers
# ---------------------------------------------------------
FIRST_NAMES = [
    "Aarav", "Ananya", "Rahul", "Pooja", "Siddharth", "Meera", "Karan", "Divya",
    "Gaurav", "Sneha", "Arjun", "Tanvi", "Nikhil", "Shreya", "Varun", "Rhea",
    "Abhishek", "Kavya", "Manish", "Ishita", "Sanjay", "Anjali", "Deepak", "Swati",
    "Amit", "Preeti", "Rajesh", "Sunita", "Harish", "Monika", "Alok", "Ritu",
    "Tushar", "Pallavi", "Vivek", "Payal", "Sameer", "Simran", "Chetan", "Jyoti",
    "Vikram", "Tarun", "Kunal", "Bhavna", "Rohit", "Ankit", "Shruti", "Geeta"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Mehta", "Reddy", "Nair", "Kapoor", "Bose",
    "Iyer", "Chopra", "Gupta", "Rao", "Saxena", "Desai", "Menon", "Joshi",
    "Kulkarni", "Agarwal", "Bhatia", "Chatterjee", "Mishra", "Trivedi", "Banerjee",
    "Singhania", "Mukherjee", "Malhotra", "Nambiar", "Pillai", "Choudhury", "Bhatt"
]

TRANSCRIPT_TEMPLATES = {
    "critical_outflow_churn": [
        "Customer: I have requested a complete withdrawal of my liquid margin funds to my secondary bank account. Please expedite without delay. "
        "Representative: Hello, your withdrawal request is in process. Is there anything specific that prompted this transfer? "
        "Customer: I am dissatisfied with the frequent order rejection during high-volatility sessions. Not looking to discuss further.",

        "Customer: Why has my margin pledge unblocking taken more than 48 hours? I am missing trades while my capital is locked. "
        "Representative: We apologize for the delay, our clearing partner was undergoing a maintenance cycle. "
        "Customer: This is the second time this month. If this is not settled by today, I am initiating account closure and portfolio transfer.",

        "Customer: Can you provide the written confirmation for closing my custodial sub-account? "
        "Representative: We'd love to help resolve any friction first. What went wrong? "
        "Customer: I have migrated my primary derivative hedging desk to an institutional DMA provider. Just send the closure NOC."
    ],
    "high_tech_friction": [
        "Customer: The desktop trading terminal crashed twice right at 9:15 AM open. I couldn't modify my bracket orders. "
        "Representative: We had a microservice lag during the market opening tick surge. It has been resolved. "
        "Customer: Losing money because of your system latency is unacceptable. I have attached the error screenshots.",

        "Customer: My market order for NIFTY weekly calls was placed at 14:10 but got confirmed 45 seconds later at a much worse price. "
        "Representative: We are looking into the exchange connectivity logs for that timestamp. "
        "Customer: Please investigate and process slippage reimbursement. I trade high volume and expect reliable execution.",

        "Customer: Your API token expired mid-trading session without sending a refresh callback. 6 limit orders were unfulfilled. "
        "Representative: Our auth service had a scheduled key rotation. "
        "Customer: You cannot rotate auth keys during active market hours! I lost substantial margin on open naked positions."
    ],
    "subtle_dissatisfaction": [
        "Customer: Hi, could you explain why my auto-square-off charges were ₹50 + GST instead of the standard rate? "
        "Representative: Auto-square-off for intraday MIS positions carried after 3:15 PM incurs standard RMS handling fees. "
        "Customer: Other discount brokers don't charge this penalty if market volatility triggers the stop loss. Good to know.",

        "Customer: Hi team, can you share the documentation for API trading rate limits and if there are plans to offer lower margin requirements? "
        "Representative: Our API rate limit is currently 10 requests/second with standard SEBI margin requirements. "
        "Customer: Got it. Some new broker platforms are offering 20 req/s with zero brokerage. Thanks.",

        "Customer: How do I export my complete 3-year trading history into Excel format? "
        "Representative: You can download financial year statements from the Reports section. "
        "Customer: Thanks. I am consolidating all my investment statements for an external wealth audit."
    ],
    "medium_friction_support": [
        "Customer: I updated my nominee details last week through Digilocker, but the profile page still says Pending Verification. "
        "Representative: Let me check that for you right away. Yes, the backend verification is queued and will reflect within 24 hours. "
        "Customer: Okay, please make sure it goes through without requiring re-upload.",

        "Customer: Why did my UPI fund deposit of ₹50,000 take 3 hours to reflect in my trading balance? "
        "Representative: There was a brief banking partner gateway latency. The funds have now been credited to your margin account. "
        "Customer: Thanks, but please improve the gateway. Missed a good entry point today."
    ],
    "healthy_routine_inquiries": [
        "Customer: Hello! Can you please tell me when the quarterly dividend for TCS will be credited to my linked bank account? "
        "Representative: Hi! The dividend has been processed by the RTA and should credit within 3-4 working days. "
        "Customer: Great, thanks for the quick confirmation! Have a wonderful day.",

        "Customer: Hi team, I want to set up an automatic monthly SIP in Nifty 50 ETF. Is that supported via e-mandate? "
        "Representative: Yes absolutely! Go to Mutual Funds/ETFs > SIP > Select e-mandate to configure weekly or monthly recurring debits. "
        "Customer: Perfect, just configured it. Very smooth process. Thanks!",

        "Customer: Loving the new dark mode UI and the instant option chain payoff graphs. Keep it up! "
        "Representative: Thank you so much for the kind words! We are glad you are enjoying the new features. "
        "Customer: Cheers!",

        "Customer: Could you help me understand how the tax loss harvesting report calculates short-term capital gains? "
        "Representative: The report uses FIFO (First-In, First-Out) accounting according to Indian income tax regulations. "
        "Customer: Understood, that clarifies it. Thanks for the quick explanation."
    ]
}


def generate_dataset(total_rows: int = 75, seed: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Generates a full dataset of FinTech customers including Golden Records and procedural records.
    """
    if seed is not None:
        random.seed(seed)
        
    records: List[Dict[str, Any]] = [dict(r) for r in GOLDEN_RECORDS]
    current_id_num = 1006
    remaining_count = total_rows - len(records)
    
    for i in range(remaining_count):
        cust_id = f"CUST-{current_id_num}"
        current_id_num += 1
        
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        cohort_roll = random.random()
        
        if cohort_roll < 0.20:
            # At-Risk Cohort (High / Critical signals)
            tier = random.choices(["HNI", "Pro Trader", "Standard"], weights=[0.35, 0.45, 0.20])[0]
            if tier == "HNI":
                portfolio = round(random.uniform(15000000, 45000000), -4)
                outflow = round(random.uniform(0.3, 0.75) * portfolio, -4)
            elif tier == "Pro Trader":
                portfolio = round(random.uniform(2500000, 8000000), -3)
                outflow = round(random.uniform(0.2, 0.65) * portfolio, -3)
            else:
                portfolio = round(random.uniform(300000, 1500000), -3)
                outflow = round(random.uniform(0.3, 0.85) * portfolio, -3)
                
            volume_change = round(random.uniform(-92.0, -45.0), 1)
            failed_orders = random.randint(4, 16)
            tickets = random.randint(2, 6)
            latency = round(random.uniform(450.0, 1150.0), 1)
            transcript = random.choice(TRANSCRIPT_TEMPLATES["critical_outflow_churn"] + TRANSCRIPT_TEMPLATES["high_tech_friction"])
            
        elif cohort_roll < 0.50:
            # Moderate Friction / Emerging Risk Cohort
            tier = random.choices(["HNI", "Pro Trader", "Standard"], weights=[0.20, 0.35, 0.45])[0]
            if tier == "HNI":
                portfolio = round(random.uniform(10000000, 30000000), -4)
                outflow = round(random.uniform(0.05, 0.22) * portfolio, -4)
            elif tier == "Pro Trader":
                portfolio = round(random.uniform(1500000, 5000000), -3)
                outflow = round(random.uniform(0.05, 0.25) * portfolio, -3)
            else:
                portfolio = round(random.uniform(200000, 1000000), -3)
                outflow = round(random.uniform(0.05, 0.30) * portfolio, -3)
                
            volume_change = round(random.uniform(-42.0, -10.0), 1)
            failed_orders = random.randint(1, 4)
            tickets = random.randint(1, 3)
            latency = round(random.uniform(120.0, 480.0), 1)
            transcript = random.choice(TRANSCRIPT_TEMPLATES["subtle_dissatisfaction"] + TRANSCRIPT_TEMPLATES["medium_friction_support"])
            
        else:
            # Healthy / Engaged Cohort
            tier = random.choices(["HNI", "Pro Trader", "Standard"], weights=[0.25, 0.35, 0.40])[0]
            if tier == "HNI":
                portfolio = round(random.uniform(12000000, 50000000), -4)
            elif tier == "Pro Trader":
                portfolio = round(random.uniform(2000000, 7500000), -3)
            else:
                portfolio = round(random.uniform(100000, 2000000), -3)
                
            outflow = 0.0 if random.random() > 0.15 else round(random.uniform(5000, 50000), -2)
            volume_change = round(random.uniform(-5.0, 55.0), 1)
            failed_orders = random.choices([0, 1, 2], weights=[0.80, 0.15, 0.05])[0]
            tickets = random.choices([0, 1, 2], weights=[0.60, 0.30, 0.10])[0]
            latency = round(random.uniform(35.0, 110.0), 1)
            transcript = random.choice(TRANSCRIPT_TEMPLATES["healthy_routine_inquiries"])
            
        records.append({
            "customer_id": cust_id,
            "customer_name": name,
            "account_tier": tier,
            "portfolio_value_inr": portfolio,
            "trading_volume_change_30d_pct": volume_change,
            "net_outflow_30d_inr": outflow,
            "failed_orders_30d": failed_orders,
            "tickets_opened_30d": tickets,
            "avg_latency_30d_ms": latency,
            "recent_interaction_transcript": transcript
        })
        
    return records


def save_to_csv(records: List[Dict[str, Any]], filepath: str = OUTPUT_FILE) -> None:
    """Saves records to CSV with exact required schema headers."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fieldnames = [
        "customer_id",
        "customer_name",
        "account_tier",
        "portfolio_value_inr",
        "trading_volume_change_30d_pct",
        "net_outflow_30d_inr",
        "failed_orders_30d",
        "tickets_opened_30d",
        "avg_latency_30d_ms",
        "recent_interaction_transcript"
    ]
    
    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            writer.writerow(row)


def regenerate_dataset_file(filepath: str = OUTPUT_FILE, seed: Optional[int] = None) -> List[Dict[str, Any]]:
    """Regenerates dataset with an optional seed and writes to CSV."""
    records = generate_dataset(total_rows=75, seed=seed)
    save_to_csv(records, filepath)
    return records


if __name__ == "__main__":
    dataset = generate_dataset(total_rows=75, seed=42)
    save_to_csv(dataset, OUTPUT_FILE)
    print(f"Generated {len(dataset)} records at {OUTPUT_FILE}")
