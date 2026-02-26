# Trader-Sentiment-Analysis
Trader Performance vs Market Sentiment

Data Science Intern Assignment

---

## Objective

This project analyzes the relationship between market sentiment (Fear & Greed Index) and trader behavior using historical trading data.

The goal was to understand how different sentiment regimes (Extreme Fear to Extreme Greed) influence:

- Trading activity
- Profitability (Daily PnL)
- Volatility
- Risk-taking behavior

Based on the findings, actionable strategy recommendations were derived.

---

## Dataset

Two datasets were used:

- Bitcoin Fear & Greed Index
- Historical trader transaction data

Both datasets were cleaned and aligned at the daily level using normalized timestamps before merging.

## How to Run Locally

Install dependencies:

pip install -r requirements.txt

Run the dashboard:

streamlit run app/app.py

Run the notebook:

jupyter notebook notebooks/analysis.ipynb
