import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Trader Sentiment Dashboard", layout="wide")

st.title("📊 Trader Sentiment Dashboard")

# -----------------------------
# Load & Prepare Data
# -----------------------------
@st.cache_data
def load_data():
    fear = pd.read_csv("fear_greed_index.csv")
    trades = pd.read_csv("historical_data.csv")

    fear.columns = fear.columns.str.strip().str.lower()
    trades.columns = trades.columns.str.strip().str.lower()

    fear['date'] = pd.to_datetime(fear['date']).dt.normalize()

    trades['timestamp ist'] = pd.to_datetime(
        trades['timestamp ist'],
        format="%d-%m-%Y %H:%M"
    )
    trades['date'] = trades['timestamp ist'].dt.normalize()

    merged = trades.merge(
        fear[['date','classification']],
        on='date',
        how='left'
    )

    # Daily metrics
    daily_pnl = merged.groupby(['date','classification'])['closed pnl'].sum().reset_index()
    daily_pnl.rename(columns={'closed pnl':'daily_pnl'}, inplace=True)

    trade_count = merged.groupby(['date','classification']).size().reset_index(name='trade_count')

    daily = daily_pnl.merge(trade_count, on=['date','classification'])

    return daily

daily_metrics = load_data()

# -----------------------------
# Sidebar Filter
# -----------------------------
st.sidebar.header("Filter Options")

sentiments = st.sidebar.multiselect(
    "Select Sentiment",
    options=daily_metrics['classification'].unique(),
    default=daily_metrics['classification'].unique()
)

filtered = daily_metrics[daily_metrics['classification'].isin(sentiments)]

# -----------------------------
# KPI Section
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Avg Daily PnL", round(filtered['daily_pnl'].mean(),2))
col2.metric("Avg Trades per Day", round(filtered['trade_count'].mean(),2))
col3.metric("Total Trading Days", filtered['date'].nunique())

st.markdown("---")

# -----------------------------
# Graph 1 — PnL Distribution
# -----------------------------
st.subheader("📈 Daily PnL Distribution by Sentiment")

fig1 = plt.figure(figsize=(10,6))
sns.boxplot(
    data=filtered,
    x='classification',
    y='daily_pnl'
)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig1)

# -----------------------------
# Graph 2 — Trade Activity
# -----------------------------
st.subheader("📊 Trade Activity by Sentiment")

freq_stats = filtered.groupby('classification')['trade_count'].mean()

fig2 = plt.figure(figsize=(8,5))
freq_stats.plot(kind='bar')
plt.ylabel("Average Trades per Day")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)

# -----------------------------
# Graph 3 — Trade Frequency vs PnL
# -----------------------------
st.subheader("🔎 Trade Frequency vs Daily PnL")

fig3 = plt.figure(figsize=(10,6))
sns.scatterplot(
    data=filtered,
    x='trade_count',
    y='daily_pnl',
    alpha=0.5
)
plt.tight_layout()
st.pyplot(fig3)

st.markdown("---")
st.success("Dashboard Loaded Successfully 🚀")