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
# SIMPLE CLEAN LOGIN FORM AT TOP
# =====================================================

def login_form():
    # Remove the duplicate key issue by using a unique key
    st.markdown("""
    <style>
    /* Hide default Streamlit elements only on login page */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Simple white background */
    .stApp {
        background-color: white;
    }
    
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
    }
    
    .login-card {
        background: white;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        width: 100%;
        max-width: 400px;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    
    .login-card h1 {
        color: #E31837;
        font-size: 24px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .login-card p {
        color: #666;
        font-size: 14px;
        margin-bottom: 30px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        padding: 10px 14px;
        border: 1px solid #ddd;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #E31837;
        box-shadow: 0 0 0 2px rgba(227,24,55,0.1);
    }
    
    .stButton > button {
        width: 100%;
        background-color: #E31837;
        color: white;
        border-radius: 8px;
        height: 44px;
        font-weight: 600;
        border: none;
        margin-top: 10px;
    }
    
    .stButton > button:hover {
        background-color: #B8102E;
        transform: translateY(-1px);
    }
    
    .stAlert {
        border-radius: 8px;
        margin-top: 15px;
    }
    </style>
    
    <div class="login-container">
        <div class="login-card">
            <h1>🎯 SPAR Rewards Intelligence Hub</h1>
            <p>Enter your password to access the dashboard</p>
    """, unsafe_allow_html=True)
    
    # Use a unique key for the password input
    password = st.text_input("", placeholder="Enter password", type="password", key="login_password_input", label_visibility="collapsed")
    
    if st.button("Access Dashboard", key="login_button", use_container_width=True):
        if verify_password(password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.session_state.login_attempt += 1
            st.error(f"❌ Incorrect password. Please try again.")
    
    st.markdown("""
        </div>
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
# CHURN PREDICTION
# =====================================================
@st.cache_data
def calculate_churn_probability(rfm):
    rfm['churn_score'] = (
        (rfm['recency'] / max(rfm['recency'].max(), 1)) * 0.5 +
        (1 - rfm['frequency'] / max(rfm['frequency'].max(), 1)) * 0.3 +
        (1 - rfm['monetary'] / max(rfm['monetary'].max(), 1)) * 0.2
    )
    rfm['churn_risk'] = pd.cut(rfm['churn_score'], bins=[0, 0.3, 0.6, 1], labels=['Low Risk', 'Medium Risk', 'High Risk'])
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
        'potential_revenue_at_risk': rfm[rfm['segment'] == '⚠️ At Risk']['monetary'].sum(),
        'estimated_retention_value': rfm[rfm['segment'] == '⚠️ At Risk']['monetary'].sum() * 0.3,
    }

# =====================================================
# GENERATE ALERTS
# =====================================================
def generate_alerts(rfm):
    alerts = []
    at_risk = len(rfm[rfm['segment'] == '⚠️ At Risk'])
    if at_risk > 50:
        alerts.append(f"⚠️ WARNING: {at_risk} customers are at risk of churning!")
    champions = len(rfm[rfm['segment'] == '👑 Champions'])
    if champions < 10:
        alerts.append(f"💡 OPPORTUNITY: Only {champions} champions. Grow this segment!")
    return alerts

# =====================================================
# BENCHMARKS
# =====================================================
def calculate_benchmarks(rfm):
    return {
        'Total Customers': len(rfm),
        'Avg Customer Value': rfm['monetary'].mean(),
        'Retention Rate': len(rfm[rfm['frequency'] > 1]) / len(rfm) * 100 if len(rfm) > 0 else 0,
        'Churn Rate': len(rfm[rfm['segment'] == '💔 Churned']) / len(rfm) * 100 if len(rfm) > 0 else 0,
        'Active Rate': len(rfm[rfm['recency'] <= 30]) / len(rfm) * 100 if len(rfm) > 0 else 0,
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
# SEGMENTATION
# =====================================================
def segment_customers(rfm):
    conditions = [
        (rfm['r_score'] >= 3) & (rfm['f_score'] >= 3) & (rfm['m_score'] >= 3),
        (rfm['r_score'] >= 3) & (rfm['f_score'] >= 2),
        (rfm['r_score'] >= 2) & (rfm['f_score'] >= 2),
        (rfm['frequency'] == 1),
        (rfm['recency'] > 60) & (rfm['recency'] <= 90),
        (rfm['recency'] > 90)
    ]
    choices = ["👑 Champions", "⭐ Loyal", "🌱 Potential", "🆕 One-Time", "⚠️ At Risk", "💔 Churned"]
    rfm['segment'] = np.select(conditions, choices, default="📊 Others")
    rfm['risk_score'] = 0
    rfm.loc[rfm['segment'] == '⚠️ At Risk', 'risk_score'] = 70
    rfm.loc[rfm['segment'] == '💔 Churned', 'risk_score'] = 90
    return rfm

# =====================================================
# ACTION ENGINE
# =====================================================
def generate_actions(rfm):
    actions, priorities = [], []
    for idx, row in rfm.iterrows():
        if row['segment'] == '⚠️ At Risk':
            actions.append("🚨 Send 25% discount coupon")
            priorities.append("High")
        elif row['segment'] == '💔 Churned':
            actions.append("🔄 Re-engagement campaign")
            priorities.append("High")
        elif row['segment'] == '🆕 One-Time':
            actions.append("🎁 Welcome back incentive")
            priorities.append("Medium")
        elif row['segment'] == '⭐ Loyal':
            actions.append("🏆 Loyalty points bonus")
            priorities.append("Medium")
        elif row['segment'] == '👑 Champions':
            actions.append("💎 VIP early access")
            priorities.append("Low")
        else:
            actions.append("📈 Nurture engagement")
            priorities.append("Low")
    rfm['recommended_action'] = actions
    rfm['priority'] = priorities
    return rfm

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
        return f"⚠️ **At Risk Customers:** {at_risk} members need attention"
    return None

# =====================================================
# HEADER WITH LOGOUT BUTTON
# =====================================================
if st.session_state.authenticated:
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

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    if st.session_state.authenticated:
        st.markdown(f"<h3 style='color:{SPAR_RED};'>📂 Upload Data</h3>", unsafe_allow_html=True)
        file = st.file_uploader("Choose CSV file", type=["csv"], key="file_uploader")
        
        if file:
            st.success("✅ File loaded successfully")

# =====================================================
# MAIN DASHBOARD
# =====================================================
if not st.session_state.authenticated:
    login_form()
elif not file:
    # Welcome screen
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
    # Load and process data
    df = pd.read_csv(file)
    df = clean_data(df)
    
    if df.empty:
        st.error("❌ No valid data found. Please check your file format.")
        st.stop()
    
    # Date slicer
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown("### 📅 Date Slicer")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        available_years = sorted(df['year'].unique(), reverse=True)
        selected_years = st.multiselect("Select Year(s)", options=available_years, default=available_years if len(available_years) <= 3 else [available_years[0]], key="year_select")
    with col2:
        months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                  7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        available_months = sorted(df['month'].unique())
        selected_months = st.multiselect("Select Month(s)", options=available_months, default=available_months, format_func=lambda x: months.get(x, str(x)), key="month_select")
    with col3:
        available_days = sorted(df['day'].unique())
        selected_days = st.multiselect("Select Day(s)", options=available_days, default=available_days, format_func=lambda x: f"{x:02d}", key="day_select")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
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
    
    # Calculate metrics
    rfm = calculate_rfm(filtered_df)
    rfm = segment_customers(rfm)
    rfm = generate_actions(rfm)
    rfm = calculate_clv(rfm)
    rfm = calculate_churn_probability(rfm)
    rfm = rfm.reset_index()
    
    hourly_revenue, daily_patterns = add_time_insights(filtered_df)
    campaign_metrics = calculate_campaign_impact(rfm)
    alerts = generate_alerts(rfm)
    benchmarks = calculate_benchmarks(rfm)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    def card(title, value, icon=""):
        st.markdown(f"""
        <div class="metric-card">
            <div class="big-number">{icon}{value}</div>
            <div class="label">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col1:
        card("Total Customers", f"{len(rfm):,}", "👥 ")
    with col2:
        card("Total Revenue", f"${rfm['monetary'].sum():,.0f}", "💰 ")
    with col3:
        card("Avg. CLV", f"${rfm['clv'].mean():,.0f}", "💎 ")
    with col4:
        at_risk_count = len(rfm[rfm['segment'].isin(['⚠️ At Risk', '💔 Churned'])])
        card("At Risk", f"{at_risk_count}", "⚠️ ")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Customer Filters
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
    
    # Apply customer filters
    filtered_customers = rfm.copy()
    if segment_filter:
        filtered_customers = filtered_customers[filtered_customers['segment'].isin(segment_filter)]
    if min_spend > 0:
        filtered_customers = filtered_customers[filtered_customers['monetary'] >= min_spend]
    if priority_filter:
        filtered_customers = filtered_customers[filtered_customers['priority'].isin(priority_filter)]
    if age_filter:
        filtered_customers = filtered_customers[filtered_customers['age_group'].isin(age_filter)]
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Customer Segments")
        seg_counts = filtered_customers['segment'].value_counts().reset_index()
        seg_counts.columns = ['Segment', 'Count']
        fig = px.pie(seg_counts, values='Count', names='Segment', 
                     color_discrete_sequence=[SPAR_RED, SPAR_GREEN, '#FFB6C1', '#90EE90', '#FFA07A', '#D3D3D3'],
                     hole=0.3)
        fig.update_layout(height=400)
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
    
    # Intelligence Hub
    st.markdown("### 🧠 Intelligence Hub")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 CLV & Churn", "⏰ Time Patterns", "🎯 Campaign ROI", "🚨 Alerts"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(filtered_customers, x='clv', nbins=30, title="CLV Distribution",
                              color_discrete_sequence=[SPAR_GREEN])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(filtered_customers.groupby('segment')['churn_risk'].value_counts().unstack().fillna(0), use_container_width=True)
    
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
            st.metric("At-Risk Revenue", f"${campaign_metrics['potential_revenue_at_risk']:,.0f}")
        with col3:
            st.metric("Est. Retention Value", f"${campaign_metrics['estimated_retention_value']:,.0f}")
    
    with tab4:
        for alert in alerts:
            if "WARNING" in alert:
                st.warning(alert)
            else:
                st.info(alert)
        if not alerts:
            st.success("✅ No active alerts!")
    
    # Action Center
    st.markdown("### 🎯 Action Center")
    
    high_priority = filtered_customers[filtered_customers['priority'] == 'High'].head(5)
    medium_priority = filtered_customers[filtered_customers['priority'] == 'Medium'].head(5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"#### 🔴 High Priority ({len(filtered_customers[filtered_customers['priority']=='High'])})")
        for idx, row in high_priority.iterrows():
            st.markdown(f"""
            <div class="action-card">
                <h4>{row['recommended_action']}</h4>
                <p>Member: {row['member_number']} | ${row['monetary']:,.0f} | {row['recency']} days ago</p>
            </div>
            """, unsafe_allow_html=True)
        if high_priority.empty:
            st.info("No high priority actions")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"#### 🟡 Medium Priority ({len(filtered_customers[filtered_customers['priority']=='Medium'])})")
        for idx, row in medium_priority.iterrows():
            st.markdown(f"""
            <div class="action-card" style="background: linear-gradient(135deg, {SPAR_GREEN} 0%, {SPAR_LIGHT_GREEN} 100%);">
                <h4>{row['recommended_action']}</h4>
                <p>Member: {row['member_number']} | ${row['monetary']:,.0f} | {row['segment']}</p>
            </div>
            """, unsafe_allow_html=True)
        if medium_priority.empty:
            st.info("No medium priority actions")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Customer Table
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📋 Customer Insights")
    
    display_cols = ['member_number', 'segment', 'age_group', 'clv_segment', 'churn_risk', 
                   'recency', 'frequency', 'monetary', 'priority', 'recommended_action']
    
    display_df = filtered_customers[display_cols].copy()
    display_df['monetary'] = display_df['monetary'].apply(lambda x: f"${x:,.2f}")
    display_df['recency'] = display_df['recency'].apply(lambda x: f"{x} days")
    
    st.dataframe(display_df, use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Export
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_customers[display_cols].to_csv(index=False)
        st.download_button("📥 Download Data (CSV)", data=csv,
                          file_name=f"spar_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                          mime="text/csv", use_container_width=True)
    
    with col2:
        high_csv = filtered_customers[filtered_customers['priority'] == 'High'][['member_number', 'monetary', 'recommended_action']].to_csv(index=False)
        st.download_button("🚨 Export High Priority", data=high_csv,
                          file_name="high_priority_customers.csv", mime="text/csv", use_container_width=True)
    
    # AI Assistant in Sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🤖 SPAR AI Assistant")
        
        if "ai_messages" not in st.session_state:
            st.session_state.ai_messages = [{"role": "assistant", "content": "👋 Ask me about SPAR Rewards or your data!"}]
        
        for msg in st.session_state.ai_messages[-3:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if user_question := st.chat_input("Ask me...", key="chat_input"):
            st.session_state.ai_messages.append({"role": "user", "content": user_question})
            
            response = get_spar_info_response(user_question)
            if not response:
                response = get_data_response(user_question, rfm, filtered_df)
            if not response:
                response = "Ask about SPAR Rewards, customer segments, revenue, or at-risk customers!"
            
            st.session_state.ai_messages.append({"role": "assistant", "content": response})
            st.rerun()

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px;">
    <p style="color: #999; font-size: 12px;">
    SPAR Rewards Intelligence Hub | © 2024 SPAR Zimbabwe
    </p>
</div>
""", unsafe_allow_html=True)