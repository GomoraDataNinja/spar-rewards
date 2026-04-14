import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import hashlib

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
# MODERN UI STYLING
# =====================================================
st.markdown(f"""
<style>
    /* Main container */
    .main {{
        background-color: {SPAR_GRAY};
    }}
    
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 2rem;
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
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-weight: bold;
        font-size: 32px;
        margin-bottom: 5px;
        color: {SPAR_RED};
        letter-spacing: -0.5px;
        text-align: center;
    }}
    
    .header p {{
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 14px;
        color: #666;
        margin-top: 5px;
        text-align: center;
    }}
    
    /* Card styling */
    .card {{
        background-color: {SPAR_WHITE};
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        transition: transform 0.2s;
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
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-weight: bold;
        font-size: 32px;
        color: {SPAR_RED};
        margin-bottom: 5px;
    }}
    
    .label {{
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 13px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
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
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-weight: bold;
        margin: 0 0 5px 0;
        font-size: 14px;
    }}
    
    .action-card p {{
        margin: 0;
        font-size: 12px;
        opacity: 0.9;
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
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-weight: bold;
        border-radius: 8px;
        transition: all 0.3s;
    }}
    
    .stButton > button:hover {{
        background-color: {SPAR_DARK_RED};
        transform: translateY(-1px);
        box-shadow: 0px 2px 8px rgba(227,24,55,0.3);
    }}
    
    /* Dataframe styling */
    .dataframe {{
        font-family: 'Arial', 'Helvetica', sans-serif;
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
    
    # Alert 4: Champions growth opportunity
    champions = len(rfm[rfm['segment'] == '👑 Champions'])
    if champions < 10:
        alerts.append(f"💡 OPPORTUNITY: Only {champions} champions. Focus on loyalty program to grow this segment.")
    
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
    try:
        rfm['r_score'] = pd.qcut(rfm['recency'].rank(method='first'), 4, labels=[4,3,2,1])
        rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1,2,3,4])
        rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), 4, labels=[1,2,3,4])
    except:
        rfm['r_score'] = pd.cut(rfm['recency'], bins=4, labels=[4,3,2,1])
        rfm['f_score'] = pd.cut(rfm['frequency'], bins=4, labels=[1,2,3,4])
        rfm['m_score'] = pd.cut(rfm['monetary'], bins=4, labels=[1,2,3,4])
    return rfm

# =====================================================
# SEGMENTATION - FIXED WITH PROPER AT RISK LOGIC
# =====================================================
def segment_customers(rfm):
    """
    IMPROVED SEGMENTATION:
    - Uses churn_score for risk assessment
    - Adds 'Warming' stage (30-60 days)
    - 'At Risk' for 60-90 days OR high churn_score
    """
    # Ensure churn_score exists
    if 'churn_score' not in rfm.columns:
        rfm['churn_score'] = 0
    
    conditions = [
        # Champions: High RFM scores
        (rfm['r_score'] >= 3) & (rfm['f_score'] >= 3) & (rfm['m_score'] >= 3),
        
        # Loyal: Good recency and frequency
        (rfm['r_score'] >= 3) & (rfm['f_score'] >= 2),
        
        # Potential: Moderate engagement
        (rfm['r_score'] >= 2) & (rfm['f_score'] >= 2),
        
        # One-Time: First purchase only
        (rfm['frequency'] == 1),
        
        # ⚠️ WARMING: Early warning signs (30-60 days inactive) OR medium churn risk
        ((rfm['recency'] > 30) & (rfm['recency'] <= 60)) | ((rfm['churn_score'] > 0.4) & (rfm['churn_score'] <= 0.6)),
        
        # ⚠️ AT RISK: 60-90 days inactive OR high churn risk
        ((rfm['recency'] > 60) & (rfm['recency'] <= 90)) | (rfm['churn_score'] > 0.6),
        
        # 💔 CHURNED: Over 90 days
        (rfm['recency'] > 90)
    ]
    
    choices = [
        "👑 Champions",      # Top tier
        "⭐ Loyal",          # Regular customers
        "🌱 Potential",      # Growing engagement
        "🆕 One-Time",       # New/one-time buyers
        "⚠️ Warming",        # NEW: Early risk signs (30-60 days or medium churn)
        "⚠️ At Risk",        # FIXED: True at risk (60-90 days or high churn)
        "💔 Churned"         # Lost customers
    ]
    
    # Use select with default for unmatched
    rfm['segment'] = np.select(conditions, choices, default="📊 Others")
    
    # Risk scoring based on segment
    risk_map = {
        '👑 Champions': 0,
        '⭐ Loyal': 10,
        '🌱 Potential': 25,
        '🆕 One-Time': 40,
        '⚠️ Warming': 60,
        '⚠️ At Risk': 80,
        '💔 Churned': 95,
        '📊 Others': 50
    }
    rfm['risk_score'] = rfm['segment'].map(risk_map)
    
    return rfm

# =====================================================
# ACTION ENGINE - UPDATED FOR NEW SEGMENTS
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
        elif row['segment'] == '⭐ Loyal':
            actions.append("🏆 Loyalty points bonus + referral program")
            priorities.append("Medium")
        elif row['segment'] == '👑 Champions':
            actions.append("💎 VIP early access + exclusive events")
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
        # Convert to int first, then format
        return f"{int(float(day)):02d}"
    except:
        return "01"

# =====================================================
# AI ASSISTANT KNOWLEDGE BASE
# =====================================================
def get_spar_info_response(question):
    q = question.lower()
    if 'spar rewards' in q or 'what is spar' in q:
        return "🎯 **SPAR Rewards** is a customer loyalty program offering points on purchases, exclusive discounts, and birthday rewards. Join free at any SPAR store!"
    elif 'how to join' in q or 'sign up' in q:
        return "📝 **Join SPAR Rewards:** Visit any SPAR store, fill registration form, receive member number, start earning points instantly!"
    elif 'earn points' in q:
        return "⭐ **Earn points:** 1 point per $1 spent, double points on birthdays, bonus points on promotions!"
    elif 'redeem' in q:
        return "🎁 **Redeem points:** 100 points = $5 voucher, 500 points = $30 voucher. Ask cashier to check balance!"
    else:
        return None

def get_data_response(question, rfm, df):
    q = question.lower()
    if 'total customers' in q:
        return f"👥 **Total Customers:** {len(rfm):,} members"
    elif 'total revenue' in q:
        return f"💰 **Total Revenue:** ${rfm['monetary'].sum():,.2f}"
    elif 'at risk' in q:
        at_risk = len(rfm[rfm['segment'] == '⚠️ At Risk'])
        warming = len(rfm[rfm['segment'] == '⚠️ Warming'])
        return f"⚠️ **At Risk Customers:** {at_risk} members need urgent attention\n⚡ **Warming Up:** {warming} members showing early warning signs"
    elif 'churned' in q:
        churned = len(rfm[rfm['segment'] == '💔 Churned'])
        return f"💔 **Churned Customers:** {churned} members have stopped engaging (>90 days)"
    elif 'warming' in q:
        warming = len(rfm[rfm['segment'] == '⚠️ Warming'])
        return f"⚡ **Warming Customers:** {warming} members inactive 30-60 days - intervene now!"
    return None

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
            # Convert to int and filter out NaN
            available_years = [int(y) for y in available_years if pd.notna(y)]
            selected_years = st.multiselect("Select Year(s)", options=available_years, default=available_years if len(available_years) <= 3 else [available_years[0]], key="year_select")
        
        with col2:
            months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                      7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
            available_months = sorted(df['month'].unique())
            # Convert to int and filter out NaN
            available_months = [int(m) for m in available_months if pd.notna(m)]
            selected_months = st.multiselect("Select Month(s)", options=available_months, default=available_months, format_func=lambda x: months.get(x, str(x)), key="month_select")
        
        with col3:
            available_days = sorted(df['day'].unique())
            # Convert to int and filter out NaN
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
        
        # Calculate all metrics (order matters now)
        rfm = calculate_rfm(filtered_df)
        rfm = calculate_churn_probability(rfm)  # Calculate churn score FIRST
        rfm = segment_customers(rfm)            # Then segment using churn_score
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
        
        # CHARTS SECTION
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 Customer Segments")
            seg_counts = filtered_customers['segment'].value_counts().reset_index()
            seg_counts.columns = ['Segment', 'Count']
            fig = px.pie(seg_counts, values='Count', names='Segment', 
                         color_discrete_sequence=[SPAR_RED, SPAR_GREEN, '#FFB6C1', '#90EE90', '#FFA07A', '#D3D3D3', '#FF6B6B'],
                         hole=0.3)
            fig.update_layout(height=400)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("👥 Age Group Distribution")
            age_counts = filtered_customers['age_group'].value_counts().reset_index()
            age_counts.columns = ['Age Group', 'Count']
            fig = px.bar(age_counts, x='Age Group', y='Count', title="Customers by Age Group",
                        color_discrete_sequence=[SPAR_GREEN])
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # INTELLIGENCE HUB WITH 5 TABS
        st.markdown("### 🧠 Intelligence Hub")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 CLV & Churn", "⏰ Time Patterns", "🎯 Campaign ROI", "🚨 Alerts", "📈 Benchmarks"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.histogram(filtered_customers, x='clv', nbins=30, title="Customer Lifetime Value Distribution",
                                  color_discrete_sequence=[SPAR_GREEN])
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                # Show churn risk distribution
                churn_dist = filtered_customers['churn_risk'].value_counts().reset_index()
                churn_dist.columns = ['Churn Risk', 'Count']
                fig = px.bar(churn_dist, x='Churn Risk', y='Count', title="Churn Risk Distribution",
                            color_discrete_sequence=[SPAR_RED])
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
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
            
            # Show breakdown
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
        
        high_priority = filtered_customers[filtered_customers['priority'] == 'High'].head(5)
        medium_priority = filtered_customers[filtered_customers['priority'] == 'Medium'].head(5)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"#### 🔴 High Priority Actions ({len(filtered_customers[filtered_customers['priority']=='High'])})")
            for idx, row in high_priority.iterrows():
                # Color code by segment
                bg_color = "#E31837" if row['segment'] == '⚠️ At Risk' else "#FF8C00"
                monetary_val = safe_currency_format(row['monetary'])
                st.markdown(f"""
                <div class="action-card" style="background: linear-gradient(135deg, {bg_color} 0%, {bg_color}CC 100%);">
                    <h4>{row['recommended_action']}</h4>
                    <p>👤 Member: {row['member_number']} | 💰 {monetary_val} | ⏰ {int(row['recency'])} days ago | 📊 {row['segment']} | 🎯 Risk: {row['churn_risk']}</p>
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
            high_priority_export = filtered_customers[filtered_customers['priority'] == 'High'][['member_number', 'monetary', 'segment', 'recommended_action', 'churn_risk']]
            if not high_priority_export.empty:
                high_csv = high_priority_export.to_csv(index=False)
                st.download_button("🚨 Export High Priority List", data=high_csv,
                                  file_name="high_priority_customers.csv", mime="text/csv", use_container_width=True)
        
        with col3:
            # Export at risk and warming specifically
            risk_customers = filtered_customers[filtered_customers['segment'].isin(['⚠️ At Risk', '⚠️ Warming'])][['member_number', 'monetary', 'segment', 'recency', 'churn_risk']]
            if not risk_customers.empty:
                risk_csv = risk_customers.to_csv(index=False)
                st.download_button("⚠️ Export At-Risk + Warming List", data=risk_csv,
                                  file_name="at_risk_warming_customers.csv", mime="text/csv", use_container_width=True)
        
        # AI ASSISTANT IN SIDEBAR
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🤖 SPAR AI Assistant")
            
            if "ai_messages" not in st.session_state:
                st.session_state.ai_messages = [{"role": "assistant", "content": "👋 Hi! I'm your SPAR Rewards AI assistant. Ask me about SPAR Rewards or your data insights!"}]
            
            for msg in st.session_state.ai_messages[-5:]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            if user_question := st.chat_input("Ask me anything...", key="chat_input"):
                st.session_state.ai_messages.append({"role": "user", "content": user_question})
                
                response = get_spar_info_response(user_question)
                if not response and 'rfm' in locals():
                    response = get_data_response(user_question, rfm, filtered_df)
                if not response:
                    response = "I can help with SPAR Rewards info or analyze your customer data! Try asking about segments, revenue, at risk customers, warming customers, or churned customers."
                
                st.session_state.ai_messages.append({"role": "assistant", "content": response})
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
