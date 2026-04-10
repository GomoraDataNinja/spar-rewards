import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import io

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="SPAR Rewards Intelligence",
    page_icon="🎯",
    layout="wide"
)

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
# MODERN UI STYLING WITH SPAR COLORS & ARIAL BOLD
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
    
    /* Header styling - Arial Bold */
    .header {{
        background: linear-gradient(135deg, {SPAR_WHITE} 0%, {SPAR_GRAY} 100%);
        padding: 20px 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border-left: 5px solid {SPAR_RED};
    }}
    
    .header h1 {{
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-weight: bold;
        font-size: 32px;
        margin-bottom: 5px;
        color: {SPAR_RED};
        letter-spacing: -0.5px;
    }}
    
    .header p {{
        font-family: 'Arial', 'Helvetica', sans-serif;
        font-size: 14px;
        color: #666;
        margin-top: 5px;
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
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER WITH ARIAL BOLD
# =====================================================
col1, col2 = st.columns([1, 8])

with col1:
    try:
        st.image("spar_logo.png", width=70)
    except:
        st.markdown(f"<h1 style='color:{SPAR_RED}; font-size:40px;'>SPAR</h1>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="header">
        <h1>SPAR Rewards Intelligence</h1>
        <p>🎯 Customer behavior analysis • Retention strategies • Revenue optimization</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DATA CLEANING (UPDATED FOR YOUR COLUMNS)
# =====================================================
@st.cache_data
def clean_data(df):
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    # Map your specific columns
    if 'member_number' not in df.columns:
        # Try alternative names
        for col in ['member no', 'member', 'customer_id', 'customer']:
            if col in df.columns:
                df.rename(columns={col: 'member_number'}, inplace=True)
                break
    
    if 'creation_date' not in df.columns:
        for col in ['date', 'transaction_date', 'created_date']:
            if col in df.columns:
                df.rename(columns={col: 'creation_date'}, inplace=True)
                break
    
    if 'redeeming_basket_value' in df.columns:
        df.rename(columns={'redeeming_basket_value': 'basket_value'}, inplace=True)
    
    # Convert data types
    df['creation_date'] = pd.to_datetime(df['creation_date'], errors='coerce')
    df['basket_value'] = pd.to_numeric(df['basket_value'], errors='coerce')
    
    # Clean data
    df = df[df['basket_value'] > 0]
    df = df[df['member_number'].notna()]
    df = df[df['creation_date'].notna()]
    
    # Filter to redeemed only if status exists
    if 'status' in df.columns:
        df = df[df['status'].str.lower() == 'redeemed']
    
    return df

# =====================================================
# RFM CALCULATION
# =====================================================
@st.cache_data
def calculate_rfm(df):
    ref_date = df['creation_date'].max()
    
    rfm = df.groupby('member_number').agg(
        recency=('creation_date', lambda x: (ref_date - x.max()).days),
        frequency=('member_number', 'count'),
        monetary=('basket_value', 'sum'),
        avg_basket=('basket_value', 'mean'),
        last_purchase=('creation_date', 'max')
    )
    
    # Handle potential qcut errors
    try:
        rfm['r_score'] = pd.qcut(rfm['recency'].rank(method='first'), 4, labels=[4,3,2,1])
        rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1,2,3,4])
        rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), 4, labels=[1,2,3,4])
    except:
        rfm['r_score'] = pd.cut(rfm['recency'], bins=4, labels=[4,3,2,1])
        rfm['f_score'] = pd.cut(rfm['frequency'], bins=4, labels=[1,2,3,4])
        rfm['m_score'] = pd.cut(rfm['monetary'], bins=4, labels=[1,2,3,4])
    
    rfm[['r_score','f_score','m_score']] = rfm[['r_score','f_score','m_score']].astype(int)
    
    return rfm

# =====================================================
# ENHANCED SEGMENTATION
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
    
    # Calculate risk score
    rfm['risk_score'] = 0
    rfm.loc[rfm['segment'] == '⚠️ At Risk', 'risk_score'] = 70
    rfm.loc[rfm['segment'] == '💔 Churned', 'risk_score'] = 90
    rfm.loc[rfm['segment'] == '🆕 One-Time', 'risk_score'] = 50
    rfm.loc[rfm['recency'] > 45, 'risk_score'] += 20
    
    return rfm

# =====================================================
# ACTION ENGINE
# =====================================================
def generate_actions(rfm):
    actions = []
    priorities = []
    
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
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown(f"<h3 style='color:{SPAR_RED};'>📂 Upload Data</h3>", unsafe_allow_html=True)
    file = st.file_uploader("Choose CSV file", type=["csv"])
    
    if file:
        st.success("✅ File loaded successfully")
        
        # Quick stats preview
        if 'df' in locals():
            st.markdown("---")
            st.markdown(f"<small>📊 {len(df):,} transactions</small>", unsafe_allow_html=True)
            st.markdown(f"<small>👥 {df['member_number'].nunique():,} customers</small>", unsafe_allow_html=True)

# =====================================================
# MAIN DASHBOARD
# =====================================================
if file:
    # Load and process data
    df = pd.read_csv(file)
    df = clean_data(df)
    
    if df.empty:
        st.error("❌ No valid data found. Please check your file format.")
        st.stop()
    
    # Calculate metrics
    rfm = calculate_rfm(df)
    rfm = segment_customers(rfm)
    rfm = generate_actions(rfm)
    rfm = rfm.reset_index()
    
    # =====================================================
    # KPI CARDS
    # =====================================================
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
        card("Avg. Customer Value", f"${rfm['monetary'].mean():,.0f}", "⭐ ")
    with col4:
        at_risk_count = len(rfm[rfm['segment'].isin(['⚠️ At Risk', '💔 Churned'])])
        card("At Risk / Churned", f"{at_risk_count}", "⚠️ ")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =====================================================
    # FILTERS ROW (LIKE POWER BI)
    # =====================================================
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown("### 🔍 Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        segment_filter = st.multiselect(
            "Customer Segment",
            options=rfm['segment'].unique(),
            default=[]
        )
    
    with col2:
        min_spend = st.number_input("Minimum Spend ($)", min_value=0, value=0, step=50)
    
    with col3:
        priority_filter = st.multiselect(
            "Action Priority",
            options=['High', 'Medium', 'Low'],
            default=[]
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = rfm.copy()
    if segment_filter:
        filtered_df = filtered_df[filtered_df['segment'].isin(segment_filter)]
    if min_spend > 0:
        filtered_df = filtered_df[filtered_df['monetary'] >= min_spend]
    if priority_filter:
        filtered_df = filtered_df[filtered_df['priority'].isin(priority_filter)]
    
    # =====================================================
    # CHARTS SECTION
    # =====================================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Customer Segments")
        seg_counts = filtered_df['segment'].value_counts().reset_index()
        seg_counts.columns = ['Segment', 'Count']
        fig = px.pie(seg_counts, values='Count', names='Segment', 
                     color_discrete_sequence=[SPAR_RED, SPAR_GREEN, '#FFB6C1', '#90EE90', '#FFA07A', '#D3D3D3'],
                     hole=0.3)
        fig.update_layout(showlegend=True, height=400)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 Recency Distribution")
        fig = px.histogram(filtered_df, x='recency', nbins=30,
                          title="Days Since Last Purchase",
                          color_discrete_sequence=[SPAR_GREEN])
        fig.update_layout(xaxis_title="Days", yaxis_title="Number of Customers", height=400)
        fig.add_vline(x=30, line_dash="dash", line_color="orange", annotation_text="30 days")
        fig.add_vline(x=60, line_dash="dash", line_color="red", annotation_text="60 days")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Second row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💰 Revenue by Segment")
        segment_revenue = filtered_df.groupby('segment')['monetary'].sum().reset_index()
        fig = px.bar(segment_revenue, x='segment', y='monetary',
                    title="Total Revenue per Segment",
                    color='segment',
                    color_discrete_sequence=[SPAR_RED, SPAR_GREEN, '#FFB6C1', '#90EE90', '#FFA07A', '#D3D3D3'])
        fig.update_layout(xaxis_tickangle=-45, height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔄 Frequency Analysis")
        freq_dist = filtered_df['frequency'].value_counts().sort_index().head(20).reset_index()
        freq_dist.columns = ['Transactions', 'Customers']
        fig = px.line(freq_dist, x='Transactions', y='Customers',
                     title="Customer Transaction Frequency",
                     markers=True,
                     color_discrete_sequence=[SPAR_RED])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # =====================================================
    # ACTION CENTER PANEL
    # =====================================================
    st.markdown("### 🎯 Action Center")
    
    # Top priority actions
    high_priority = filtered_df[filtered_df['priority'] == 'High'].head(5)
    medium_priority = filtered_df[filtered_df['priority'] == 'Medium'].head(5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"#### 🔴 High Priority Actions ({len(filtered_df[filtered_df['priority']=='High'])})")
        
        if not high_priority.empty:
            for idx, row in high_priority.iterrows():
                st.markdown(f"""
                <div class="action-card">
                    <h4>{row['recommended_action']}</h4>
                    <p>👤 Member: {row['member_number']} | 💰 ${row['monetary']:,.0f} | ⏰ {row['recency']} days ago</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No high priority actions at this time")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"#### 🟡 Medium Priority Actions ({len(filtered_df[filtered_df['priority']=='Medium'])})")
        
        if not medium_priority.empty:
            for idx, row in medium_priority.iterrows():
                st.markdown(f"""
                <div class="action-card" style="background: linear-gradient(135deg, {SPAR_GREEN} 0%, {SPAR_LIGHT_GREEN} 100%);">
                    <h4>{row['recommended_action']}</h4>
                    <p>👤 Member: {row['member_number']} | 💰 ${row['monetary']:,.0f} | ⭐ {row['segment']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No medium priority actions at this time")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # =====================================================
    # CUSTOMER INSIGHTS TABLE
    # =====================================================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📋 Customer Insights Dashboard")
    
    # Display table with key columns
    display_cols = ['member_number', 'segment', 'recency', 'frequency', 'monetary', 
                   'avg_basket', 'risk_score', 'priority', 'recommended_action']
    
    # Format for display
    display_df = filtered_df[display_cols].copy()
    display_df['monetary'] = display_df['monetary'].apply(lambda x: f"${x:,.2f}")
    display_df['avg_basket'] = display_df['avg_basket'].apply(lambda x: f"${x:,.2f}")
    display_df['recency'] = display_df['recency'].apply(lambda x: f"{x} days")
    
    st.dataframe(display_df, use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # =====================================================
    # EXPORT SECTION
    # =====================================================
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export filtered data
        csv = filtered_df[display_cols].to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name=f"spar_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Export high priority actions
        high_priority_export = filtered_df[filtered_df['priority'] == 'High'][['member_number', 'monetary', 'recommended_action']]
        if not high_priority_export.empty:
            high_csv = high_priority_export.to_csv(index=False)
            st.download_button(
                label="🚨 Export High Priority List",
                data=high_csv,
                file_name="high_priority_customers.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col3:
        # Summary statistics
        st.markdown(f"""
        <div style="background-color: {SPAR_WHITE}; padding: 10px; border-radius: 8px; text-align: center;">
            <small>
            📊 Summary<br>
            Total: {len(filtered_df):,} customers<br>
            Revenue: ${filtered_df['monetary'].sum():,.0f}<br>
            Avg RFM: {filtered_df['r_score'].mean():.1f}/{filtered_df['f_score'].mean():.1f}/{filtered_df['m_score'].mean():.1f}
            </small>
        </div>
        """, unsafe_allow_html=True)
    
    # =====================================================
    # ANIMATED TREND LINE (Optional)
    # =====================================================
    with st.expander("📈 View Revenue Trend Analysis"):
        # Aggregate revenue by date
        daily_revenue = df.groupby(df['creation_date'].dt.date)['basket_value'].sum().reset_index()
        daily_revenue.columns = ['Date', 'Revenue']
        
        fig = px.line(daily_revenue, x='Date', y='Revenue', 
                     title="Daily Revenue Trend",
                     color_discrete_sequence=[SPAR_RED])
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            hovermode='x unified'
        )
        fig.add_annotation(
            x=daily_revenue['Date'].iloc[-1],
            y=daily_revenue['Revenue'].iloc[-1],
            text="Latest",
            showarrow=True,
            arrowhead=1
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    # Welcome screen
    st.markdown(f"""
    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, {SPAR_WHITE} 0%, {SPAR_GRAY} 100%); border-radius: 20px; margin-top: 50px;">
        <h2 style="color: {SPAR_RED}; font-family: Arial; font-weight: bold;">🎯 SPAR Rewards Intelligence</h2>
        <p style="font-size: 18px; color: #666; margin-top: 20px;">Upload your customer transaction data to unlock powerful insights</p>
        <p style="font-size: 14px; color: #999; margin-top: 30px;">
            Required columns: Member Number, Creation Date, Redeeming Basket Value<br>
            Optional: Redeeming Basket Code, Status
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show example
    with st.expander("📖 View sample data format"):
        sample_df = pd.DataFrame({
            'Member Number': ['M001234', 'M001234', 'M005678'],
            'Creation Date': ['2026-04-01', '2026-03-15', '2026-04-05'],
            'Redeeming Basket Value': [45.50, 32.00, 89.99],
            'Redeeming Basket Code': ['RCP001', 'RCP002', 'RCP003'],
            'Status': ['redeemed', 'redeemed', 'redeemed']
        })
        st.dataframe(sample_df)


# =====================================================
# SPAR REWARDS AI ASSISTANT (Add at the end of your file)
# =====================================================

# SPAR Rewards Knowledge Base
SPAR_REWARDS_INFO = {
    "what is spar rewards": """
    🎯 **SPAR Rewards** is a customer loyalty program designed to reward frequent shoppers at SPAR stores in Zimbabwe.
    
    **Key Benefits:**
    • Earn points on every purchase
    • Redeem points for discounts and vouchers
    • Exclusive member-only promotions
    • Birthday rewards and special offers
    • Priority access to new products
    
    **How it works:**
    1. Sign up for free at any SPAR store
    2. Present your member number at checkout
    3. Earn points on eligible purchases
    4. Redeem vouchers on future visits
    
    🔗 **Official Website:** [SPAR Rewards Zimbabwe](https://www.spar.co.zw/rewards)
    """,
    
    "how to join": """
    📝 **Joining SPAR Rewards is easy and free!**
    
    **Steps to join:**
    1. Visit any SPAR store in Zimbabwe
    2. Ask the cashier for a rewards registration form
    3. Fill in your details (name, phone number, email)
    4. Receive your unique **Member Number**
    5. Start earning points immediately!
    
    **You can also:**
    • Ask at the customer service desk
    • Call SPAR customer care for assistance
    
    🔗 **Learn more:** [https://www.spar.co.zw/rewards](https://www.spar.co.zw/rewards)
    """,
    
    "how to earn points": """
    ⭐ **Earning SPAR Rewards Points:**
    
    **Earn points when you:**
    • Make purchases at any SPAR store
    • Buy selected promotional items (extra points)
    • Shop during double-points events
    • Refer friends to join rewards program
    
    **Points calculation:**
    • Standard rate: 1 point per $1 spent
    • Promotional items: Up to 5x points
    • Birthday month: Double points
    
    **Tips to maximize points:**
    • Always present your member number
    • Watch for weekly specials
    • Shop during promotional periods
    
    🔗 **Current promotions:** [https://www.spar.co.zw/rewards](https://www.spar.co.zw/rewards)
    """,
    
    "how to redeem": """
    🎁 **Redeeming Your SPAR Rewards:**
    
    **Redeem for:**
    • Discount vouchers on next purchase
    • Free products (selected items)
    • Cashback on specific products
    • Exclusive member gifts
    
    **Steps to redeem:**
    1. Accumulate enough points
    2. Ask cashier to check your balance
    3. Choose reward from available options
    4. Voucher applied instantly to your purchase
    
    **Redemption rates:**
    • 100 points = $5 voucher
    • 500 points = $30 voucher
    • 1000+ points = Special rewards
    
    🔗 **View rewards catalog:** [https://www.spar.co.zw/rewards](https://www.spar.co.zw/rewards)
    """,
    
    "benefits": """
    ✨ **SPAR Rewards Member Benefits:**
    
    **Free Benefits:**
    ✅ Free to join - no membership fees
    ✅ Earn points on every purchase
    ✅ Birthday rewards
    ✅ Exclusive member prices
    ✅ Early access to sales
    
    **Premium Benefits (frequent shoppers):**
    👑 Priority checkout lanes
    👑 Special event invitations
    👑 Personalized offers
    👑 Free delivery on large orders
    👑 Dedicated customer service
    
    🔗 **Full benefits list:** [https://www.spar.co.zw/rewards](https://www.spar.co.zw/rewards)
    """,
    
    "contact": """
    📞 **SPAR Rewards Customer Support:**
    
    **Get help with:**
    • Lost member number
    • Points not showing
    • Redemption issues
    • General inquiries
    
    **Contact methods:**
    • In-store: Customer service desk
    • Phone: Call your local SPAR store
    • Email: rewards@spar.co.zw
    
    **Store locator:** Find nearest SPAR on their website
    
    🔗 **Contact page:** [https://www.spar.co.zw/rewards](https://www.spar.co.zw/rewards)
    """,
    
    "troubleshooting": """
    🔧 **Common SPAR Rewards Issues & Solutions:**
    
    **"Points not showing up":**
    • Wait 24-48 hours for points to process
    • Check if you presented your member number
    • Contact store with receipt
    
    **"Can't redeem points":**
    • Ensure you have minimum points (100)
    • Check voucher expiry dates
    • Some products may be excluded
    
    **"Lost member number":**
    • Visit any SPAR store with ID
    • They can look up your number
    • Request a replacement card
    
    **Still having issues?** Visit [https://www.spar.co.zw/rewards](https://www.spar.co.zw/rewards)
    """
}

# Function to get SPAR info response
def get_spar_info_response(question):
    q = question.lower().strip()
    
    # Check for SPAR general questions
    if any(phrase in q for phrase in ['what is spar rewards', 'tell me about spar rewards', 'about spar rewards']):
        return SPAR_REWARDS_INFO["what is spar rewards"]
    
    elif any(phrase in q for phrase in ['how to join', 'sign up', 'register', 'become a member']):
        return SPAR_REWARDS_INFO["how to join"]
    
    elif any(phrase in q for phrase in ['earn points', 'how to earn', 'get points', 'collect points']):
        return SPAR_REWARDS_INFO["how to earn points"]
    
    elif any(phrase in q for phrase in ['redeem', 'how to redeem', 'use points', 'voucher']):
        return SPAR_REWARDS_INFO["how to redeem"]
    
    elif any(phrase in q for phrase in ['benefits', 'advantages', 'perks', 'why join']):
        return SPAR_REWARDS_INFO["benefits"]
    
    elif any(phrase in q for phrase in ['contact', 'support', 'help', 'customer service', 'call']):
        return SPAR_REWARDS_INFO["contact"]
    
    elif any(phrase in q for phrase in ['problem', 'issue', 'not working', 'trouble', 'error']):
        return SPAR_REWARDS_INFO["troubleshooting"]
    
    elif 'website' in q or 'link' in q or 'url' in q:
        return "🔗 **SPAR Rewards Official Website:**\n\n[Click here to visit SPAR Rewards](https://www.spar.co.zw/rewards)\n\nYou can find information about:\n• Current promotions\n• Reward catalog\n• Store locations\n• Latest news and events"
    
    elif 'spar' in q and 'rewards' in q:
        return f"""🛒 **About SPAR Rewards Zimbabwe:**\n\nSPAR Rewards is the official loyalty program of SPAR Zimbabwe, designed to thank loyal customers with points, discounts, and exclusive benefits.\n\n🔗 **Official Website:** [https://www.spar.co.zw/rewards](https://www.spar.co.zw/rewards)\n\n💡 **Try asking:**\n• "How do I join SPAR Rewards?"\n• "How to earn points?"\n• "What are the benefits?"\n• "How to redeem vouchers?"\n• "Contact customer support" """
    
    return None

# Function to answer data questions
def get_data_response(question, rfm, df):
    q = question.lower()
    
    # Data-specific questions
    if any(word in q for word in ['total customers', 'how many customers', 'customer count']):
        return f"👥 **Total Customers:** {len(rfm):,} unique members have redeemed rewards in your SPAR program."
    
    elif any(word in q for word in ['total revenue', 'total sales', 'revenue total']):
        return f"💰 **Total Revenue:** ${rfm['monetary'].sum():,.2f}\n\n**Average per customer:** ${rfm['monetary'].mean():,.2f}"
    
    elif any(word in q for word in ['average', 'avg spend', 'average basket']):
        return f"📊 **Average Metrics:**\n• Avg spend per customer: ${rfm['monetary'].mean():,.2f}\n• Avg basket value: ${df['basket_value'].mean():,.2f}\n• Avg transactions per customer: {rfm['frequency'].mean():.1f}"
    
    elif any(word in q for word in ['at risk', 'risk customers', 'churn risk']):
        at_risk = len(rfm[rfm['segment'] == '⚠️ At Risk'])
        churned = len(rfm[rfm['segment'] == '💔 Churned'])
        return f"⚠️ **Customer Risk Analysis:**\n\n• At Risk: {at_risk} customers\n• Churned: {churned} customers\n• Total needing attention: {at_risk + churned}\n\n💡 Action: Send retention offers to these customers."
    
    elif any(word in q for word in ['champion', 'top customers', 'best customers']):
        champions = len(rfm[rfm['segment'] == '👑 Champions'])
        top5 = rfm.nlargest(5, 'monetary')
        response = f"🏆 **Champions:** {champions} high-value customers\n\n**Top 5 Customers by Spend:**\n"
        for i, (_, row) in enumerate(top5.iterrows(), 1):
            response += f"{i}. Member {row['member_number']}: ${row['monetary']:,.2f} ({row['frequency']} transactions)\n"
        return response
    
    elif 'segment' in q or 'breakdown' in q:
        segments = rfm['segment'].value_counts()
        response = "📊 **Customer Segment Distribution:**\n\n"
        for seg, count in segments.items():
            pct = (count/len(rfm))*100
            response += f"{seg}: {count} customers ({pct:.1f}%)\n"
        return response
    
    elif 'recommend' in q or 'action' in q or 'what should i do' in q:
        high = len(rfm[rfm['priority'] == 'High'])
        medium = len(rfm[rfm['priority'] == 'Medium'])
        return f"""🎯 **SPAR Rewards Recommended Actions:**

🔴 **Immediate (High Priority - {high} customers):**
• Send 25% discount to at-risk members
• Re-engagement email campaign
• Call or SMS churned customers

🟡 **Short-term (Medium Priority - {medium} customers):**
• Welcome back offers for one-time buyers
• Double points weekend for loyal members
• Birthday rewards this month

🟢 **Long-term Strategy:**
• VIP program for champions
• Referral rewards program
• Seasonal promotions

📊 **Expected impact:** Retaining {high} at-risk customers could save ${rfm[rfm['priority'] == 'High']['monetary'].sum():,.2f} in potential lost revenue."""
    
    return None

# =====================================================
# AI ASSISTANT INTERFACE (Add to sidebar)
# =====================================================
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🤖 SPAR AI Assistant")
    st.markdown("*Ask me anything about SPAR Rewards or your data*")
    
    # Initialize chat
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = [
            {"role": "assistant", "content": "👋 Hi! I'm your SPAR Rewards AI assistant. I can help you with:\n\n📌 **SPAR Rewards info** - How to join, earn points, redeem vouchers\n📊 **Your data** - Customer insights, revenue, segments\n💡 **Recommendations** - Actions to improve retention\n\nWhat would you like to know?"}
        ]
    
    # Display chat history
    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    if user_question := st.chat_input("Ask about SPAR Rewards or your data..."):
        # Add user message
        st.session_state.ai_messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Generate response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # Check if data is loaded
            data_loaded = 'file' in locals() and file is not None and 'rfm' in locals()
            
            # Try to get response
            response = None
            
            # First check SPAR knowledge base
            spar_response = get_spar_info_response(user_question)
            if spar_response:
                response = spar_response
            
            # Then check data questions if data is loaded
            elif data_loaded:
                data_response = get_data_response(user_question, rfm, df)
                if data_response:
                    response = data_response
            
            # Default response
            if not response:
                if data_loaded:
                    response = f"""🤔 I can help you with:

**SPAR Rewards info:**
• What is SPAR Rewards?
• How to join or earn points?
• How to redeem vouchers?
• Benefits of membership?
• Contact customer support

**Your Data Analysis:**
• Total customers and revenue
• At-risk customers
• Top performing segments
• Recommended actions
• Customer breakdown

**Try asking:** "What is SPAR Rewards?" or "Show me my top customers"

🔗 **Official website:** [https://www.spar.co.zw/rewards](https://www.spar.co.zw/rewards)"""
                else:
                    response = f"""📂 **Please upload your SPAR data first** using the file uploader above, then I can analyze your customer data.

In the meantime, I can answer questions about SPAR Rewards:

**Try asking:**
• "What is SPAR Rewards all about?"
• "How do I join SPAR Rewards?"
• "How to earn points?"
• "How to redeem vouchers?"
• "What are the benefits?"
• "SPAR Rewards website link"

🔗 **Official website:** [https://www.spar.co.zw/rewards](https://www.spar.co.zw/rewards)"""
            
            response_placeholder.markdown(response)
            st.session_state.ai_messages.append({"role": "assistant", "content": response})

# Optional: Add a quick link button in the main area
st.markdown("---")
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("""
    <div style="text-align: center; padding: 10px; background-color: #f0f0f0; border-radius: 10px;">
        <p style="margin: 0;">
        🔗 <strong>Official SPAR Rewards Website:</strong> 
        <a href="https://www.spar.co.zw/rewards" target="_blank" style="color: #E31837; text-decoration: none;">
        https://www.spar.co.zw/rewards
        </a>
        </p>
    </div>
    """, unsafe_allow_html=True)