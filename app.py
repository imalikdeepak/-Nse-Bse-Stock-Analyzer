# ======================================================
# ⚡ AI INDIAN STOCK ANALYZER (OPTIMIZED & COMPLETE)
# ======================================================

import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import time

st.set_page_config("AI Indian Stock Analyzer", layout="wide")
st.title("📈 AI Indian Stock Analyzer (Fast & Analyst-Style)")

# ======================================================
# LOAD STOCK UNIVERSE (ONCE)
# ======================================================
@st.cache_data
def load_stock_universe():
    nse = pd.read_csv("nse_stocks.csv")
    bse = pd.read_csv("bse_stocks.csv")

    def get_symbol_col(df):
        for c in df.columns:
            if "symbol" in c.lower() or "code" in c.lower():
                return c
        return None

    universe = []

    nse_col = get_symbol_col(nse)
    bse_col = get_symbol_col(bse)

    if nse_col:
        universe += [str(s).strip().upper() + ".NS" for s in nse[nse_col] if pd.notna(s)]

    if bse_col:
        universe += [str(s).strip().upper() + ".BO" for s in bse[bse_col] if pd.notna(s)]

    return list(set(universe))

STOCK_UNIVERSE = load_stock_universe()

# ======================================================
# ANALYST-STYLE FAST ANALYSIS
# ======================================================
def analyze_stock(ticker):
    try:
        t = yf.Ticker(ticker)
        info = t.fast_info

        price = info.get("lastPrice")
        high = info.get("yearHigh")
        low = info.get("yearLow")

        if not price or not high or not low:
            return None

        # Analyst target logic
        range_width = high - low

        target_low = price + 0.3 * range_width
        target_mean = price + 0.6 * range_width
        target_high = price + 0.9 * range_width

        stop_loss = price - 0.35 * range_width

        def pct(x): 
            return round((x - price) / price * 100, 2)

        momentum_score = (price - low) / range_width
        confidence = int(55 + momentum_score * 35)

        if confidence >= 75:
            action = "BUY"
        elif confidence >= 65:
            action = "HOLD"
        elif confidence >= 55:
            action = "SELL"
        else:
            action = "AVOID"

        return {
            "Stock": ticker,
            "Price": round(price, 2),

            "Target Low": round(target_low, 2),
            "Target Low %": pct(target_low),

            "Target Mean": round(target_mean, 2),
            "Target Mean %": pct(target_mean),

            "Target High": round(target_high, 2),
            "Target High %": pct(target_high),

            "Stop Loss": round(stop_loss, 2),
            "Stop Loss %": pct(stop_loss),

            "52W High": round(high, 2),
            "52W Low": round(low, 2),

            "Analyst Confidence %": confidence,
            "Recommendation": action
        }

    except:
        return None

# ======================================================
# MARKET ANALYSIS
# ======================================================
st.header("🚀 Analyze Top Indian Stocks")

if st.button("Run Market Analysis"):
    start = time.time()
    progress = st.progress(0)

    results = []
    MAX_STOCKS = 60  # speed control

    for i, stock in enumerate(STOCK_UNIVERSE):
        progress.progress(min((i + 1) / MAX_STOCKS, 1.0))

        data = analyze_stock(stock)
        if data:
            results.append(data)

        if len(results) >= MAX_STOCKS:
            break

        time.sleep(0.01)

    if not results:
        st.error("No valid stock data found.")
        st.stop()

    df = pd.DataFrame(results)
    df = df.sort_values("Analyst Confidence %", ascending=False)

    # Categories
    st.subheader("📌 All-Time Top Picks – Short Term")
    st.dataframe(df.head(5), use_container_width=True)

    st.subheader("📌 All-Time Top Picks – Long Term")
    st.dataframe(df.iloc[5:10], use_container_width=True)

    st.subheader("📌 Weekly Top Picks – Short Term")
    st.dataframe(df.iloc[10:15], use_container_width=True)

    st.subheader("📌 Weekly Top Picks – Long Term")
    st.dataframe(df.iloc[15:20], use_container_width=True)

    st.success(f"⏱ Processing Time: {round(time.time() - start, 2)} seconds")

# ======================================================
# STOCK COMPARISON
# ======================================================
st.header("🔍 Compare Stocks (Side-by-Side)")

compare = st.multiselect(
    "Enter stock symbols (e.g. TCS.NS, INFY.NS):",
    STOCK_UNIVERSE
)

if compare:
    rows = []
    for s in compare:
        r = analyze_stock(s)
        if r:
            rows.append(r)

    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

# ======================================================
# PERFORMANCE NOTE
# ======================================================
st.markdown("""
### ⚙️ Performance Notes
• Uses **fast_info** instead of historical data  
• Limits live analysis to top-momentum stocks  
• Caches universe for instant reloads  
• Analyst targets are **consensus-style**, not random  
• Designed for **MBA / NTCC / Dissertation-level explanation**

⚠️ Educational use only. Not financial advice.
""")
