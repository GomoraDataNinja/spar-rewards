import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import hashlib
import re

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="SPAR Rewards Intelligence",
    page_icon="🎯",
    layout="wide"
)

# =====================================================
# SECURITY - SINGLE PASSWORD "spar"
# =====================================================

# Password hash for "spar"
PASSWORD_HASH = hashlib.sha256("spar".encode()).hexdigest()

def verify_password(password):
    return hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH

def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'login_attempt' not in st.session_state:
        st.session_state.login_attempt = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'show_segmentation_chart' not in st.session_state:
        st.session_state.show_segmentation_chart = False
    if 'show_age_chart' not in st.session_state:
        st.session_state.show_age_chart = False
    if 'show_clv_chart' not in st.session_state:
        st.session_state.show_clv_chart = False
    if 'show_churn_chart' not in st.session_state:
        st.session_state.show_churn_chart = False
    if 'show_monthly_chart' not in st.session_state:
        st.session_state.show_monthly_chart = False

init_session_state()

# =====================================================
# COMPACT LOGIN FORM (NOT FULL PAGE)
# =====================================================

def login_form():
    # Create three columns for centering
    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        st.markdown(f"""
        <style>
        /* Keep app background normal */
        .stApp {{
            background-color: #f6f7fb !important;
        }}
        
        /* Better fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}
        
        .compact-login-card {{
            background: white;
            padding: 30px 35px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
            border-top: 4px solid #E31837;
            margin-top: 80px;
        }}
        
        .compact-login-card h1 {{
            color: #E31837;
            font-size: 24px;
            margin-bottom: 8px;
            font-weight: 700;
        }}
        
        .compact-login-card p {{
            color: #666;
            font-size: 14px;
            margin-bottom: 25px;
        }}
        
        .compact-login-card .stTextInput > div > div > input {{
            border-radius: 10px;
            padding: 12px 15px;
            border: 1px solid #ddd;
            font-size: 14px;
        }}
        
        .compact-login-card .stButton > button {{
            width: 100%;
            background-color: #E31837;
            color: white;
            border-radius: 10px;
            height: 46px;
            font-weight: 600;
            border: none;
            margin-top: 10px;
        }}
        
        .compact-login-card .stButton > button:hover {{
            background-color: #B8102E;
        }}
        </style>
        
        <div class="compact-login-card">
            <h1>🎯 SPAR Rewards Intelligence Hub</h1>
            <p>Enter password to access dashboard</p>
        """, unsafe_allow_html=True)
        
        password = st.text_input("", placeholder="Enter password", type="password", key="login_password_input", label_visibility="collapsed")
        
        if st.button("Access Dashboard", key="login_button", use_container_width=True):
            if verify_password(password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.session_state.login_attempt += 1
                st.error("❌ Incorrect password. Please try again.")
        
        st.markdown(f"""
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# SPAR BRAND COLORS
# =====================================================
SPAR_RED = "#E31837"
SPAR_GREEN = "#8DC63F"
SPAR_DARK_RED = "#B8102E"
SPAR_LIGHT_GREEN = "#A8D46B"
SPAR_GRAY = "#f6f7fb"
SPAR_WHITE = "#FFFFFF"

# =====================================================
# MODERN UI STYLING WITH BETTER FONTS
# =====================================================
st.markdown(f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    
    /* Global font settings */
    html, body, [class*="css"] {{
        font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Main container */
    .main {{
        background-color: {SPAR_GRAY};
    }}
    
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 2rem;
    }}
    
    /* Headers with better fonts */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Inter', 'SF Pro Display', sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }}
    
    /* Centered Header styling */
    .header {{
        background: linear-gradient(135deg, {SPAR_WHITE} 0%, {SPAR_GRAY} 100%);
        padding: 20px 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        text-align: center;
        border-bottom: 3px solid {SPAR_RED};
    }}
    
    .header h1 {{
        font-family: 'Inter', 'SF Pro Display', sans-serif;
        font-weight: 800;
        font-size: 32px;
        margin-bottom: 5px;
        color: {SPAR_RED};
        letter-spacing: -0.5px;
        text-align: center;
    }}
    
    .header p {{
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #666;
        margin-top: 5px;
        text-align: center;
        font-weight: 400;
    }}
    
    /* Card styling */
    .card {{
        background-color: {SPAR_WHITE};
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .card:hover {{
        transform: translateY(-2px);
        box-shadow: 0px 4px 20px rgba(0,0,0,0.12);
    }}
    
    /* Metric card styling */
    .metric-card {{
        background: linear-gradient(135deg, {SPAR_WHITE} 0%, {SPAR_GRAY} 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        border-top: 3px solid {SPAR_RED};
        transition: all 0.3s;
    }}
    
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0px 4px 15px rgba(227,24,55,0.15);
        border-top: 3px solid {SPAR_GREEN};
    }}
    
    .big-number {{
        font-family: 'Inter', 'SF Pro Display', sans-serif;
        font-weight: 800;
        font-size: 32px;
        color: {SPAR_RED};
        margin-bottom: 5px;
    }}
    
    .label {{
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }}
    
    /* Action center styling */
    .action-card {{
        background: linear-gradient(135deg, {SPAR_RED} 0%, {SPAR_DARK_RED} 100%);
        padding: 15px;
        border-radius: 12px;
        color: white;
        margin-bottom: 10px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }}
    
    .action-card h4 {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        margin: 0 0 5px 0;
        font-size: 14px;
    }}
    
    .action-card p {{
        margin: 0;
        font-size: 12px;
        opacity: 0.9;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background-color: {SPAR_WHITE};
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: {SPAR_RED};
        color: white;
        border: none;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s;
    }}
    
    .stButton > button:hover {{
        background-color: {SPAR_DARK_RED};
        transform: translateY(-1px);
        box-shadow: 0px 2px 8px rgba(227,24,55,0.3);
    }}
    
    /* Expander styling for collapsible sections */
    .streamlit-expanderHeader {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        background-color: {SPAR_WHITE};
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: {SPAR_GRAY};
        border-color: {SPAR_RED};
    }}
    
    /* Dataframe styling */
    .dataframe {{
        font-family: 'Inter', monospace;
        font-size: 13px;
    }}
    
    /* Filter section */
    .filter-section {{
        background-color: {SPAR_WHITE};
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }}
    
    /* Divider */
    hr {{
        margin: 20px 0;
        border: none;
        height: 1px;
        background: linear-gradient(to right, {SPAR_RED}, {SPAR_GREEN}, {SPAR_RED});
    }}
    
    /* Welcome screen */
    .welcome-screen {{
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, {SPAR_WHITE} 0%, {SPAR_GRAY} 100%);
        border-radius: 20px;
        margin-top: 50px;
    }}
    
    /* Chat message styling */
    .chat-message-user {{
        background-color: {SPAR_RED};
        color: white;
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 85%;
        margin-left: auto;
        font-family: 'Inter', sans-serif;
    }}
    
    .chat-message-assistant {{
        background-color: {SPAR_WHITE};
        color: #333;
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 85%;
        border-left: 3px solid {SPAR_RED};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Toggle button styling */
    .toggle-btn {{
        background-color: {SPAR_GREEN};
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCTION TO CALCULATE AGE GROUP
# =====================================================
def calculate_age_group(birthdate):
    if pd.isna(birthdate):
        return "Unknown"
    today = datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 18: return "Under 18"
    elif age < 25: return "18-24"
    elif age < 35: return "25-34"
    elif age < 45: return "35-44"
    elif age < 55: return "45-54"
    elif age < 65: return "55-64"
    else: return "65+"

# =====================================================
# MONTHLY PERFORMANCE METRICS
# =====================================================
@st.cache_data
def calculate_monthly_performance(df):
    """Calculate monthly revenue and customer metrics"""
    df = df.copy()
    df['year_month'] = df['redemption_date'].dt.strftime('%Y-%m')
    
    monthly_stats = df.groupby('year_month').agg(
        revenue=('basket_value', 'sum'),
        transactions=('member_number', 'count'),
        unique_customers=('member_number', 'nunique'),
        avg_basket=('basket_value', 'mean')
    ).reset_index()
    
    # Sort by date
    monthly_stats = monthly_stats.sort_values('year_month')
    
    return monthly_stats

# =====================================================
# CHURN PREDICTION - IMPROVED VERSION
# =====================================================
@st.cache_data
def calculate_churn_probability(rfm):
    # Normalize metrics
    max_recency = max(rfm['recency'].max(), 1)
    max_frequency = max(rfm['frequency'].max(), 1)
    max_monetary = max(rfm['monetary'].max(), 1)
    
    rfm['churn_score'] = (
        (rfm['recency'] / max_recency) * 0.5 +
        (1 - rfm['frequency'] / max_frequency) * 0.3 +
        (1 - rfm['monetary'] / max_monetary) * 0.2
    )
    
    # More granular churn risk categories
    rfm['churn_risk'] = pd.cut(rfm['churn_score'], 
                                bins=[0, 0.25, 0.5, 0.75, 1], 
                                labels=['Very Low Risk', 'Low Risk', 'Medium Risk', 'High Risk'])
    return rfm

# =====================================================
# CUSTOMER LIFETIME VALUE
# =====================================================
@st.cache_data
def calculate_clv(rfm):
    avg_transaction_value = rfm['monetary'] / rfm['frequency'].clip(lower=1)
    avg_frequency_days = rfm['recency'] / rfm['frequency'].clip(lower=1)
    purchase_frequency_per_month = 30 / avg_frequency_days.clip(lower=1)
    rfm['clv'] = avg_transaction_value * purchase_frequency_per_month * 12
    rfm['clv'] = rfm['clv'].fillna(0)
    try:
        rfm['clv_segment'] = pd.qcut(rfm['clv'], q=4, labels=['Bronze', 'Silver', 'Gold', 'Platinum'])
    except:
        rfm['clv_segment'] = 'Standard'
    return rfm

# =====================================================
# TIME-BASED INSIGHTS
# =====================================================
def add_time_insights(df):
    df = df.copy()
    df['hour'] = df['redemption_date'].dt.hour
    df['day_of_week'] = df['redemption_date'].dt.day_name()
    hourly_revenue = df.groupby('hour')['basket_value'].sum().reset_index()
    hourly_revenue.columns = ['Hour', 'Revenue']
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_patterns = df.groupby('day_of_week')['basket_value'].sum().reindex(day_order).reset_index()
    daily_patterns.columns = ['Day', 'Revenue']
    return hourly_revenue, daily_patterns

# =====================================================
# CAMPAIGN ROI TRACKING
# =====================================================
def calculate_campaign_impact(rfm):
    return {
        'total_customers_targeted': len(rfm[rfm['priority'].isin(['High', 'Medium'])]),
        'potential_revenue_at_risk': rfm[rfm['segment'].isin(['⚠️ At Risk', '⚠️ Warming'])]['monetary'].sum(),
        'estimated_retention_value': rfm[rfm['segment'].isin(['⚠️ At Risk', '⚠️ Warming'])]['monetary'].sum() * 0.3,
        'high_value_customers': len(rfm[rfm['clv_segment'] == 'Platinum']) if 'clv_segment' in rfm.columns else 0,
        'avg_clv': rfm['clv'].mean() if 'clv' in rfm.columns else 0,
        'total_opportunity': rfm[rfm['churn_risk'] == 'High Risk']['monetary'].sum() if 'churn_risk' in rfm.columns else 0
    }

# =====================================================
# GENERATE ALERTS - UPDATED WITH NEW LOGIC
# =====================================================
def generate_alerts(rfm):
    alerts = []
    
    # Alert 1: High-value customers at high risk
    if 'clv' in rfm.columns and 'churn_risk' in rfm.columns:
        high_risk_high_value = rfm[(rfm['churn_risk'] == 'High Risk') & 
                                    (rfm['clv'] > rfm['clv'].quantile(0.75))]
        if len(high_risk_high_value) > 0:
            alerts.append(f"🚨 CRITICAL: {len(high_risk_high_value)} high-value customers at HIGH churn risk!")
    
    # Alert 2: At risk customers count (based on new logic)
    at_risk = len(rfm[rfm['segment'] == '⚠️ At Risk'])
    warming = len(rfm[rfm['segment'] == '⚠️ Warming'])
    if at_risk > 30:
        alerts.append(f"⚠️ WARNING: {at_risk} customers at risk + {warming} warming up. Immediate action recommended!")
    elif warming > 50:
        alerts.append(f"⚠️ HEADS UP: {warming} customers showing early warning signs (30-60 days inactive)")
    
    # Alert 3: Churned customers
    churned = len(rfm[rfm['segment'] == '💔 Churned'])
    if churned > 100:
        alerts.append(f"💔 ALERT: {churned} customers have churned (>90 days). Re-engagement campaign needed!")
    
    return alerts

# =====================================================
# BENCHMARKS
# =====================================================
def calculate_benchmarks(rfm):
    return {
        'Total Customers': len(rfm),
        'Avg Customer Value': rfm['monetary'].mean(),
        'Avg Frequency': rfm['frequency'].mean(),
        'Avg Recency (days)': rfm['recency'].mean(),
        'Retention Rate': len(rfm[rfm['frequency'] > 1]) / len(rfm) * 100 if len(rfm) > 0 else 0,
        'Churn Rate': len(rfm[rfm['segment'] == '💔 Churned']) / len(rfm) * 100 if len(rfm) > 0 else 0,
        'Active Rate (30 days)': len(rfm[rfm['recency'] <= 30]) / len(rfm) * 100 if len(rfm) > 0 else 0,
        'Avg CLV': rfm['clv'].mean() if 'clv' in rfm.columns else 0
    }

# =====================================================
# DATA CLEANING
# =====================================================
@st.cache_data
def clean_data(df):
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    if 'member_number' not in df.columns:
        for col in ['member no', 'member', 'customer_id', 'customer']:
            if col in df.columns:
                df.rename(columns={col: 'member_number'}, inplace=True)
                break
    
    if 'redemption_date' not in df.columns:
        for col in ['date', 'transaction_date', 'created_date', 'creation_date', 'redeem_date']:
            if col in df.columns:
                df.rename(columns={col: 'redemption_date'}, inplace=True)
                break
    
    if 'redeeming_basket_value' in df.columns:
        df.rename(columns={'redeeming_basket_value': 'basket_value'}, inplace=True)
    
    if 'birthday' in df.columns:
        df['birthday'] = pd.to_datetime(df['birthday'], errors='coerce')
        df['age_group'] = df['birthday'].apply(calculate_age_group)
    else:
        df['age_group'] = "Unknown"
    
    df['redemption_date'] = pd.to_datetime(df['redemption_date'], errors='coerce')
    df['basket_value'] = pd.to_numeric(df['basket_value'], errors='coerce')
    df['year'] = df['redemption_date'].dt.year
    df['month'] = df['redemption_date'].dt.month
    df['day'] = df['redemption_date'].dt.day
    
    # Convert day to integer (fix for float values)
    df['day'] = df['day'].astype('Int64')
    
    df = df[df['basket_value'] > 0]
    df = df[df['member_number'].notna()]
    df = df[df['redemption_date'].notna()]
    
    if 'status' in df.columns:
        df = df[df['status'].str.lower() == 'redeemed']
    
    return df

# =====================================================
# RFM CALCULATION
# =====================================================
@st.cache_data
def calculate_rfm(df):
    ref_date = df['redemption_date'].max()
    rfm = df.groupby('member_number').agg(
        recency=('redemption_date', lambda x: (ref_date - x.max()).days),
        frequency=('member_number', 'count'),
        monetary=('basket_value', 'sum'),
        avg_basket=('basket_value', 'mean'),
        age_group=('age_group', 'first')
    )
    return rfm

# =====================================================
# SIMPLIFIED SEGMENTATION - BASED ONLY ON RECENCY
# =====================================================
def segment_customers(rfm):
    """
    SIMPLIFIED 5-STEP SEGMENTATION (Recency Only):
    Step 1: Active (0-30 days) → ⭐ Active
    Step 2: Warming (31-60 days) → ⚠️ Warming  
    Step 3: At Risk (61-90 days) → ⚠️ At Risk
    Step 4: Churned (>90 days) → 💔 Churned
    Step 5: One-Time (frequency=1, not captured above) → 🆕 One-Time
    """
    # Initialize all as 'Other'
    rfm['segment'] = '📊 Other'
    
    # =============================================
    # STEP 1: ACTIVE (0-30 days) - LOW PRIORITY
    # =============================================
    mask_active = (rfm['recency'] <= 30)
    rfm.loc[mask_active, 'segment'] = "⭐ Active"
    
    # =============================================
    # STEP 2: WARMING (31-60 days) - HIGH PRIORITY
    # =============================================
    mask_warming = (rfm['recency'] > 30) & (rfm['recency'] <= 60)
    rfm.loc[mask_warming, 'segment'] = "⚠️ Warming"
    
    # =============================================
    # STEP 3: AT RISK (61-90 days) - HIGH PRIORITY
    # =============================================
    mask_at_risk = (rfm['recency'] > 60) & (rfm['recency'] <= 90)
    rfm.loc[mask_at_risk, 'segment'] = "⚠️ At Risk"
    
    # =============================================
    # STEP 4: CHURNED (>90 days) - HIGH PRIORITY
    # =============================================
    mask_churned = (rfm['recency'] > 90)
    rfm.loc[mask_churned, 'segment'] = "💔 Churned"
    
    # =============================================
    # STEP 5: ONE-TIME (frequency == 1, not already classified)
    # =============================================
    mask_one_time = (rfm['frequency'] == 1) & (rfm['segment'] == '📊 Other')
    rfm.loc[mask_one_time, 'segment'] = "🆕 One-Time"
    
    # =============================================
    # RISK SCORE based on segment
    # =============================================
    risk_map = {
        '⭐ Active': 0,
        '⚠️ Warming': 60,
        '⚠️ At Risk': 80,
        '💔 Churned': 95,
        '🆕 One-Time': 30,
        '📊 Other': 50
    }
    rfm['risk_score'] = rfm['segment'].map(risk_map)
    
    return rfm

# =====================================================
# SIMPLIFIED ACTION ENGINE - BASED ON RECENCY SEGMENTS
# =====================================================
def generate_actions(rfm):
    actions = []
    priorities = []
    
    for idx, row in rfm.iterrows():
        if row['segment'] == '⚠️ At Risk':
            actions.append("🚨 URGENT: Send 30% discount + personalized email")
            priorities.append("High")
        elif row['segment'] == '⚠️ Warming':
            actions.append("⚡ ACT NOW: Send 15% off + engagement email")
            priorities.append("High")
        elif row['segment'] == '💔 Churned':
            actions.append("🔄 Win-back campaign with special offer")
            priorities.append("High")
        elif row['segment'] == '🆕 One-Time':
            actions.append("🎁 Welcome back incentive + loyalty program invite")
            priorities.append("Medium")
        elif row['segment'] == '⭐ Active':
            actions.append("🎉 Thank you for shopping! Check out our latest offers")
            priorities.append("Low")
        else:
            actions.append("📈 Nurture engagement with regular content")
            priorities.append("Low")
    
    rfm['recommended_action'] = actions
    rfm['priority'] = priorities
    return rfm

# =====================================================
# SAFE FORMATTING FUNCTIONS
# =====================================================
def safe_int_format(value):
    """Safely format integer values"""
    try:
        if pd.isna(value) or value is None:
            return "0"
        return f"{int(round(float(value))):,}"
    except:
        return "0"

def safe_currency_format(value):
    """Safely format currency values"""
    try:
        if pd.isna(value) or value is None:
            return "$0"
        return f"${float(value):,.0f}"
    except:
        return "$0"

def safe_percent_format(value):
    """Safely format percentage values"""
    try:
        if pd.isna(value) or value is None:
            return "0%"
        return f"{float(value):.1f}%"
    except:
        return "0%"

def safe_day_format(day):
    """Safely format day values for display"""
    try:
        if pd.isna(day) or day is None:
            return "01"
        return f"{int(float(day)):02d}"
    except:
        return "01"

# =====================================================
# TANAKA AI ASSISTANT - ENHANCED WITH CONTEXT MEMORY
# =====================================================

class TanakaAssistant:
    """SPAR AI Assistant with conversation memory and multiple response handling"""
    
    def __init__(self):
        self.name = "Tanaka"
        self.context = {}
        
    def get_greeting(self):
        greetings = [
            f"👋 Hi! I'm {self.name}, your SPAR Rewards AI assistant. How can I help you today?",
            f"🎯 Hello! {self.name} here. Ready to analyze your customer data and SPAR Rewards insights!",
            f"📊 Welcome! I'm {self.name}. Ask me anything about your customers, rewards program, or retention strategies!"
        ]
        return np.random.choice(greetings)
    
    def get_spar_info_response(self, question):
        q = question.lower()
        
        spar_info = {
            'spar rewards': "🎯 **SPAR Rewards Program**\n\n- Earn 1 point per $1 spent\n- Double points on your birthday\n- Exclusive member discounts\n- Birthday rewards\n- Join free at any SPAR store!",
            'how to join': "📝 **How to Join SPAR Rewards:**\n\n1. Visit any SPAR store near you\n2. Fill out the registration form\n3. Receive your member number\n4. Start earning points instantly!\n\nIt's completely FREE!",
            'earn points': "⭐ **How to Earn Points:**\n\n- 1 point per $1 spent\n- 2x points on your birthday month\n- Bonus points on promotional items\n- Referral bonuses for friends who join",
            'redeem': "🎁 **How to Redeem Points:**\n\n- 100 points = $5 voucher\n- 500 points = $30 voucher\n- 1000 points = $70 voucher\n\nJust ask the cashier to check your balance at checkout!",
            'benefits': "✨ **SPAR Rewards Benefits:**\n\n- 🎂 Birthday rewards\n- 💰 Exclusive discounts\n- 🎯 Personalized offers\n- 🏆 Loyalty bonuses\n- 📱 Digital member card",
            'tiers': "🏆 **Membership Tiers:**\n\n- Bronze: 0-500 points\n- Silver: 501-1000 points  \n- Gold: 1001-2000 points\n- Platinum: 2000+ points\n\nHigher tiers = better rewards!"
        }
        
        for key, response in spar_info.items():
            if key in q:
                return response
        return None
    
    def get_data_response(self, question, rfm, df):
        q = question.lower()
        
        # Customer counts by segment
        if 'active customers' in q or 'active members' in q:
            active = len(rfm[rfm['segment'] == '⭐ Active'])
            return f"👥 **Active Customers:** {active:,} members have shopped in the last 30 days"
        
        elif 'at risk' in q and 'warming' not in q:
            at_risk = len(rfm[rfm['segment'] == '⚠️ At Risk'])
            return f"⚠️ **At Risk Customers:** {at_risk:,} members haven't shopped in 60-90 days. They need urgent attention!"
        
        elif 'warming' in q:
            warming = len(rfm[rfm['segment'] == '⚠️ Warming'])
            return f"⚡ **Warming Customers:** {warming:,} members inactive for 30-60 days. Time to re-engage them!"
        
        elif 'churned' in q:
            churned = len(rfm[rfm['segment'] == '💔 Churned'])
            return f"💔 **Churned Customers:** {churned:,} members haven't shopped in over 90 days. A win-back campaign could help!"
        
        elif 'one time' in q or 'one-time' in q:
            one_time = len(rfm[rfm['segment'] == '🆕 One-Time'])
            return f"🆕 **One-Time Customers:** {one_time:,} members made only one purchase. Time to convert them into repeat buyers!"
        
        # Revenue metrics
        elif 'total revenue' in q or 'total sales' in q:
            total_rev = rfm['monetary'].sum()
            return f"💰 **Total Revenue:** ${total_rev:,.2f} from all customers"
        
        elif 'average order' in q or 'avg basket' in q:
            avg_basket = rfm['avg_basket'].mean()
            return f"🛒 **Average Basket Value:** ${avg_basket:.2f} per transaction"
        
        elif 'clv' in q or 'lifetime value' in q:
            avg_clv = rfm['clv'].mean()
            high_clv = rfm[rfm['clv_segment'] == 'Platinum']['clv'].count() if 'clv_segment' in rfm.columns else 0
            return f"💎 **Customer Lifetime Value:**\n- Average CLV: ${avg_clv:.2f}\n- Platinum members: {high_clv:,} high-value customers"
        
        # Performance metrics
        elif 'retention' in q or 'retention rate' in q:
            retention = len(rfm[rfm['frequency'] > 1]) / len(rfm) * 100
            return f"📈 **Retention Rate:** {retention:.1f}% of customers have made multiple purchases"
        
        elif 'churn rate' in q:
            churn_rate = len(rfm[rfm['segment'] == '💔 Churned']) / len(rfm) * 100
            return f"⚠️ **Churn Rate:** {churn_rate:.1f}% of customers have stopped engaging"
        
        elif 'active rate' in q:
            active_rate = len(rfm[rfm['recency'] <= 30]) / len(rfm) * 100
            return f"✅ **Active Rate:** {active_rate:.1f}% of customers shopped in the last 30 days"
        
        # Monthly performance
        elif 'monthly' in q or 'trend' in q or 'performance' in q:
            monthly_stats = calculate_monthly_performance(df)
            if not monthly_stats.empty:
                latest_month = monthly_stats.iloc[-1]
                prev_month = monthly_stats.iloc[-2] if len(monthly_stats) > 1 else latest_month
                growth = ((latest_month['revenue'] - prev_month['revenue']) / prev_month['revenue'] * 100) if prev_month['revenue'] > 0 else 0
                return f"📈 **Monthly Performance:**\n- Latest month revenue: ${latest_month['revenue']:,.2f}\n- Month-over-month growth: {growth:+.1f}%\n- Active customers: {latest_month['unique_customers']:,}\n- Total transactions: {latest_month['transactions']:,}"
        
        # Help and suggestions
        elif 'help' in q or 'what can you do' in q:
            return self.get_help_text()
        
        return None
    
    def get_help_text(self):
        return """🤖 **I can help you with:**\n\n**📊 Customer Insights**\n- Ask about active, at-risk, or churned customers\n- Check total revenue or average order value\n- Get CLV (Customer Lifetime Value) metrics\n\n**🎯 SPAR Rewards Info**\n- How to join the rewards program\n- How to earn and redeem points\n- Membership benefits and tiers\n\n**📈 Performance Metrics**\n- Retention and churn rates\n- Active customer rates\n- Monthly performance trends\n\n**💡 Try asking:**\n- "How many at risk customers do we have?"\n- "What's our total revenue?"\n- "How do I earn SPAR points?"\n- "Show me active customers"\n- "What's our monthly performance trend?" """
    
    def get_follow_up_suggestions(self, last_question, rfm):
        q = last_question.lower()
        suggestions = []
        
        if 'at risk' in q:
            suggestions = [
                "Show me at risk customers by age group",
                "What's the revenue at risk?",
                "How can we re-engage warming customers?"
            ]
        elif 'revenue' in q or 'sales' in q:
            suggestions = [
                "Show revenue by customer segment",
                "What's the average order value?",
                "Which segment generates most revenue?"
            ]
        elif 'active' in q:
            suggestions = [
                "What's the retention rate?",
                "Show me active customers by age group",
                "How many one-time customers do we have?"
            ]
        elif 'churned' in q:
            suggestions = [
                "How can we win back churned customers?",
                "Show me churned customers by segment",
                "What's our current churn rate?"
            ]
        elif 'monthly' in q or 'trend' in q:
            suggestions = [
                "Show me the monthly performance chart",
                "Which month had highest revenue?",
                "What's the customer growth trend?"
            ]
        
        if suggestions:
            return "\n\n💡 **Follow-up questions you might like:**\n" + "\n".join([f"   • {s}" for s in suggestions])
        return ""
    
    def get_response(self, question, rfm=None, df=None):
        """Main response handler with multiple response types and context"""
        if not question:
            return self.get_greeting()
        
        question_lower = question.lower()
        
        # Check for greetings
        if any(greeting in question_lower for greeting in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
            greetings = [
                f"👋 Hello! {self.name} here, ready to help with your SPAR Rewards data!",
                f"🎯 Hi there! I'm {self.name}. What would you like to know about your customers today?",
                f"📊 Hey! {self.name} at your service. Ask me anything about your analytics!"
            ]
            return np.random.choice(greetings)
        
        # Check for thank you
        if any(word in question_lower for word in ['thank', 'thanks', 'appreciate']):
            return f"😊 You're welcome! I'm {self.name}, always happy to help. Any other questions about your data?"
        
        # Check for bye
        if any(word in question_lower for word in ['bye', 'goodbye', 'see you']):
            return f"👋 Goodbye! {self.name} signing off. Come back anytime you need insights about your SPAR Rewards data!"
        
        # Get response from SPAR info
        response = self.get_spar_info_response(question)
        if response:
            return response
        
        # Get response from data (if rfm is available)
        if rfm is not None:
            response = self.get_data_response(question, rfm, df)
            if response:
                # Add follow-up suggestions
                follow_up = self.get_follow_up_suggestions(question, rfm)
                return response + follow_up
        
        # Default response with help
        return f"🤔 I'm not sure about that, {self.name} here. {self.get_help_text()}"

# Initialize Tanaka
tanaka = TanakaAssistant()

# =====================================================
# MAIN APP - Only show if authenticated
# =====================================================

if not st.session_state.authenticated:
    login_form()
else:
    # Logout button and header
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("🚪 Logout", key="logout_button", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="header">
            <h1>🎯 SPAR Rewards Intelligence Hub</h1>
            <p>Customer behavior analysis • Retention strategies • Revenue optimization • Predictive Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar for file upload
    with st.sidebar:
        st.markdown(f"<h3 style='color:{SPAR_RED};'>📂 Upload Data</h3>", unsafe_allow_html=True)
        file = st.file_uploader("Choose CSV file", type=["csv"], key="file_uploader")
        
        if file:
            st.success("✅ File loaded successfully")
    
    if not file:
        st.markdown("""
        <div class="welcome-screen">
            <h2 style="color: #E31837;">🎯 Welcome to SPAR Rewards Intelligence Hub</h2>
            <p style="font-size: 18px; color: #666; margin-top: 20px;">Upload your customer transaction data to unlock powerful insights</p>
            <p style="font-size: 14px; color: #999; margin-top: 30px;">
                Required columns: Member Number, Redemption Date, Redeeming Basket Value<br>
                Optional: Birthday, Status
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📖 View sample data format"):
            sample_df = pd.DataFrame({
                'Member Number': ['M001234', 'M001234', 'M005678'],
                'Redemption Date': ['2026-04-01', '2026-03-15', '2026-04-05'],
                'Redeeming Basket Value': [45.50, 32.00, 89.99],
                'Birthday': ['1990-05-15', '1990-05-15', '1985-12-20'],
                'Status': ['redeemed', 'redeemed', 'redeemed']
            })
            st.dataframe(sample_df)
    
    elif file:
        df = pd.read_csv(file)
        df = clean_data(df)
        
        if df.empty:
            st.error("❌ No valid data found. Please check your file format.")
            st.stop()
        
        # DATE SLICER
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown("### 📅 Date Slicer")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            available_years = sorted(df['year'].unique(), reverse=True)
            available_years = [int(y) for y in available_years if pd.notna(y)]
            selected_years = st.multiselect("Select Year(s)", options=available_years, default=available_years if len(available_years) <= 3 else [available_years[0]], key="year_select")
        
        with col2:
            months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                      7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
            available_months = sorted(df['month'].unique())
            available_months = [int(m) for m in available_months if pd.notna(m)]
            selected_months = st.multiselect("Select Month(s)", options=available_months, default=available_months, format_func=lambda x: months.get(x, str(x)), key="month_select")
        
        with col3:
            available_days = sorted(df['day'].unique())
            available_days = [int(d) for d in available_days if pd.notna(d)]
            selected_days = st.multiselect("Select Day(s)", options=available_days, default=available_days, format_func=safe_day_format, key="day_select")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply date filters
        filtered_df = df.copy()
        if selected_years:
            filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]
        if selected_months:
            filtered_df = filtered_df[filtered_df['month'].isin(selected_months)]
        if selected_days:
            filtered_df = filtered_df[filtered_df['day'].isin(selected_days)]
        
        if filtered_df.empty:
            st.warning("⚠️ No data available for the selected date range.")
            st.stop()
        
        # Calculate monthly performance
        monthly_stats = calculate_monthly_performance(filtered_df)
        
        # Calculate all metrics (order matters now)
        rfm = calculate_rfm(filtered_df)
        rfm = calculate_churn_probability(rfm)
        rfm = segment_customers(rfm)
        rfm = generate_actions(rfm)
        rfm = calculate_clv(rfm)
        rfm = rfm.reset_index()
        
        # Time insights
        hourly_revenue, daily_patterns = add_time_insights(filtered_df)
        campaign_metrics = calculate_campaign_impact(rfm)
        alerts = generate_alerts(rfm)
        benchmarks = calculate_benchmarks(rfm)
        
        # KPI CARDS - Using safe formatting
        col1, col2, col3, col4 = st.columns(4)
        
        def card(title, value, icon=""):
            st.markdown(f"""
            <div class="metric-card">
                <div class="big-number">{icon}{value}</div>
                <div class="label">{title}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Calculate counts for KPI cards with safe values
        total_customers = len(rfm)
        total_revenue = safe_currency_format(rfm['monetary'].sum())
        avg_clv = safe_currency_format(rfm['clv'].mean())
        at_risk_count = len(rfm[rfm['segment'] == '⚠️ At Risk'])
        warming_count = len(rfm[rfm['segment'] == '⚠️ Warming'])
        
        with col1:
            card("Total Customers", f"{total_customers:,}", "👥 ")
        with col2:
            card("Total Revenue", total_revenue, "💰 ")
        with col3:
            card("Avg. CLV", avg_clv, "💎 ")
        with col4:
            card("At Risk / Warming", f"{at_risk_count} / {warming_count}", "⚠️ ")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # =====================================================
        # MONTHLY PERFORMANCE LINE CHART (ALWAYS VISIBLE)
        # =====================================================
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 Monthly Performance Trend")
        
        if not monthly_stats.empty:
            # Create figure with secondary y-axis
            fig = go.Figure()
            
            # Add revenue line
            fig.add_trace(go.Scatter(
                x=monthly_stats['year_month'],
                y=monthly_stats['revenue'],
                name='Revenue ($)',
                line=dict(color=SPAR_RED, width=3),
                marker=dict(size=8),
                yaxis='y'
            ))
            
            # Add unique customers line
            fig.add_trace(go.Scatter(
                x=monthly_stats['year_month'],
                y=monthly_stats['unique_customers'],
                name='Active Customers',
                line=dict(color=SPAR_GREEN, width=3, dash='dash'),
                marker=dict(size=8),
                yaxis='y2'
            ))
            
            # Update layout
            fig.update_layout(
                title="Monthly Revenue & Active Customer Trends",
                xaxis_title="Month",
                yaxis_title="Revenue ($)",
                yaxis2=dict(
                    title="Number of Customers",
                    overlaying='y',
                    side='right'
                ),
                hovermode='x unified',
                height=450,
                template='plotly_white',
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show monthly stats table
            with st.expander("📊 View Monthly Performance Details"):
                display_stats = monthly_stats.copy()
                display_stats['revenue'] = display_stats['revenue'].apply(lambda x: f"${x:,.2f}")
                display_stats['avg_basket'] = display_stats['avg_basket'].apply(lambda x: f"${x:.2f}")
                st.dataframe(display_stats, use_container_width=True)
        else:
            st.info("No monthly data available for the selected date range")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # CUSTOMER FILTERS
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown("### 🔍 Customer Filters")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            segment_filter = st.multiselect("Customer Segment", options=rfm['segment'].unique(), default=[], key="segment_filter")
        with col2:
            min_spend = st.number_input("Minimum Spend ($)", min_value=0, value=0, step=50, key="min_spend")
        with col3:
            priority_filter = st.multiselect("Action Priority", options=['High', 'Medium', 'Low'], default=[], key="priority_filter")
        with col4:
            age_filter = st.multiselect("Age Group", options=rfm['age_group'].unique(), default=[], key="age_filter")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_customers = rfm.copy()
        if segment_filter:
            filtered_customers = filtered_customers[filtered_customers['segment'].isin(segment_filter)]
        if min_spend > 0:
            filtered_customers = filtered_customers[filtered_customers['monetary'] >= min_spend]
        if priority_filter:
            filtered_customers = filtered_customers[filtered_customers['priority'].isin(priority_filter)]
        if age_filter:
            filtered_customers = filtered_customers[filtered_customers['age_group'].isin(age_filter)]
        
        # =====================================================
        # COLLAPSIBLE CHARTS SECTION
        # =====================================================
        st.markdown("### 📊 Visual Analytics")
        st.markdown("*Click on any section below to view the chart*")
        
        # Chart 1: Customer Segments
        with st.expander("🍩 Customer Segments Distribution - Click to view"):
            col1, col2 = st.columns([2, 1])
            with col1:
                seg_counts = filtered_customers['segment'].value_counts().reset_index()
                seg_counts.columns = ['Segment', 'Count']
                fig = px.pie(seg_counts, values='Count', names='Segment', 
                             color_discrete_sequence=[SPAR_GREEN, SPAR_RED, '#FFA07A', '#D3D3D3', '#90EE90'],
                             hole=0.3)
                fig.update_layout(height=450, title="Customer Segments Distribution")
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.markdown(f"""
                <div style="padding: 20px; background: {SPAR_GRAY}; border-radius: 10px;">
                    <h4 style="color: {SPAR_RED}; margin-bottom: 15px;">Segment Insights</h4>
                    <p><strong>⭐ Active:</strong> Recently engaged, low priority</p>
                    <p><strong>⚠️ Warming:</strong> 30-60 days inactive, high priority</p>
                    <p><strong>⚠️ At Risk:</strong> 61-90 days inactive, urgent</p>
                    <p><strong>💔 Churned:</strong> 90+ days inactive, win-back needed</p>
                    <p><strong>🆕 One-Time:</strong> First-time buyers, convert them!</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Chart 2: Age Group Distribution
        with st.expander("👥 Age Group Distribution - Click to view"):
            col1, col2 = st.columns(2)
            with col1:
                age_counts = filtered_customers['age_group'].value_counts().reset_index()
                age_counts.columns = ['Age Group', 'Count']
                fig = px.bar(age_counts, x='Age Group', y='Count', title="Customers by Age Group",
                            color_discrete_sequence=[SPAR_GREEN],
                            text='Count')
                fig.update_traces(textposition='outside')
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                # At risk by age group
                at_risk_by_age = filtered_customers[filtered_customers['segment'].isin(['⚠️ At Risk', '⚠️ Warming'])].groupby('age_group').size().reset_index(name='count')
                if not at_risk_by_age.empty:
                    fig = px.bar(at_risk_by_age, x='age_group', y='count',
                                title="At-Risk Customers by Age Group",
                                color_discrete_sequence=[SPAR_RED],
                                text='count')
                    fig.update_traces(textposition='outside')
                    fig.update_layout(height=450)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No at-risk customers in selected data")
        
        # Chart 3: CLV Distribution
        with st.expander("💰 Customer Lifetime Value Distribution - Click to view"):
            col1, col2 = st.columns(2)
            with col1:
                fig = px.histogram(filtered_customers, x='clv', nbins=30, 
                                  title="CLV Distribution",
                                  color_discrete_sequence=[SPAR_GREEN],
                                  labels={'clv': 'Customer Lifetime Value ($)', 'count': 'Number of Customers'})
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                # CLV by segment
                clv_by_segment = filtered_customers.groupby('segment')['clv'].mean().reset_index()
                fig = px.bar(clv_by_segment, x='segment', y='clv', 
                            title="Average CLV by Segment",
                            color_discrete_sequence=[SPAR_RED],
                            labels={'clv': 'Avg CLV ($)', 'segment': 'Customer Segment'})
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
        
        # Chart 4: Churn Risk Distribution
        with st.expander("📊 Churn Risk Analysis - Click to view"):
            col1, col2 = st.columns(2)
            with col1:
                churn_dist = filtered_customers['churn_risk'].value_counts().reset_index()
                churn_dist.columns = ['Risk Level', 'Count']
                fig = px.bar(churn_dist, x='Risk Level', y='Count', 
                            title="Churn Risk Distribution",
                            color='Risk Level',
                            color_discrete_map={'Very Low Risk': SPAR_GREEN, 'Low Risk': '#90EE90', 
                                               'Medium Risk': '#FFA500', 'High Risk': SPAR_RED})
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                # Risk score distribution
                risk_dist = filtered_customers['risk_score'].value_counts().sort_index().reset_index()
                risk_dist.columns = ['Risk Score', 'Count']
                fig = px.bar(risk_dist, x='Risk Score', y='Count', 
                            title="Risk Score Distribution (0-100)",
                            color_discrete_sequence=[SPAR_RED])
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
        
        # INTELLIGENCE HUB WITH 5 TABS
        st.markdown("### 🧠 Intelligence Hub")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 CLV & Churn Details", "⏰ Time Patterns", "🎯 Campaign ROI", "🚨 Alerts", "📈 Benchmarks"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Average CLV", safe_currency_format(benchmarks['Avg CLV']))
                st.metric("High Value Customers (Platinum)", f"{campaign_metrics['high_value_customers']:,}")
            with col2:
                st.metric("Total CLV Value", safe_currency_format(filtered_customers['clv'].sum()))
                st.metric("Median CLV", safe_currency_format(filtered_customers['clv'].median()))
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(hourly_revenue, x='Hour', y='Revenue', title="Revenue by Hour",
                            color_discrete_sequence=[SPAR_RED])
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.bar(daily_patterns, x='Day', y='Revenue', title="Revenue by Day",
                            color_discrete_sequence=[SPAR_GREEN])
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Targetable Customers", f"{campaign_metrics['total_customers_targeted']:,}")
            with col2:
                st.metric("At-Risk + Warming Revenue", safe_currency_format(campaign_metrics['potential_revenue_at_risk']))
            with col3:
                st.metric("Est. Retention Value", safe_currency_format(campaign_metrics['estimated_retention_value']))
            
            st.markdown("---")
            st.markdown("#### 🎯 Segmentation Breakdown")
            seg_breakdown = filtered_customers['segment'].value_counts()
            st.dataframe(seg_breakdown, use_container_width=True)
        
        with tab4:
            for alert in alerts:
                if "CRITICAL" in alert:
                    st.error(alert)
                elif "WARNING" in alert or "ALERT" in alert:
                    st.warning(alert)
                else:
                    st.info(alert)
            if not alerts:
                st.success("✅ No active alerts. All metrics are within normal ranges!")
        
        with tab5:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Customers", f"{benchmarks['Total Customers']:,}")
                st.metric("Avg Customer Value", safe_currency_format(benchmarks['Avg Customer Value']))
                st.metric("Avg Frequency", f"{benchmarks['Avg Frequency']:.1f}")
                st.metric("Avg Recency (days)", f"{benchmarks['Avg Recency (days)']:.1f}")
            
            with col2:
                st.metric("Retention Rate", safe_percent_format(benchmarks['Retention Rate']))
                st.metric("Churn Rate", safe_percent_format(benchmarks['Churn Rate']))
                st.metric("Active Rate (30 days)", safe_percent_format(benchmarks['Active Rate (30 days)']))
                st.metric("Avg CLV", safe_currency_format(benchmarks['Avg CLV']))
        
        # ACTION CENTER
        st.markdown("### 🎯 Action Center")
        
        high_priority = filtered_customers[filtered_customers['priority'] == 'High'].head(10)
        medium_priority = filtered_customers[filtered_customers['priority'] == 'Medium'].head(5)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"#### 🔴 High Priority Actions ({len(filtered_customers[filtered_customers['priority']=='High'])})")
            for idx, row in high_priority.iterrows():
                bg_color = SPAR_RED if row['segment'] == '⚠️ At Risk' else "#FF8C00"
                monetary_val = safe_currency_format(row['monetary'])
                recency_days = int(row['recency']) if not pd.isna(row['recency']) else 0
                st.markdown(f"""
                <div class="action-card" style="background: linear-gradient(135deg, {bg_color} 0%, {bg_color}CC 100%);">
                    <h4>{row['recommended_action']}</h4>
                    <p>👤 Member: {row['member_number']} | 💰 {monetary_val} | ⏰ {recency_days} days ago | 📊 {row['segment']}</p>
                </div>
                """, unsafe_allow_html=True)
            if high_priority.empty:
                st.info("No high priority actions at this time")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"#### 🟡 Medium Priority Actions ({len(filtered_customers[filtered_customers['priority']=='Medium'])})")
            for idx, row in medium_priority.iterrows():
                monetary_val = safe_currency_format(row['monetary'])
                st.markdown(f"""
                <div class="action-card" style="background: linear-gradient(135deg, {SPAR_GREEN} 0%, {SPAR_LIGHT_GREEN} 100%);">
                    <h4>{row['recommended_action']}</h4>
                    <p>👤 Member: {row['member_number']} | 💰 {monetary_val} | ⭐ {row['segment']} | 🎂 {row['age_group']}</p>
                </div>
                """, unsafe_allow_html=True)
            if medium_priority.empty:
                st.info("No medium priority actions at this time")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # CUSTOMER INSIGHTS TABLE
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📋 Customer Insights Dashboard")
        
        display_cols = ['member_number', 'segment', 'age_group', 'clv_segment', 'churn_risk', 
                       'recency', 'frequency', 'monetary', 'avg_basket', 'risk_score', 'priority', 'recommended_action']
        
        display_df = filtered_customers[display_cols].copy()
        display_df['monetary'] = display_df['monetary'].apply(lambda x: safe_currency_format(x))
        display_df['avg_basket'] = display_df['avg_basket'].apply(lambda x: safe_currency_format(x))
        display_df['recency'] = display_df['recency'].apply(lambda x: f"{int(x)} days")
        display_df['frequency'] = display_df['frequency'].apply(lambda x: f"{int(x)}")
        display_df['risk_score'] = display_df['risk_score'].apply(lambda x: f"{int(x)}")
        
        st.dataframe(display_df, use_container_width=True, height=400)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # EXPORT SECTION
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = filtered_customers[display_cols].to_csv(index=False)
            st.download_button("📥 Download Filtered Data (CSV)", data=csv,
                              file_name=f"spar_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                              mime="text/csv", use_container_width=True)
        
        with col2:
            high_priority_export = filtered_customers[filtered_customers['priority'] == 'High'][['member_number', 'monetary', 'segment', 'recommended_action', 'recency']]
            if not high_priority_export.empty:
                high_priority_export['recency'] = high_priority_export['recency'].apply(lambda x: f"{int(x)} days")
                high_csv = high_priority_export.to_csv(index=False)
                st.download_button("🚨 Export High Priority List", data=high_csv,
                                  file_name="high_priority_customers.csv", mime="text/csv", use_container_width=True)
        
        with col3:
            # Export at risk and warming specifically
            risk_customers = filtered_customers[filtered_customers['segment'].isin(['⚠️ At Risk', '⚠️ Warming'])][['member_number', 'monetary', 'segment', 'recency']]
            if not risk_customers.empty:
                risk_customers['recency'] = risk_customers['recency'].apply(lambda x: f"{int(x)} days")
                risk_csv = risk_customers.to_csv(index=False)
                st.download_button("⚠️ Export At-Risk + Warming List", data=risk_csv,
                                  file_name="at_risk_warming_customers.csv", mime="text/csv", use_container_width=True)
        
        # TANAKA AI ASSISTANT IN SIDEBAR
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"### 🤖 Meet {tanaka.name} - Your AI Assistant")
            st.markdown(f"<p style='font-size:12px; color:#666;'>Ask {tanaka.name} anything about SPAR Rewards or your customer data!</p>", unsafe_allow_html=True)
            
            # Clear chat button
            if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
            
            st.markdown("---")
            
            # Display chat history
            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.chat_history[-10:]:  # Show last 10 messages
                    if msg["role"] == "user":
                        st.markdown(f"<div class='chat-message-user'><strong>You:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-message-assistant'><strong>🧠 {tanaka.name}:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
            
            # Chat input
            st.markdown("---")
            user_question = st.chat_input(f"Ask {tanaka.name} a question...", key="tanaka_chat_input")
            
            if user_question:
                # Add user message to history
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                
                # Get response from Tanaka
                response = tanaka.get_response(user_question, rfm, filtered_df)
                
                # Add assistant response to history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Rerun to update chat display
                st.rerun()
            
            # Quick questions buttons
            st.markdown("---")
            st.markdown("#### 💡 Quick Questions")
            
            quick_questions = [
                "How many at risk customers?",
                "What's our total revenue?",
                "How do I earn SPAR points?",
                "Show me monthly performance"
            ]
            
            for q in quick_questions:
                if st.button(q, key=f"quick_{q[:20]}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    response = tanaka.get_response(q, rfm, filtered_df)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <p style="color: #999; font-size: 12px;">
        SPAR Rewards Intelligence Hub | © 2024 SPAR Zimbabwe | 
        <a href="https://www.spar.co.zw/rewards" target="_blank" style="color: {SPAR_RED};">Official Website</a>
        </p>
    </div>
    """, unsafe_allow_html=True)